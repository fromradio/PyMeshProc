# author: Ruimin Wang (ruimin.wang13@gmail.com)
# practice on python implementing simple halfedge datastructure

import numpy as np
import os
# simple geometric kernel
from geometry import *

class Vertex(object):
	"""
	class for vertex:
		geometry
	"""
	def __init__(self,x=0.0,y=0.0,z=0.0):
		self._point = Point(x,y,z)
		self._vertexbegin= None;
	# overload '__repr__', print the geometric position
	def __repr__(self):
		return "The geometric position is (%f,%f,%f)"%(self._point.x,self._point.y,self._point.z)
	# overload '__str__', the same as '__repr__'
	def __str__(self):
		return "The geometric position is (%f,%f,%f)"%(self._point.x,self._point.y,self._point.z)
	# 'point' property
	@property 
	def point(self):
		return self._point
	@point.setter
	def point(self,val):
		if isinstance(val,Point):
			self._point = val.copy()
		else:
			raise ValueError("The type should be a Point")
	# halfedge
	def vertexbegin():
		return _vertexbegin;

	# debug function
	def debug(self):
		print self._point

class Halfedge(object):
	"""
	'Halfedge' data structure
	"""
	def __init__(self):
		# opposite halfedge
		self._oppo = None
		# previous halfedge
		self._prev = None
		# next halfedge
		self._next = None
		# vertex handle
		self._vertex = Vertex()
		# is border
		self._isBorder = False
		# facet
		self._facet = None
	def opposite(self):
		return self._oppo
	def setOpposite(self,val):
		if isinstance(val,Halfedge):
			self._oppo = val
		else:
			raise ValueError("Type Error: Should be 'Halfedge'")
	def prev(self):
		return self._prev
	def setPrev(self,val):
		if isinstance(val,Halfedge):
			self._prev = val
		else:
			raise ValueError("The type should be 'Halfedge'")
	def next(self):
		return self._next
	def setNext(self,val):
		if isinstance(val,Halfedge):
			self._next = val
		else:
			raise ValueError("The type should be 'Halfedge'")
	def vertex(self):
		return self._vertex
	def setVertex(self,val):
		if isinstance(val,Vertex):
			self._vertex = val
		else:
			raise ValueError("The type should be 'Vertex'")
	def facet(self):
		return self._facet
	def setFacet(self,val):
		if isinstance(val,Facet):
			self._facet = val
		else:
			raise ValueError("Type Error: Should be 'Facet'")

	def isBorder(self):
		return self._isBorder

class Facet(object):
	def __init__(self):
		pass

class MeshConstruction(object):
	def __init__(self):
		# facet list
		self._facetList = []
		self._mesh = None

	def meshConstruction(self,mesh):
		if not isinstance(mesh,Mesh):
			raise ValueError("the type should be 'Mesh'")
		else:
			self._mesh = mesh
			self.readFromFile()
	def readFromFile(self):
		if self._mesh is None:
			raise ValueError("The mesh is None")
		if self._mesh._filename == '':
			raise ValueError("The filename should not be none")
		objFile = open(self._mesh._filename,'r')

		count = 0
		faceList = []
		for l in objFile:
			splited = l.split()
			if len(splited) == 0:
				pass
			elif splited[0] == 'v':
				# the vertex
				x = float(splited[1])
				y = float(splited[2])
				z = float(splited[3])
				v = Vertex(x,y,z)
				self._mesh.appendVertex(v)
			elif splited[0] == 'f':
				# the facet
				vl = []
				for i in range(1,len(splited)):
					# in case of vt
					splitedFaceData = splited[i].split('/')
					# set the index (0 as beginning)
					vl.append(int(splitedFaceData[0])-1)
				# push the vertex list
				faceList.append(vl)
				if count == 8000:
					print vl
			count += 1
		# halfedge construction
		self.halfedgeConstruction(faceList)
		# the mesh organize some information
		self._mesh.selfCombination()

		# some debug
		print "There are ",len(self._mesh._halfedges)," halfedges"
	def halfedgeConstruction(self,facetList):
		"""
		Construct the halfedge structure based on the facetList
		"""
		edges = []
		# the temporary map of the halfedges
		edgeMap = {}
		count = 0
		for i in range(0,len(facetList)):
			# 
			for j in range(0,len(facetList[i])):
				# j is the index of the current vertex
				key = (facetList[i][j-1],facetList[i][j])
				edges.append(key)
				edgeMap[key] = count
				count += 1
				# initialze the current halfedge
				he = Halfedge()
				# assume that the mesh has been well oriented
				he.setVertex(self._mesh._vertices[facetList[i][j]])
				self._mesh._halfedges.append(he)
		# construct the opposite halfedge
		for key in edgeMap:
			i = edgeMap[key]
			if self._mesh._halfedges[i].opposite() is None:
				# the opposite has not been set
				oppo = key[1],key[0]
				if oppo in edgeMap:
					# interior edge
					j = edgeMap[oppo]
					self._mesh._halfedges[i].setOpposite(self._mesh._halfedges[j])
					self._mesh._halfedges[j].setOpposite(self._mesh._halfedges[i])
				else:
					# border edge
					# construct a border halfedge
					he = Halfedge()
					# the edge is border edge
					he._isBorder = True
					self._mesh._halfedges[i].setOpposite(he)
					he.setOpposite(self._mesh._halfedges[i])
					# append the halfedge
					self._mesh._halfedges.append(he)
					count += 1
		# set next and prev halfedge
		# the interior edges
		count = 0
		for i in range(0,len(facetList)):
			for j in range(0,len(facetList[i])):
				if j == len(facetList[i])-1:
					# the last edge: the next edge is the beggining edge
					self._mesh._halfedges[count+j].setNext(self._mesh._halfedges[count])
					self._mesh._halfedges[count+j].setPrev(self._mesh._halfedges[count+j-1])
				elif j == 0:
					# the beginning edge: the prev edge is the last one
					self._mesh._halfedges[count+j].setNext(self._mesh._halfedges[count+j+1])
					self._mesh._halfedges[count+j].setPrev(self._mesh._halfedges[count+len(facetList[i])-1])
				else:
					# the interior edge
					self._mesh._halfedges[count+j].setNext(self._mesh._halfedges[count+j+1])
					self._mesh._halfedges[count+j].setPrev(self._mesh._halfedges[count+j-1])
			# the count
			count += len(facetList[i])
		# the border edges
		for i in range(count,len(self._mesh._halfedges)):
			he = self._mesh._halfedges[i]
			# first set the vertex
			he.setVertex(he.opposite().prev().vertex())
			# two kinds of situation
			if he.opposite().prev().opposite().isBorder():
				he.setNext(he.opposite().prev().opposite())
			else:
				he.setNext(he.opposite().prev().opposite().prev().opposite())
			if he.opposite().next().opposite().isBorder():
				he.setPrev(he.opposite().next().opposite())
			else:
				he.setPrev(he.opposite().next().opposite().next().opposite())
			
class Mesh(object):
	"""
	the class for mesh
	"""
	def __init__(self):
		self._vertices = []
		self._halfedges = []
		self._facets = []
		self._filename = ''
		self._sizeOfVertices=0

	def readFile(self,filename):
		# read from a file
		ext = os.path.splitext(filename)
		print ext[-1]
		if ext[-1] != ".obj":
			print "only support obj file right now"
			return None
		self._filename = filename
		mc =MeshConstruction()
		mc.meshConstruction(self)
	# construct the halfedge structure via facet information
	def constructFromFaceStructure(self,faceList):
		for facet in facetList:
			pass
	# append the vertex
	def appendVertex(self,vertex):
		if not isinstance(vertex,Vertex):
			raise ValueError("Type Error, should be 'Vertex'")
		else:
			self._vertices.append(vertex)
	# compute some necessary values
	def selfCombination(self):
		self._sizeOfVertices = len(self._vertices)

	# obtain the i-th vertex
	def vertex(self,i):
		if i < 0 or i >= self._sizeOfVertices:
			raise ValueError("Index out of range via obtaining the vertex")
		else:
			return self._vertices[i]

	def vertices(self):
		return self._vertices
	def destory(self):
		self._vertices.clear()
		self._halfedges.clear()
		self._facets.clear()
"""
debug
"""
def main():
	v = Vertex()
	v.point.x = 1.0
	v.debug()
	m = Mesh()
	m.readFile("test.obj")
	#mc = MeshConstruction()
	#mc.meshConstruction(m)
	print len(m._vertices)
	print m.vertex(2)

if __name__=='__main__':
	main()

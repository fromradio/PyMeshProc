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
		# previous halfedge
		self._prev = None
		# next halfedge
		self._next = None
		# vertex handle
		self._vertex = Vertex()
		# is border
		self._isBorder = True
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
		self._mesh.selfCombination()
			
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

	# get the i-th vertex
	def vertex(self,i):
		if i < 0 or i >= self._sizeOfVertices:
			raise ValueError("Index out of range via obtaining the vertex")
		else:
			return self._vertices[i]
"""
debug
"""
def main():
	v = Vertex()
	v.point.x = 1.0
	v.debug()
	m = Mesh()
	m.readFile("test.obj")
	mc = MeshConstruction()
	mc.meshConstruction(m)
	print len(m._vertices)
	print m.vertex(2)

if __name__=='__main__':
	main()

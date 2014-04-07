# author: Ruimin Wang (ruimin.wang13@gmail.com)
# practice on python implementing simple halfedge datastructure

import numpy as np
import os
from geometry import *

class Vertex(object):
	"""
	class for vertex:
		geometry
	"""
	def __init__(self,x=0.0,y=0.0,z=0.0):
		self._point = Point(x,y,z)
		self._vertexbegin= None;

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
		for l in objFile:
			splited = l.split()
			if splited[0] == 'v':
				# the vertex
				self._mesh
			count += 1
			
			
class Mesh(object):
	"""
	the class for mesh
	"""
	def __init__(self):
		self._vertices = []
		self._halfedges = []
		self._facets = []
		self._filename = ''

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

if __name__=='__main__':
	main()

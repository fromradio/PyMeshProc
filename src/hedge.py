# author: Ruimin Wang (ruimin.wang13@gmail.com)
# practice on python implementing simple halfedge datastructure

import numpy as np
import os

class vertex:
	"""
	class for vertex:
		geometry
	"""
	def __init__(self):
		pass

class halfedge:
	def __init__(self):
		pass

class facet:
	def __init__(self):
		pass

class Mesh:
	"""
	the class for mesh
	"""
	def __init__(self):
		self.vertices = []
		self.halfedges = []
		self.facets = []

	def readFile(self,filename):
		# read from a file
		ext = os.path.splittext(filename)
		if ext != ".obj":
			print "only support obj file right now"
			return None
		

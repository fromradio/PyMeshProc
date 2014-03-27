#! /usr/bin/env python
# written by Ruimin Wang(ruimin.wang13@gmail.com)

import math
import numpy as np

class Point(object):
	def __init__(self,x=0.,y=0.,z=0.):
		self.coordinate = np.array([x,y,z],dtype = np.float64)
		self._x = 100
		print self.coordinate
	#def test(self):
	#	print self.coordinate[0]

	# access to the three coordinates
	@property
	def x(self):
		return self.coordinate[0]
	@x.setter
	def x(self,value):
		if isinstance(value,int) or isinstance(value,float):
			self.coordinate[0] = value
		else:
			raise ValueError("please input interger or float")

	@property
	def y(self):
		return self.coordinate[1]
	@y.setter
	def y(self,value):
		if isinstance(value,int) or isinstance(value,float):
			self.coordinate[1] = value
		else:
			raise ValueError("please input interger or float")

	@property 
	def z(self):
		return self.coordinate[2]
	@z.setter
	def z(self,value):
		if isinstance(value,int) or isinstance(value,float):
			self.coordinate[2] = value
		else:
			raise ValueError("please input interger or float")

	def set(self,x,y,z):
		self.coordinate = np.array([x,y,z],dtype = np.float64)

	def __repr__(self):
		return "Point(%f,%f,%f)"%(self.coordinate[0],self.coordinate[1],self.coordinate[2])
	def __str__(self):
		return "Point(%f,%f,%f)"%(self.coordinate[0],self.coordinate[1],self.coordinate[2])
	def __add__(self,vec):
		if isinstance(vec,Vector):
			return Point(self.x+vec.x,self.y+vec.y,self.z+vec.z)
		else:
			raise ValueError("The object should be a Vector")

	def __sub__(self,pt):
		if isinstance(pt,Point):
			return Vector(self.x-pt.x,self.y-pt.y,self.z-pt.z)
		else:
			raise ValueError("The object should be a Point")
	def __eq__(self,pt):
		return isinstance(pt,Point) and self.x==pt.x and self.y==pt.y and self.z==pt.z
	def __ne__(self,pt):
		return not (self==pt)

class Vector(object):
	def __init__(self,x=0.,y=0.,z=0.):
		self.coordinate = np.array([x,y,z],dtype = np.float64)


	# data access
	@property
	def x(self):
		return self.coordinate[0]
	@x.setter
	def x(self,value):
		if isinstance(value,int) or isinstance(value,float):
			self.coordinate[0] = value
		else:
			raise ValueError("please input interger or float")

	@property
	def y(self):
		return self.coordinate[1]
	@y.setter
	def y(self,value):
		if isinstance(value,int) or isinstance(value,float):
			self.coordinate[1] = value
		else:
			raise ValueError("please input interger or float")

	@property 
	def z(self):
		return self.coordinate[2]
	@z.setter
	def z(self,value):
		if isinstance(value,int) or isinstance(value,float):
			self.coordinate[2] = value
		else:
			raise ValueError("please input interger or float")

	# setter to three directions
	def set(x,y,z):
		self.coordinate = np.array([x,y,z],dtype = np.float64)

	# __repr__
	def __repr__(self):
		return "Vector(%f,%f,%f)"%(self.coordinate[0],self.coordinate[1],self.coordinate[2])
	def __str__(self):
		return "Vector(%f,%f,%f)"%(self.coordinate[0],self.coordinate[1],self.coordinate[2])
# for debug:
def main():
	pt = Point(0.0,0.0,1.0)
	pt2 = Point(1.0,0.0,0.0)
	print pt-pt2
	vec = Vector(3.0,0.0,0.0)
	print pt+vec

	#print pt.x()
if __name__ == '__main__':
	main()
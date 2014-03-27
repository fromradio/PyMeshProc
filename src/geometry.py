#! /usr/bin/env python
# written by Ruimin Wang(ruimin.wang13@gmail.com)

import math
import numpy as np

################################################################
class Point(object):
	"""
	the point class
	notice:
		property x,y,z
	"""
	def __init__(self,x=0.,y=0.,z=0.,ar = None):
		if ar is None:
			self.coordinate = np.array([x,y,z],dtype = np.float64)
		else:
			self.coordinate = ar
	#def __init__(self,ar):
	#	self.coordinate = ar
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

	@staticmethod
	def Origin():
		return Point()

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

########################################################################
class Vector(object):
	"""
	the vector class
	"""
	def __init__(self,x=0.,y=0.,z=0.,ar =None):
		if ar is not None:
			self.coordinate = ar
		else:
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
	def set(self,x,y,z):
		self.coordinate = np.array([x,y,z],dtype = np.float64)

	# __repr__
	def __repr__(self):
		return "Vector(%f,%f,%f)"%(self.coordinate[0],self.coordinate[1],self.coordinate[2])
	def __str__(self):
		return "Vector(%f,%f,%f)"%(self.coordinate[0],self.coordinate[1],self.coordinate[2])
	# some basic operations
	# compute the norm
	def norm(self):
		return np.linalg.norm(self.coordinate)
	def normalize(self):
		n = self.norm()
		if n != 0:
			self.coordinate = self.coordinate/n
			return Vector(ar=self.coordinate)
		else:
			return Vector(ar=self.coordinate)
	def normalized(self):
		n = self.norm()
		if n != 0:
			return Vector(ar=(self.coordinate/n))
		else:
			return Vector(ar=self.coordinate)
	# overloadded operators
	def __add__(self,vec):
		if isinstance(vec,Vector):
			return Vector(self.x+vec.x,self.y+vec.y,self.z+vec.z)
		else:
			raise ValueError("The object should be a Vector")
	def __sub__(self,vec):
		if isinstance(vec,Vector):
			return Point(self.x-vec.x,self.y-vec.y,self.z-vec.z)
		else:
			raise ValueError("The object should be a Vector")
	def __eq__(self,vec):
		return isinstance(vec,Vector) and self.x==vec.x and self.y==vec.y and self.z==vec.z
	def __ne__(self,vec):
		return not (self==vec)
	def __neg__(self):
		return Vector(-self.x,-self.y,-self.z)
	def __mul__(self,val):
		if isinstance(val,Vector):
			return self.x*val.x+self.y*val.y+self.z*val.z
		elif isinstance(val,int) or isinstance(val,float):
			return Vector(self.x*val,self.y*val,self.z*val)
		else:
			raise ValueError("The object should be a Vector or scalar")
	def __rmul__(self,val):
		return self*val
	def __div__(self,val):
		if isinstance(val,int) or isinstance(val,float):
			if val == 0:
				raise ValueError("cannot div with zero value")
			else:
				return Vector(self.x/val,self.y/val,self.z/val)
		else:
			raise ValueError("The object should be a scalar")
	def __xor__(self,vec):
		if isinstance(vec,Vector):
			return Vector(self.y*vec.z-self.z*vec.y,self.z*vec.x-self.x*vec.z,self.x*vec.y-self.y*vec.x)
		else:
			raise ValueError("The object should be a Vector")

##########################################################################
class Matrix4x4(object):
	"""
	class for 4 times 4 Matrix
	This matrix is frequently used in opengl operations
	"""
	def __init__(self):
		self.mat = np.identity(4,dtype = np.float64)

	def setIdentity():
		self.mat = np.identity(4,dtype = np.float64)

	@property 
	def matrix(self):
		return self.mat
	@matrix.setter
	def matrix(self,val):
		if isinstance(val,np.array):
			self.mat = val
		else:
			raise ValueError("The object should be a numpy matrix")
	# overload
	def __repr__(self):
		return "Matrix:\n"+self.mat.__repr__()
	def __str__(self):
		return "Matrix:\n"+self.mat.__str__()

	# methods:
	@staticmethod
	def translation(vec):
		M = Matrix4x4()
		M.mat[0,3]=vec.x
		M.mat[1,3]=vec.y
		M.mat[2,3]=vec.z
		return M
	@staticmethod
	def rotationAroundOrigin(angleInRadians,axisVec):
		# normalize axisVector at first
		if axisVec.norm == 0:
			raise ValueError("the norm of axis is zero")
		axisVector = axisVec.normalized()
		c = math.cos(angleInRadians)
		s = math.sin(angleInRadians)
		oc = 1-c
		M = Matrix4x4()
		M.mat[0,0] = c+oc*axisVector.x*axisVector.x
		M.mat[1,1] = c+oc*axisVector.y*axisVector.y
		M.mat[2,2] = c+oc*axisVector.z*axisVector.z
		M.mat[1,0] = M.mat[0,1]=oc*axisVector.x*axisVector.y
		M.mat[2,0] = M.mat[0,2]=oc*axisVector.x*axisVector.z
		M.mat[2,1] = M.mat[1,2]=oc*axisVector.y*axisVector.z

		xs = axisVector.x*s
		ys = axisVector.y*s
		zs = axisVector.z*s
		M.mat[1,0] += zs
		M.mat[0,1] -= zs
		M.mat[2,0] -= ys
		M.mat[0,2] += ys
		M.mat[2,1] += xs
		M.mat[1,2] -= xs

		return M
	@staticmethod
	def rotation(angleInRadians,axisVec,originPoint):
		v = originPoint-Point.Origin()
		return Matrix4x4.translation(v)*Matrix4x4.rotationAroundOrigin(angleInRadians,axisVec)*Matrix4x4.translation(-v)
	@staticmethod
	def uniformScaleAroundOrigin(scale):
		M = Matrix4x4()
		M.mat = scale*M.mat
		M.mat[3,3]=1.0
		return M

	@staticmethod
	def uniformScale(scale,originPt):
		v = originPt-Point.Origin()
		print v
		print Matrix4x4.translation(v)
		print Matrix4x4.translation(v)*Matrix4x4.uniformScaleAroundOrigin(scale)
		return Matrix4x4.translation(v)*Matrix4x4.uniformScaleAroundOrigin(scale)*Matrix4x4.translation(-v)
	@staticmethod
	def lookAt(eyePoint,targetPoint,upVector,isInverted):
		# generate a rotation matrix
		z = (eyePoint-targetPoint).normalized()
		y = upVector
		x = y^z
		y = z^x

		x = x.normalized()
		y = y.normalized()

		M = Matrix4x4()
		if isInverted:
			M.mat[0,0] = x.x; M.mat[0,1] = y.x; M.mat[0,2] = z.x;
			M.mat[1,0] = x.y; M.mat[1,1] = y.y; M.mat[1,2] = z.y;
			M.mat[2,0] = x.z; M.mat[2,1] = y.z; M.mat[2,2] = z.z;
			return Matrix4x4.translation(eyePoint-Point.Origin)*M
		else:
			M.mat[0,0] = x.x; M.mat[0,1] = x.y; M.mat[0.2] = x.z;
			M.mat[1,0] = y.x; M.mat[1,1] = y.y; M.mat[1,2] = y.z;
			M.mat[2,0] = z.x; M.mat[2,1] = z.y; M.mat[2,2] = z.z;
			return M*Matrix4x4.translation(-(eyePoint-Point.Origin))

	def __mul__(a,b):
		if isinstance(a,Matrix4x4):
			if isinstance(b,Matrix4x4):
				M = Matrix4x4()
				M.mat = np.dot(a.mat,b.mat)
				print M.mat
				return M
			elif isinstance(b,Vector):
				tv = np.dot(a.mat[0:3,0:3],b.coordinate)
				return Vector(ar = tv)
			elif isinstance(b,Point):
				return Point(a.mat[0,0]*b.x+a.mat[0,1]*b.y+a.mat[0,2]*b.z+a.mat[0,3],a.mat[1,0]*b.x+a.mat[1,1]*b.y+a.mat[1,2]*b.z+a.mat[1,3],a.mat[2,0]*b.x+a.mat[2,1]*b.y+a.mat[2,2]*b.z+a.mat[2,3])
			else:
				raise ValueError("wrong type for multiply of matrix")
		else:
			raise ValueError("wrong type for multiply of matrix")


# for debug:
def main():
	pt = Point(0.0,0.0,1.0)
	pt2 = Point(1.0,0.0,0.0)
	print pt-pt2
	vec = Vector(3.0,0.0,0.0)
	print pt+vec
	vec2 = Vector(3.0,0.0,0.0)
	print vec==vec2
	vec2.set(4.0,1.0,3.0)
	print vec^vec2
	mat = Matrix4x4()
	print mat
	print mat.matrix
	mat.matrix[1,2] = 10
	print mat.matrix
	print mat.translation(vec2)
	print Matrix4x4().translation(vec2)
	print 'rotation test'
	print Matrix4x4.rotationAroundOrigin(1.57,vec2)
	print 'scale test'
	print Matrix4x4.uniformScale(3,Point(1,0,0))
	print 'multipy test'
	print Matrix4x4()*vec2
	print Matrix4x4()*(Point.Origin()+vec2)

	#print pt.x()
if __name__ == '__main__':
	main()
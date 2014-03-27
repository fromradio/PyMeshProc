#! /usr/bin/env python

from OpenGL.GL import *
from geometry import *
import math

class camera:
	def __init__(self):
		self.FIELD_OF_VIEW_IN_DEGREES = 30.0
		self.ORBITING_SPEED_IN_DEGREES_PER_RADIUS_OF_VIEWPORT = 300.0

		# world-space units
		self.nearPlane = 1.0
		self.farPlane = 10000.0
		# threshold for preventing objects being too close
		self.PUSH_THRESHOLD=1.3
		self.viewportWidthInPixels = 10
		self.viewportHeightInPixels = 10
		self.viewportRadiusInPixels = 5

		self.sceneRadius = 10

		# point of view: the ego-center, the eye point
		self.position = Point()

		# point of interest
		self.target = Point()

		# up direction of camera
		self.up = Vector()
		# up direction of the ground
		self.ground = Vector(0.,1.,0.)
		self.reset()
	def reset(self):
		tangent = math.tan(self.FIELD_OF_VIEW_IN_DEGREES/2.0/180.0*math.pi)
		distanceFromTarget = self.sceneRadius/tangent
		self.position = Point(0,0,distanceFromTarget)
		self.target = Point(0,0,0)
		self.up = self.ground.copy()

	def setViewportDimensions(self,widthInpixels,heightInpixels):
		self.viewportWidthInPixels = widthInpixels
		self.viewportHeightInPixels = heightInpixels
		self.viewportRadiusInPixels = 0.5*widthInpixels if (widthInpixels<heightInpixels) else 0.5*heightInpixels

	def getViewportWidth(self):
		return self.viewportWidthInPixels
	def getViewportHeight(self):
		return self.viewportHeightInPixels
	def setSceneRadius(self,radius):
		self.sceneRadius = radius

	def transform(self):
		tangent = math.tan(self.FIELD_OF_VIEW_IN_DEGREES/2.0/180.0*math.pi)
		viewportRadius = self.nearPlane * tangent
		if self.viewportWidthInPixels < self.viewportHeightInPixels:
			viewportWidth = 2.0*viewportRadius 
			viewportHeight = viewportWidth*self.viewportHeightInPixels/float(self.viewportWidthInPixels)
		else:
			viewportHeight = 2.0*viewportRadius
			viewportWidth = viewportHeight*self.viewportWidthInPixels/float(self.viewportHeightInPixels)
		glFrustum(-0.5*viewportWidth,0.5*viewportWidth,-0.5*viewportHeight,0.5*viewportHeight,self.nearPlane,self.farPlane)

		M = Matrix4x4.lookAt(self.position,self.target,self.up,False)
		glMultMatrixf(M.get())

	# lal
	def orbit(self,old_x_pixels,old_y_pixels,new_x_pixels,new_y_pixels):
		pixelsPerDegree = self.viewportRadiusInPixels/float(self.ORBITING_SPEED_IN_DEGREES_PER_RADIUS_OF_VIEWPORT)
		radianPerPixel = 1.0/pixelsPerDegree*math.pi/180.0

		t2p = self.position-self.target

		M = Matrix4x4.rotationAroundOrigin((old_x_pixels-new_x_pixels)*radianPerPixel,self.ground)
		t2p = M*t2p
		self.up = M*self.up
		self.position = self.target + t2p

	def translateSceneRightAndUp(self,delta_x_pixels,delta_y_pixels):
		direction = self.target-self.position
		distanceFromTarget = direction.norm()
		direction = direction.normalized()
		translationSpeedInUnitsPerRadius = distanceFromTarget*math.tan(self.FIELD_OF_VIEW_IN_DEGREES/2.0/180.0*math.pi)
		pixelsPerUnit = self.viewportRadiusInPixels/translationSpeedInUnitsPerRadius

		right = direction^self.up
		translation = right*(-delta_x_pixels/pixelsPerUnit)+self.up*(-delta_y_pixels/pixelsPerUnit)

		self.position = self.position+translation
		self.target = self.target+translation


	def dollyCameraForward(self,delta_pixels,pushTarget):
		direction = self.target-self.position
		distanceFromTarget = direction.norm()
		direction = direction.normalized()

		translationSpeedInUnitsPerRadius = distanceFromTarget*math.tan(self.FIELD_OF_VIEW_IN_DEGREES/360.0*math.pi)
		pixelsPerUnit = self.viewportRadiusInPixels/translationSpeedInUnitsPerRadius

		dollyDistance = delta_pixels/pixelsPerUnit

		if not pushTarget:
			distanceFromTarget -= dollyDistance
			if distanceFromTarget < self.PUSH_THRESHOLD*self.nearPlane:
				distanceFromTarget = self.PUSH_THRESHOLD*self.nearPlane

		self.position += direction*dollyDistance
		self.target = self.position+direction*distanceFromTarget


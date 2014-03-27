#! /usr/bin/env python

from OpenGL.GL import *
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
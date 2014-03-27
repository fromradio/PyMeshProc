# gui for presenting mesh
#! /usr/bin/env python

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import sys
import hedge.py

class Viewer3DWidget(QtOpenGL.QGLWidget):
	def __init__(self,parent = None):
		super(Viewer3DWidget,self).__init__(parent)
		self.setMouseTracking(True)
		self.camera 

def main():
	pass

if __name__== '__main__':
	main()


# gui for presenting mesh
#! /usr/bin/env python

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from camera import *
import numpy as np
from math import cos,sin
from meshdraw import *

#from models import *
from ArcBall import *
import sys

PI2 = 2*np.pi


#test models

def Torus(MinorRadius,MajorRadius):
	# draw a torus with normals
	glBegin(GL_TRIANGLE_STRIP)
	for i in xrange(20):
		for j in xrange(-1,20):
			if j < 0:
				wrapFrac = (-j%20)/20.0
				wrapFrac *= -1.0
			else:
				wrapFrac = (j%20)/20.0
			phi = PI2*wrapFrac
			sinphi = sin(phi)
			cosphi = cos(phi)

			r = MajorRadius + MinorRadius*cosphi
			glNormal3f (sin(PI2*(i%20+wrapFrac)/20.0)*cosphi,sinphi,cos(PI2*(i%20+wrapFrac)/20.0)*cosphi)
			glVertex3f (sin(PI2*(i%20+wrapFrac)/20.0)*r,MinorRadius*sinphi,cos(PI2*(i%20+wrapFrac)/20.0)*r)
			glNormal3f (sin(PI2*(i+1%20+wrapFrac)/20.0)*cosphi, sinphi, cos(PI2*(i+1%20+wrapFrac)/20.0)*cosphi)
			glVertex3f (sin(PI2*(i+1%20+wrapFrac)/20.0)*r, MinorRadius*sinphi, cos(PI2*(i+1%20+wrapFrac)/20.0)*r)
	glEnd()													# // Done Torus
	return



class Viewer3DWidget(QtOpenGL.QGLWidget):
	def __init__(self,parent = None):
		super(Viewer3DWidget,self).__init__(parent)
		#self.initGL(self.width(),self.height())
		self.isPressed = False
		self.lastRot = Matrix3fT()
		self.thisRot = Matrix3fT()
		self.g_Transform = Matrix4fT()
		self.g_ArcBall = ArcBallT(640,480)
		self.oldx = self.oldy = 0
		self._mesh = Mesh()
		self._mesh.readFile("test_.obj")

	def initGL(self,width,height):
		"""
		# Enable smooth color
		glShadeModel(GL_SMOOTH)
		# to black
		glClearColor(0.0,0.0,0.0,0.5)
		# enable depty test
		glEnable(GL_DEPTH_TEST)
		# type of depth test
		glDepthFunc(GL_LEQUAL)
		# nice perspective calculation
		glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST)
		"""
		glClearColor(0.0,0.0,0.0,1.0)
		glClearDepth(1.0)
		glDepthFunc(GL_LEQUAL)
		glEnable(GL_DEPTH_TEST)
		glShadeModel(GL_FLAT)
		glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST)

		glEnable(GL_LIGHT0)
		glEnable(GL_LIGHTING)

		glEnable(GL_COLOR_MATERIAL)

	def paintGL(self):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		glLoadIdentity()
		glTranslatef(-1.5,0.0,-6.0);
		#print '1'
		glPushMatrix()
		glMultMatrixf(self.g_Transform)
		glColor3f(0.75,1.0,1.0)
		self.draw()
		#Torus(0.30,1.00)
		glPopMatrix()
		#print '2'
		glLoadIdentity()
		glTranslatef(1.5,0.0,-6.0)
		#print '3'
		glPushMatrix()
		glMultMatrixf(self.g_Transform)
		glColor3f(1.0,0.75,0.75)
		#gluSphere(g_quadratic,1.3,20,20)
		glPopMatrix()
		#print '2'
		glFlush()
		#self.swapBuffers()
		# glMatrixMode(GL_PROJECTION)
		# glLoadIdentity()
		# self.camera.transform()
		# glMatrixMode(GL_MODELVIEW)
		# glLoadIdentity()

		# glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		# glDepthFunc(GL_LEQUAL)
		# glEnable(GL_DEPTH_TEST)
		# glEnable(GL_CULL_FACE)
		# glFrontFace(GL_CCW)
		# glDisable(GL_LIGHTING)
		# glShadeModel(GL_FLAT)

		# glFlush()
	def draw(self):
		meshDrawPoints(self._mesh)

	def resizeGL(self,width,height):
		if height == 0:
			height = 1
		glViewport(0,0,width,height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45.0,float(width)/float(height),1,100.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		self.g_ArcBall.setBounds(width,height)
		#return
		#self.camera.setViewportDimensions(widthInPixels,heightInPixels)
		#glViewport(0,0,widthInPixels,heightInPixels)
	def mouseMoveEvent(self,mouseEvent):
		if mouseEvent.buttons() ==QtCore.Qt.LeftButton and self.isPressed:
			mouse_pt = Point2fT(mouseEvent.x(),mouseEvent.y())
			ThisQuat = self.g_ArcBall.drag(mouse_pt)
			self.thisRot = Matrix3fSetRotationFromQuat4f(ThisQuat)

			self.thisRot = Matrix3fMulMatrix3f(self.lastRot,self.thisRot)

			self.g_Transform = Matrix4fSetRotationFromMatrix3f(self.g_Transform,self.thisRot)
			self.update()
	def mousePressEvent(self,mouseEvent):
		if mouseEvent.buttons() == QtCore.Qt.LeftButton:
			self.isPressed = True
			mouse_pt = Point2fT(mouseEvent.x(),mouseEvent.y())
			self.g_ArcBall.click(mouse_pt)
	def mouseReleaseEvent(self,mouseEvent):
		print 'lala'
		print mouseEvent.buttons()
		if mouseEvent.button() == QtCore.Qt.LeftButton:
			self.isPressed = False
			self.lastRot = self.thisRot.copy()
			#self.update()
		elif mouseEvent.button() == QtCore.Qt.RightButton:
			self.lastRot = Matrix3fSetIdentity()
			self.thisRot = Matrix3fSetIdentity()
			self.g_Transform = Matrix4fSetRotationFromMatrix3f(self.g_Transform,self.thisRot)
			#self.update()
		self.update()

class PyQtGL(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.setWindowTitle('Python Qt OpenGL')
		self.statusBar().showMessage("Success")

		exitAction = QtGui.QAction("Exit",self)
		exitAction.setShortcut("Ctrl+Q")
		exitAction.setStatusTip("Exit")
		self.connect(exitAction,QtCore.SIGNAL('triggered()'),QtCore.SLOT('close()'))

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAction)

		self.setToolTip('This is a window')

		viewer3D = Viewer3DWidget(self)
		createButton = True
		if createButton:
			parentWidget = QtGui.QWidget()

			button1 = QtGui.QPushButton("Button1")
			button1.setStatusTip("do something")
			vbox = QtGui.QVBoxLayout()
			vbox.addWidget(button1)
			vbox.addStretch(1)
			viewer3D.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
			viewer3D.resize(640,480)
			hbox = QtGui.QHBoxLayout()
			hbox.addLayout(vbox)
			hbox.addWidget(viewer3D)

			parentWidget.setLayout(hbox)
			self.setCentralWidget(viewer3D)
	def closeEvent(self,event):
		reply = QtGui.QMessageBox.question(self,"Confirmation","Are you sure to quit?",QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,QtGui.QMessageBox.No)
		if reply == QtGui.QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()



def main():
	#qpp = QtGui.QApplication(['lala'])
	app = QtGui.QApplication(sys.argv)
	window = PyQtGL()
	window.show()
	print 'lolo'
	sys.exit(app.exec_())
	print 'lala'

if __name__== '__main__':
	main()


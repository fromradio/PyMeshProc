# gui for presenting mesh
#! /usr/bin/env python

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtOpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from camera import *
import sys

class Viewer3DWidget(QtOpenGL.QGLWidget):
	def __init__(self,parent = None):
		super(Viewer3DWidget,self).__init__(parent)
		self.setMouseTracking(True)
		self.camera = camera()
		self.camera.setSceneRadius(2)
		self.camera.reset()
		self.isPressed = False
		self.oldx = self.oldy = 0

	def paintGL(self):
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		self.camera.transform()
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

		glDepthFunc(GL_LEQUAL)
		glEnable(GL_DEPTH_TEST)
		glEnable(GL_CULL_FACE)
		glFrontFace(GL_CCW)
		glDisable(GL_LIGHTING)
		glShadeModel(GL_FLAT)

		glColor(1.0,1.0,1.0)
		glBegin(GL_LINE_STRIP)
		glVertex(-1,-1,-1)
		glVertex(1,-1,-1)
		glVertex(1,1,-1)
		glEnd()
		glColor(1.0,0.0,0.0)
		glBegin(GL_LINES)
		glVertex(0,0,0)
		glVertex(1,0,0)
		glEnd()

		glFlush()

	def resizeGL(self,widthInPixels,heightInPixels):
		self.camera.setViewportDimensions(widthInPixels,heightInPixels)
		glViewport(0,0,widthInPixels,heightInPixels)

	def initializeGL(self):
		glClearColor(0.,0.,0.,1.0)
		glClearDepth(1.0)


	def mouseMoveEvent(self,mouseEvent):
		if int(mouseEvent.buttons()) != QtCore.Qt.NoButton:
			# dragging
			delta_x = mouseEvent.x()-self.oldx
			delta_y = self.oldy - mouseEvent.y()
			if int(mouseEvent.buttons()) & QtCore.Qt.LeftButton:
				if int(mouseEvent.buttons()) & QtCore.Qt.MidButton:
					self.camera.dollyCameraForward(3*(delta_x+delta_y),False)
				else:
					self.camera.orbit(self.oldx,self.oldy,mouseEvent.x(),mouseEvent.y())
			elif int(mouseEvent.buttons()) & QtCore.Qt.MidButton:
				self.camera.translateSceneRightAndUp(delta_x,delta_y)
			self.update()
		self.oldx = mouseEvent.x()
		self.oldy = mouseEvent.y()
	def mouseDoubleClickEvent(self,mouseEvent):
		print 'double click'

	def mousePressEvent(self,mouseEvent):
		self.isPressed = True
	def mouseReleaseEvent(self,mouseEvent):
		self.isPressed = False

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
			hbox = QtGui.QHBoxLayout()
			hbox.addLayout(vbox)
			hbox.addWidget(viewer3D)

			parentWidget.setLayout(hbox)
			self.setCentralWidget(viewer3D)

		self.resize(500,500)
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
	sys.exit(app.exec_())

if __name__== '__main__':
	main()


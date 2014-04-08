# author: Ruimin Wang (ruimin.wang13@gmail.com)

from hedge import *
from OpenGL.GL import *
from OpenGL.GLU import *

def meshDrawPoints(mesh):
	glBegin(GL_POINTS)
	for vert in mesh.vertices():
		pt = vert.point
		glVertex3f(pt.x,pt.y,pt.z)
	glEnd()
def meshDrawTriangle(mesh):
	pass
def meshDrawSmoothWithoutNormal(mesh):
	pass


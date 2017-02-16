from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from HShaderProgram import HPlainPolygonProgram2D

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

gPlainPolygonProgram2D = HPlainPolygonProgram2D()

def initGL():
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0., SCREEN_WIDTH, 0., SCREEN_HEIGHT, 1., -1.)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0., 0., 0., 1.)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glDisable(GL_DEPTH_TEST)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    error = glGetError()
    if error != GL_NO_ERROR:
        print('Error initializing OpenGL')
        return False
    return True
    
def loadGP():
    global gPlainPolygonProgram2D
    if not gPlainPolygonProgram2D.loadProgram():
        print('Unable to load basic shader!')
        return False
        
    gPlainPolygonProgram2D.bind()
    return True
    
def loadMedia():
    return True
    
def update():
    pass
    
def render():
    glClear( GL_COLOR_BUFFER_BIT )
    glLoadIdentity()

    # Solid cyan quad in the center
    glTranslatef( SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0. )
    glBegin( GL_QUADS )
    glColor3f( 0., 1., 1. )
    glVertex2f( -50., -50. )
    glVertex2f(  50., -50. )
    glVertex2f(  50.,  50. )
    glVertex2f( -50.,  50. )
    glEnd()

    glutSwapBuffers()
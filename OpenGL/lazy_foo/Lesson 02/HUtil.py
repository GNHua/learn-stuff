from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

COLOR_MODE_CYAN = 0
COLOR_MODE_MULTI = 1

gColorMode = COLOR_MODE_CYAN
gProjectionScale = 1.

def initGL():    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0., SCREEN_WIDTH, SCREEN_HEIGHT, 0., 1., -1.)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(1., 0., 0., 1.)

    error = glGetError()
    if error != GL_NO_ERROR:
        print('Error initializing OpenGL! %s' % gluErrorString(error))
        return False
    return True

def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    
    # glTranslatef( SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0. )
    glTranslatef( SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0. )
    
    if gColorMode == COLOR_MODE_CYAN:
        glBegin( GL_QUADS )
        # glColor3f( 0., 1., 1. )
        glVertex2f( -50., -50. )
        glVertex2f(  50., -50. )
        glVertex2f(  50.,  50. )
        glVertex2f( -50.,  50. )
        glEnd()
    else:
        glBegin( GL_QUADS )
        glColor3f( 1., 0., 0. ); glVertex2f( -50., -50. );
        glColor3f( 1., 1., 0. ); glVertex2f(  50., -50. );
        glColor3f( 0., 1., 0. ); glVertex2f(  50.,  50. );
        glColor3f( 0., 0., 1. ); glVertex2f( -50.,  50. );
        glEnd()

    glutSwapBuffers()
    
def handleKeys(key, x, y):
    global gColorMode
    global gProjectionScale
    if key == b'q':
        if gColorMode == COLOR_MODE_CYAN:
            gColorMode = COLOR_MODE_MULTI
        else:
            gColorMode = COLOR_MODE_CYAN
    elif key == b'e':
        if gProjectionScale == 1.:
            gProjectionScale = 2.
        elif gProjectionScale == 2.:
            gProjectionScale = 0.5
        elif gProjectionScale == 0.5:
            gProjectionScale = 1.
            
        glMatrixMode( GL_PROJECTION )
        glLoadIdentity()
        glOrtho( 0.0, SCREEN_WIDTH * gProjectionScale, SCREEN_HEIGHT * gProjectionScale, 0., 1.0, -1.0 )
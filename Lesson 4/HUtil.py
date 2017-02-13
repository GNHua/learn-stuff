from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

gCameraX, gCameraY = 0., 0.

def initGL():
    glViewport( 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT )
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0., SCREEN_WIDTH, SCREEN_HEIGHT, 0., 1., -1.)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    glClearColor(0., 0., 0., 1.)

    error = glGetError()
    if error != GL_NO_ERROR:
        print('Error initializing OpenGL! %s' % gluErrorString(error))
        return False
    return True

def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    
    glPushMatrix()
    
    glTranslatef( SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0. )
    
    # Red quad
    glBegin( GL_QUADS );
    glColor3f( 1., 0., 0. );
    glVertex2f( -SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
    glVertex2f(  SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
    glVertex2f(  SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
    glVertex2f( -SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
    glEnd();

    # Move to the right of the screen
    glTranslatef( SCREEN_WIDTH, 0., 0. );

    # Green quad
    glBegin( GL_QUADS );
    glColor3f( 0., 1., 0. );
    glVertex2f( -SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
    glVertex2f(  SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
    glVertex2f(  SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
    glVertex2f( -SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
    glEnd();

    # Move to the lower right of the screen
    glTranslatef( 0., SCREEN_HEIGHT, 0. );

    # Blue quad
    glBegin( GL_QUADS );
    glColor3f( 0., 0., 1. );
    glVertex2f( -SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
    glVertex2f(  SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
    glVertex2f(  SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
    glVertex2f( -SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
    glEnd();

    # Move below the screen
    glTranslatef( -SCREEN_WIDTH, 0., 0. );

    # Yellow quad
    glBegin( GL_QUADS );
    glColor3f( 1., 1., 0. );
    glVertex2f( -SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
    glVertex2f(  SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
    glVertex2f(  SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
    glVertex2f( -SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
    glEnd();
    
    glPopMatrix()

    glutSwapBuffers()
    
def handleKeys(key, x, y):
    global gCameraX
    global gCameraY
    
    if key == b'w':
        gCameraY -= 16
    elif key == b's':
        gCameraY += 16
    elif key == b'a':
        gCameraX -= 16
    elif key == b'd':
        gCameraX += 16
        
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    glTranslatef( -gCameraX, -gCameraY, 0. )
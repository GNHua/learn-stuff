from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from enum import IntEnum

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

class ViewportMode(IntEnum):
    FULL = 1
    HALF_CENTER = 2
    HALF_TOP = 3
    QUAD = 4
    RADAR = 5

gViewportMode = ViewportMode.FULL

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
    
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    
    glTranslatef( SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0. )
    
    global gViewportMode
    # Full View
    if gViewportMode == ViewportMode.FULL:
        # Fill the screen
        glViewport( 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT );

        # Red quad
        glBegin( GL_QUADS );
        glColor3f( 1., 0., 0. );
        glVertex2f( -SCREEN_WIDTH / 2., -SCREEN_HEIGHT / 2. );
        glVertex2f(  SCREEN_WIDTH / 2., -SCREEN_HEIGHT / 2. );
        glVertex2f(  SCREEN_WIDTH / 2.,  SCREEN_HEIGHT / 2. );
        glVertex2f( -SCREEN_WIDTH / 2.,  SCREEN_HEIGHT / 2. );
        glEnd();
    # View port at center of screen
    elif gViewportMode == ViewportMode.HALF_CENTER:
        # Center viewport
        glViewport( SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 );

        # Green quad
        glBegin( GL_QUADS );
        glColor3f( 0., 1., 0. );
        glVertex2f( -SCREEN_WIDTH / 2., -SCREEN_HEIGHT / 2. );
        glVertex2f(  SCREEN_WIDTH / 2., -SCREEN_HEIGHT / 2. );
        glVertex2f(  SCREEN_WIDTH / 2.,  SCREEN_HEIGHT / 2. );
        glVertex2f( -SCREEN_WIDTH / 2.,  SCREEN_HEIGHT / 2. );
        glEnd();
    # Viewport centered at the top
    elif gViewportMode == ViewportMode.HALF_TOP:
        # Viewport at top
        glViewport( SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 );

        # Blue quad
        glBegin( GL_QUADS );
        glColor3f( 0., 0., 1. );
        glVertex2f( -SCREEN_WIDTH / 2., -SCREEN_HEIGHT / 2. );
        glVertex2f(  SCREEN_WIDTH / 2., -SCREEN_HEIGHT / 2. );
        glVertex2f(  SCREEN_WIDTH / 2.,  SCREEN_HEIGHT / 2. );
        glVertex2f( -SCREEN_WIDTH / 2.,  SCREEN_HEIGHT / 2. );
        glEnd();
    # Four viewports
    elif gViewportMode == ViewportMode.QUAD:
        # Bottom left red quad
        glViewport( 0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 );
        glBegin( GL_QUADS );
        glColor3f( 1., 0., 0. );
        glVertex2f( -SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
        glVertex2f(  SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
        glVertex2f(  SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
        glVertex2f( -SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
        glEnd();

        # Bottom right green quad
        glViewport( SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 );
        glBegin( GL_QUADS );
        glColor3f( 0., 1., 0. );
        glVertex2f( -SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
        glVertex2f(  SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
        glVertex2f(  SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
        glVertex2f( -SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
        glEnd();

        # Top left blue quad
        glViewport( 0, SCREEN_HEIGHT //2 , SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 );
        glBegin( GL_QUADS );
        glColor3f( 0., 0., 1. );
        glVertex2f( -SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
        glVertex2f(  SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
        glVertex2f(  SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
        glVertex2f( -SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
        glEnd();

        # Top right yellow quad
        glViewport( SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 );
        glBegin( GL_QUADS );
        glColor3f( 1., 1., 0. );
        glVertex2f( -SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
        glVertex2f(  SCREEN_WIDTH / 4., -SCREEN_HEIGHT / 4. );
        glVertex2f(  SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
        glVertex2f( -SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
        glEnd();
    # Viewport with radar subview port
    elif gViewportMode == ViewportMode.RADAR:
        # Full size quad
        glViewport( 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT );
        glBegin( GL_QUADS );
        glColor3f( 1., 1., 1. );
        glVertex2f( -SCREEN_WIDTH / 8., -SCREEN_HEIGHT / 8. );
        glVertex2f(  SCREEN_WIDTH / 8., -SCREEN_HEIGHT / 8. );
        glVertex2f(  SCREEN_WIDTH / 8.,  SCREEN_HEIGHT / 8. );
        glVertex2f( -SCREEN_WIDTH / 8.,  SCREEN_HEIGHT / 8. );
        glColor3f( 0., 0., 0. );
        glVertex2f( -SCREEN_WIDTH / 16., -SCREEN_HEIGHT / 16. );
        glVertex2f(  SCREEN_WIDTH / 16., -SCREEN_HEIGHT / 16. );
        glVertex2f(  SCREEN_WIDTH / 16.,  SCREEN_HEIGHT / 16. );
        glVertex2f( -SCREEN_WIDTH / 16.,  SCREEN_HEIGHT / 16. );
        glEnd();

        # Radar quad
        glViewport( SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 );
        glBegin( GL_QUADS );
        glColor3f( 1., 1., 1. );
        glVertex2f( -SCREEN_WIDTH / 8., -SCREEN_HEIGHT / 8. );
        glVertex2f(  SCREEN_WIDTH / 8., -SCREEN_HEIGHT / 8. );
        glVertex2f(  SCREEN_WIDTH / 8.,  SCREEN_HEIGHT / 8. );
        glVertex2f( -SCREEN_WIDTH / 8.,  SCREEN_HEIGHT / 8. );
        glColor3f( 0., 0., 0. );
        glVertex2f( -SCREEN_WIDTH / 16., -SCREEN_HEIGHT / 16. );
        glVertex2f(  SCREEN_WIDTH / 16., -SCREEN_HEIGHT / 16. );
        glVertex2f(  SCREEN_WIDTH / 16.,  SCREEN_HEIGHT / 16. );
        glVertex2f( -SCREEN_WIDTH / 16.,  SCREEN_HEIGHT / 16. );
        glEnd();

    glutSwapBuffers()
    
def handleKeys(key, x, y):
    global gViewportMode
    if key == b'q':
        gViewportMode += 1
        if gViewportMode > ViewportMode.RADAR:
            gViewportMode = ViewportMode.FULL
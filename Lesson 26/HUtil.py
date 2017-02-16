from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from PIL import Image
from HTexture import HTexture

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

gTexture = HTexture()

# Polygon attributes
gPolygonAngle = 0.
gPolygonX, gPolygonY = SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2.

# Stencil operation
gStencilRenderOp = GL_NOTEQUAL

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
    
    # Initialize stencil clear value
    glClearStencil( 0 )
    
    error = glGetError()
    if error != GL_NO_ERROR:
        print('Error initializing OpenGL')
        return False
    return True
    
def loadMedia():
    if not gTexture.loadTextureFromFile( "opengl.png" ):
        print( "Unable to load texture!\n" )
        return False
    return True
    
def update():
    global gPolygonAngle
    gPolygonAngle += 6.
    
def render():
    glClear( GL_COLOR_BUFFER_BIT | GL_STENCIL_BUFFER_BIT )
    glLoadIdentity()

    # Disable rendering to the color buffer
    glColorMask( GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE )

    # Start using the stencil
    glEnable( GL_STENCIL_TEST )

    # Place a 1 where rendered
    glStencilFunc( GL_ALWAYS, 1, 1 )

    # Replace where rendered
    glStencilOp( GL_REPLACE, GL_REPLACE, GL_REPLACE )
    
    global gPolygonX
    global gPolygonY
    global gPolygonAngle
    # Render stencil triangle
    glTranslatef( gPolygonX, gPolygonY, 0. );
    glRotatef( gPolygonAngle, 0., 0., 1. );
    glBegin( GL_TRIANGLES );
    glVertex2f(            -0. / 4., -SCREEN_HEIGHT / 4. );
    glVertex2f(   SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
    glVertex2f(  -SCREEN_WIDTH / 4.,  SCREEN_HEIGHT / 4. );
    glEnd();

    # Reenable color
    glColorMask( GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE );

    global gStencilRenderOp
    # Where a 1 was not rendered
    glStencilFunc( gStencilRenderOp, 1, 1 );

    # Keep the pixel
    glStencilOp( GL_KEEP, GL_KEEP, GL_KEEP );

    # Render stenciled texture
    glLoadIdentity();
    gTexture.render( ( SCREEN_WIDTH - 520 ) / 2., ( SCREEN_HEIGHT - 235 ) / 2. );

    # Finished using stencil
    glDisable( GL_STENCIL_TEST );

    glutSwapBuffers()
    
def handleKeys(key, x, y):
    global gStencilRenderOp
    # If the user presses q
    if key == b'q':
        # Cycle through stencil operations
        if gStencilRenderOp == GL_NOTEQUAL:
            # Render where stencil polygon was rendered
            gStencilRenderOp = GL_EQUAL;
        elif gStencilRenderOp == GL_EQUAL:
            # Render everything
            gStencilRenderOp = GL_ALWAYS;
        elif gStencilRenderOp == GL_ALWAYS:
            # Render where stencil polygon was not rendered
            gStencilRenderOp = GL_NOTEQUAL;
            
def handleMouseMotion(x, y):
    global gPolygonX
    global gPolygonY
    # Set polygon position
    gPolygonX = x;
    gPolygonY = y;
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from HTexture import HFRect, HTexture
import numpy as np

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30
gArrowTexture = HTexture()
gArrowClips = []
for i in range(4):
    gArrowClips.append(HFRect())

def initGL():
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0., SCREEN_WIDTH, 0., SCREEN_HEIGHT, 1., -1.)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0., 0., 0., 1.)
    glEnable(GL_TEXTURE_2D)
    
    error = glGetError()
    if error != GL_NO_ERROR:
        print('Error initializing OpenGL')
        return False
    return True
    
def loadMedia():
    gArrowClips[ 0 ].x = 0.
    gArrowClips[ 0 ].y = 0.
    gArrowClips[ 0 ].w = 128.
    gArrowClips[ 0 ].h = 128.

    gArrowClips[ 1 ].x = 128.
    gArrowClips[ 1 ].y = 0.
    gArrowClips[ 1 ].w = 128.
    gArrowClips[ 1 ].h = 128.

    gArrowClips[ 2 ].x = 0.
    gArrowClips[ 2 ].y = 128.
    gArrowClips[ 2 ].w = 128.
    gArrowClips[ 2 ].h = 128.

    gArrowClips[ 3 ].x = 128.
    gArrowClips[ 3 ].y = 128.
    gArrowClips[ 3 ].w = 128.
    gArrowClips[ 3 ].h = 128.
    
    if not gArrowTexture.loadTextureFromFile(imageName='arrows.png'):
        print('Unable to load arrow texture!')
        return False
    return True
    
def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    gArrowTexture.render( 0., 0., clip=gArrowClips[ 0 ] )
    gArrowTexture.render( SCREEN_WIDTH - gArrowClips[ 1 ].w, 0., clip=gArrowClips[ 1 ])
    gArrowTexture.render( 0., SCREEN_HEIGHT - gArrowClips[ 2 ].h, clip=gArrowClips[ 2 ] )
    gArrowTexture.render( SCREEN_WIDTH - gArrowClips[ 3 ].w, SCREEN_HEIGHT - gArrowClips[ 3 ].h, clip=gArrowClips[ 3 ] )
    glutSwapBuffers()
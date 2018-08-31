from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from HTexture import HTexture
import numpy as np

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30
gCircleTexture = HTexture()

def initGL():
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0., SCREEN_WIDTH, SCREEN_HEIGHT, 0., 1., -1.)
    
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
    
def loadMedia():
    if not gCircleTexture.loadTextureFromFileWithColorKey(imName='circle.png', rgba=b'\x00\xFF\xFF\xFF'):
        print('Unable to load circle texture!')
        return False
    return True
    
def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor4f( 1., 1., 1., 0.5 )
    x = (SCREEN_WIDTH - gCircleTexture.mImageWidth)/2
    y = (SCREEN_HEIGHT - gCircleTexture.mImageHeight)/2
    gCircleTexture.render(x, y)
    glutSwapBuffers()
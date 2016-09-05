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
    
    error = glGetError()
    if error != GL_NO_ERROR:
        print('Error initializing OpenGL')
        return False
    return True
    
def loadMedia():
    if not gCircleTexture.loadTextureFromFile(imageName='circle.png'):
        print('Unable to load non-power-of-two texture!')
        return False
        
    gCircleTexture.lock()
    targetColor = b'\x00\xFF\xFF\xFF'
    gCircleTexture.mPixels[ gCircleTexture.mPixels == targetColor ] = b'\x00\x00\x00\x00'
    gMask = np.fromfunction(lambda x, y: x%10 != y%10, \
        (gCircleTexture.mTextureHeight, gCircleTexture.mTextureWidth))
    gCircleTexture.mPixels[ gMask ] = b'\x00\x00\x00\x00'
    gCircleTexture.unlock()
    return True
    
def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    x = (SCREEN_WIDTH - gCircleTexture.mImageWidth)/2
    y = (SCREEN_HEIGHT - gCircleTexture.mImageHeight)/2
    gCircleTexture.render(x, y)
    glutSwapBuffers()
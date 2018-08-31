from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from HTexture import HFRect, HTexture
import numpy as np

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30
gRotatingTexture = HTexture()
gAngle = 0.

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
    
def loadMedia():
    if not gRotatingTexture.loadTextureFromFile('arrow.png'):
        print('Unable to load arrow texture!')
        return False
    return True
    
def update():
    global gAngle
    gAngle += 360 / SCREEN_FPS
    if gAngle > 360:
        gAngle -= 360
    
def render():
    global gAngle
    glClear(GL_COLOR_BUFFER_BIT)
    x = (SCREEN_WIDTH - gRotatingTexture.mImageWidth)/2
    y = (SCREEN_HEIGHT - gRotatingTexture.mImageHeight)/2
    gRotatingTexture.render(x, y, degrees = gAngle)
    glutSwapBuffers()
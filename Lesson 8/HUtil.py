from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from HTexture import HTexture
import numpy as np

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30
gNon2NTexture = HTexture()

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
    if not gNon2NTexture.loadTextureFromFile(imageName='opengl.png'):
        print('Unable to load non-power-of-two texture!')
        return False
    return True
    
def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    x = (SCREEN_WIDTH - gNon2NTexture.mImageWidth)/2
    y = (SCREEN_HEIGHT - gNon2NTexture.mImageHeight)/2
    gNon2NTexture.render(x, y)
    glutSwapBuffers()
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from HTexture import HTexture

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

gVBOTexture = HTexture()

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
    if not gVBOTexture.loadTextureFromFile("opengl.png"):
        print('Unable to load OpenGL texture!')
        return False
    return True
    
def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    x = (SCREEN_WIDTH - gVBOTexture.mImageWidth)/2
    y = (SCREEN_HEIGHT - gVBOTexture.mImageHeight)/2
    gVBOTexture.render(x, y)
    glutSwapBuffers()
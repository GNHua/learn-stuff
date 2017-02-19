from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from HTexture import HFRect, HTexture
import numpy as np

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30
gStretchedTexture = HTexture()
gStretchRect = HFRect(0., 0., SCREEN_WIDTH, SCREEN_HEIGHT)
gFiltering = GL_LINEAR

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
    if not gStretchedTexture.loadTextureFromFile('mini_opengl.png'):
        print('Unable to load mini texture!')
        return False
    return True
    
def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    gStretchedTexture.render(0., 0., stretch = gStretchRect)
    glutSwapBuffers()
    
def handleKeys(key, x, y):
    global gFiltering
    if key == b'q':
        glBindTexture( GL_TEXTURE_2D, gStretchedTexture.mTextureID )
        if gFiltering != GL_LINEAR:
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR )
            gFiltering = GL_LINEAR
        else:
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
            glTexParameteri( GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST )
            gFiltering = GL_NEAREST
        glBindTexture( GL_TEXTURE_2D, 0 )

























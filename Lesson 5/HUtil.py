from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from HTexture import HTexture
import numpy as np

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30
gCheckerBoardTexture = HTexture()

def initGL():
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0., SCREEN_WIDTH, SCREEN_HEIGHT, 0., 1., -1.)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0., 0., 0., 1.)
    
    ###
    glEnable(GL_TEXTURE_2D)
    
    error = glGetError()
    if error != GL_NO_ERROR:
        print('Error initializing OpenGL')
        return False
    return True
    
def loadMedia():
    CHECKERBOARD_WIDTH = 128
    CHECKERBOARD_HEIGHT = 128
    checkerBoard = np.zeros((CHECKERBOARD_HEIGHT, CHECKERBOARD_WIDTH), dtype=np.uint32)
    color1 = 0xFFFFFFFF
    color2 = 0xFF0000FF
    c = np.fromfunction(lambda x, y: (x//16 + y//16)%2, (CHECKERBOARD_HEIGHT, CHECKERBOARD_WIDTH), dtype=np.uint8)
    checkerBoard[c == 0] = color1
    checkerBoard[c == 1] = color2
    
    if not gCheckerBoardTexture.loadTextureFromPixels32(checkerBoard.tostring(), CHECKERBOARD_WIDTH, CHECKERBOARD_HEIGHT):
        print('Unable to load checkerboard texture!')
        return False
    return True
    
def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    x = (SCREEN_WIDTH - gCheckerBoardTexture.mTextureWidth)/2
    y = (SCREEN_HEIGHT - gCheckerBoardTexture.mTextureHeight)/2
    gCheckerBoardTexture.render(x, y)
    glutSwapBuffers()
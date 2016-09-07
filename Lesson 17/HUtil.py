from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

gQuadVertices = np.zeros((4, 2), dtype=GLfloat)
gIndices = np.zeros(4, dtype=GLuint)
gVertexBuffer = 0
gIndexBuffer = 0

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
    gQuadVertices[ 0, 0 ] = SCREEN_WIDTH * 1. / 4.
    gQuadVertices[ 0, 1 ] = SCREEN_HEIGHT * 1. / 4.

    gQuadVertices[ 1, 0 ] = SCREEN_WIDTH * 3. / 4.
    gQuadVertices[ 1, 1 ] = SCREEN_HEIGHT * 1. / 4.

    gQuadVertices[ 2, 0 ] = SCREEN_WIDTH * 3. / 4.
    gQuadVertices[ 2, 1 ] = SCREEN_HEIGHT * 3. / 4.

    gQuadVertices[ 3, 0 ] = SCREEN_WIDTH * 1. / 4.
    gQuadVertices[ 3, 1 ] = SCREEN_HEIGHT * 3. / 4.
    
    gIndices[ 0 ] = 0
    gIndices[ 1 ] = 1
    gIndices[ 2 ] = 2
    gIndices[ 3 ] = 3
    
    global gVertexBuffer
    gVertexBuffer = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, gVertexBuffer)
    glBufferData(GL_ARRAY_BUFFER, gQuadVertices.nbytes, \
        gQuadVertices.tostring(), GL_STATIC_DRAW)
    
    global gIndexBuffer
    gIndexBuffer = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gIndexBuffer)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, gIndices.nbytes, \
        gIndices.tostring(), GL_STATIC_DRAW)
    
    return True
    
def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glEnableClientState(GL_VERTEX_ARRAY)
    
    global gVertexBuffer
    glBindBuffer(GL_ARRAY_BUFFER, gVertexBuffer)
    glVertexPointer(2, GL_FLOAT, 0, None)
    
    global gIndexBuffer
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, gIndexBuffer)
    glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, None)
    
    glDisableClientState(GL_VERTEX_ARRAY)
    glutSwapBuffers()
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from OpenGL.arrays import vbo

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

gQuadVertices = np.zeros((4, 2), dtype=GLfloat)
gIndices = np.zeros(4, dtype=GLuint)
gVertexBuffer = 0
gIndexBuffer = 0

gVBO = vbo.VBO(data=gQuadVertices.tostring(), usage='GL_STATIC_DRAW', target='GL_ARRAY_BUFFER')
gIBO = vbo.VBO(data=gIndices.tostring(), usage='GL_STATIC_DRAW', target='GL_ELEMENT_ARRAY_BUFFER')

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
        
    gVBO.bind()
    gVBO.set_array(data=gQuadVertices.tostring())
    gVBO.copy_data()
    
    gIBO.bind()
    gIBO.set_array(data=gIndices.tostring())
    gIBO.copy_data()
    
    return True
    
def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glEnableClientState(GL_VERTEX_ARRAY)
    
    gVBO.bind()
    glVertexPointer(2, GL_FLOAT, 0, None)
    gIBO.bind()
    glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, None)
    
    glDisableClientState(GL_VERTEX_ARRAY)
    glutSwapBuffers()
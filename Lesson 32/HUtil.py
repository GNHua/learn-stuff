from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy as np
from HShaderProgram import HPlainPolygonProgram2D
from HStruct import HVertexPos2D
import matrix as m

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

gPlainPolygonProgram2D = HPlainPolygonProgram2D()

gVBO = None
gIBO = None

def initGL():
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
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
    
def loadGP():
    global gPlainPolygonProgram2D
    if not gPlainPolygonProgram2D.loadProgram():
        print('Unable to load basic shader!')
        return False
        
    gPlainPolygonProgram2D.bind()
    gPlainPolygonProgram2D.setProjection(m.make_ortho_matrix([0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 1, -1]))
    gPlainPolygonProgram2D.updateProjection()
    gPlainPolygonProgram2D.setModelView(np.identity(4, dtype=GLfloat))
    gPlainPolygonProgram2D.updateModelView()
    return True
    
def loadMedia():
    quadVertices = []
    for i in range(4):
        quadVertices.append(HVertexPos2D())
        
    quadVertices[ 0 ].x = -50.
    quadVertices[ 0 ].y = -50.

    quadVertices[ 1 ].x =  50.
    quadVertices[ 1 ].y = -50.

    quadVertices[ 2 ].x =  50.
    quadVertices[ 2 ].y =  50.

    quadVertices[ 3 ].x = -50.
    quadVertices[ 3 ].y =  50.
    
    indices = np.arange(4, dtype=GLuint)
        
    global gVBO
    global gIBO
    quadVerticesBytes = quadVertices[0] + quadVertices[1] + quadVertices[2] + quadVertices[3]
    gVBO = vbo.VBO(data=quadVerticesBytes, usage='GL_STATIC_DRAW', target='GL_ARRAY_BUFFER')
    gVBO.bind()
    gVBO.copy_data()
    gIBO = vbo.VBO(data=indices.tostring(), usage='GL_STATIC_DRAW', target='GL_ELEMENT_ARRAY_BUFFER')
    gIBO.bind()
    gIBO.copy_data()
    
    return True
    
def update():
    pass
    
def render():
    glClear( GL_COLOR_BUFFER_BIT )

    global gPlainPolygonProgram2D
    gPlainPolygonProgram2D.setModelView(m.make_translate_matrix([SCREEN_WIDTH/2., SCREEN_HEIGHT/2., 0]))
    gPlainPolygonProgram2D.updateModelView()
    gPlainPolygonProgram2D.setColor(0., 1., 1., 1.)
    
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(2, GL_FLOAT, 0, None)
    glDrawElements(GL_QUADS, 4, GL_UNSIGNED_INT, None)
    glDisableClientState(GL_VERTEX_ARRAY)
    
    glutSwapBuffers()
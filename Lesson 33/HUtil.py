from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy as np
from HShaderProgram import HMultiColorPolygonProgram2D
from HStruct import HMultiColorVertex2D
import matrix as m

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

gMultiColorPolygonProgram2D = HMultiColorPolygonProgram2D()

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
    global gMultiColorPolygonProgram2D
    if not gMultiColorPolygonProgram2D.loadProgram():
        print('Unable to load basic shader!')
        return False
        
    gMultiColorPolygonProgram2D.bind()
    gMultiColorPolygonProgram2D.setProjection(m.make_ortho_matrix([0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 1, -1]))
    gMultiColorPolygonProgram2D.updateProjection()
    gMultiColorPolygonProgram2D.setModelView(np.identity(4, dtype=GLfloat))
    gMultiColorPolygonProgram2D.updateModelView()
    return True
    
def loadMedia():
    quadVertices = []
    for i in range(4):
        quadVertices.append(HMultiColorVertex2D())
        
    quadVertices[ 0 ].pos.x = -50.
    quadVertices[ 0 ].pos.y = -50.
    quadVertices[ 0 ].rgba.r = 1.
    quadVertices[ 0 ].rgba.g = 0.
    quadVertices[ 0 ].rgba.b = 0.
    quadVertices[ 0 ].rgba.a = 1.

    quadVertices[ 1 ].pos.x =  50.
    quadVertices[ 1 ].pos.y = -50.
    quadVertices[ 1 ].rgba.r = 1.
    quadVertices[ 1 ].rgba.g = 1.
    quadVertices[ 1 ].rgba.b = 0.
    quadVertices[ 1 ].rgba.a = 1.

    quadVertices[ 2 ].pos.x =  50.
    quadVertices[ 2 ].pos.y =  50.
    quadVertices[ 2 ].rgba.r = 0.
    quadVertices[ 2 ].rgba.g = 1.
    quadVertices[ 2 ].rgba.b = 0.
    quadVertices[ 2 ].rgba.a = 1.

    quadVertices[ 3 ].pos.x = -50.
    quadVertices[ 3 ].pos.y =  50.
    quadVertices[ 3 ].rgba.r = 0.
    quadVertices[ 3 ].rgba.g = 0.
    quadVertices[ 3 ].rgba.b = 1.
    quadVertices[ 3 ].rgba.a = 1.
    
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

    global gMultiColorPolygonProgram2D
    gMultiColorPolygonProgram2D.setModelView(m.make_translate_matrix([SCREEN_WIDTH/2., SCREEN_HEIGHT/2., 0]))
    gMultiColorPolygonProgram2D.updateModelView()

    gMultiColorPolygonProgram2D.enableVertexPointer();
    gMultiColorPolygonProgram2D.enableColorPointer();
    
    global gVBO
    global gIBO
    gMultiColorPolygonProgram2D.setVertexPointer(HMultiColorVertex2D.size, gVBO+HMultiColorVertex2D.posOffset)
    gMultiColorPolygonProgram2D.setColorPointer(HMultiColorVertex2D.size, gVBO+HMultiColorVertex2D.colorOffset);
    glDrawElements(GL_TRIANGLE_FAN, 4, GL_UNSIGNED_INT, None)
    gMultiColorPolygonProgram2D.disableVertexPointer()
    gMultiColorPolygonProgram2D.disableColorPointer()
    glutSwapBuffers()
import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

__all__ = ['initGlfw', 
           'makeVBO', 
           'makeEBO', 
           'makeShaderProg', 
           'bindVAO', 
           'bindTexture']

def initGlfw():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    # The following 2 lines are CRUCIAL to get this work on Mac.
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
    
def makeVBO(vertices):
    VBO = vbo.VBO(data=vertices.tostring(), usage='GL_STATIC_DRAW', target='GL_ARRAY_BUFFER')
    VBO.bind()
    VBO.copy_data()
    return VBO
    
def makeEBO(indices):
    EBO = vbo.VBO(data=indices.tostring(), usage='GL_STATIC_DRAW', target='GL_ELEMENT_ARRAY_BUFFER')
    EBO.bind()
    EBO.copy_data()
    return EBO
    
def makeShaderProg(vert, frag, **kwargs):
    with open(vert, 'r') as f:
        vertShaderSource = f.read()
    vertShader = shaders.compileShader(vertShaderSource, GL_VERTEX_SHADER)
    with open(frag, 'r') as f:
        fragShaderSource = f.read()
    fragShader = shaders.compileShader(fragShaderSource, GL_FRAGMENT_SHADER)
    shaderProg = shaders.compileProgram(vertShader, fragShader, **kwargs)
    return shaderProg
    
class bindVAO:
    def __init__(self, vao):
        self.vao = vao
    def __enter__(self):
        glBindVertexArray(self.vao)
    def __exit__(self, type, value, traceback):
        glBindVertexArray(0)
        
class bindTexture:
    def __init__(self, target, texture):
        self.target = target
        self.texture = texture
    def __enter__(self):
        glBindTexture(self.target, self.texture)
    def __exit__(self, type, value, traceback):
        glBindTexture(self.target, 0)
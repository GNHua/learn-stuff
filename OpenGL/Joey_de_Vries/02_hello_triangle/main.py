import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
import numpy as np

WIDTH = 800
HEIGHT = 600

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
    
def makeShaderProg(vert, frag):
    vertShaderSource = open(vert, 'r').read()
    vertShader = shaders.compileShader(vertShaderSource, GL_VERTEX_SHADER)
    fragShaderSource = open(frag, 'r').read()
    fragShader = shaders.compileShader(fragShaderSource, GL_FRAGMENT_SHADER)
    shaderProg = shaders.compileProgram(vertShader, fragShader, validate=False)
    return shaderProg
    
class Triangles:
    def __init__(self):
        self.prepareWindow()
        
        self.vertices = np.array([[ 0.5,  0.5, 0.],
                                  [ 0.5, -0.5, 0.],
                                  [-0.5, -0.5, 0.],
                                  [-0.5,  0.5, 0.]], dtype=GLfloat)
        self.indices1 = np.array([1, 2, 3], dtype=GLuint)
        self.indices2 = np.array([0, 1, 2], dtype=GLuint)
        self.loadSP()
    
    def prepareWindow(self):
        self.window = glfw.create_window(WIDTH, HEIGHT, "LearnOpenGL", None, None)
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, key_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
    
        width, height = glfw.get_framebuffer_size(self.window)
        glViewport(0, 0, width, height)
        glClearColor(0.2, 0.3, 0.3, 1.)
        
    def loadSP(self):
        self.shaderProg = makeShaderProg('triangle.vert', 'triangle.frag')
        self._VAO1, self._VAO2 = glGenVertexArrays(2)
        
        glBindVertexArray(self._VAO1)
        _VBO = makeVBO(self.vertices)
        vertex_location = 0 # input location in vertex shader
        glVertexAttribPointer(vertex_location, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), _VBO)
        glEnableVertexAttribArray(vertex_location)
        _EBO = makeEBO(self.indices1)
        _VBO.unbind()
        glBindVertexArray(0)
        
        glBindVertexArray(self._VAO2)
        _VBO = makeVBO(self.vertices)
        vertex_location = 0 # input location in vertex shader
        glVertexAttribPointer(vertex_location, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), _VBO)
        glEnableVertexAttribArray(vertex_location)
        _EBO = makeEBO(self.indices2)
        _VBO.unbind()
        glBindVertexArray(0)
    
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(self.shaderProg)
        glBindVertexArray(self._VAO1)
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)
        glBindVertexArray(self._VAO2)
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        glfw.swap_buffers(self.window)
    
def main():
    initGlfw()
    triangles = Triangles()
    while not glfw.window_should_close(triangles.window):
        glfw.poll_events()
        triangles.draw()
    glfw.terminate()

def key_callback(window, key, scancode, action, mode):
    print(key)
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)
        
if __name__ == '__main__':
    main()
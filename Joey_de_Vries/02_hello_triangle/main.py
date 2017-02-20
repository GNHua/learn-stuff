import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
import numpy as np
# from OpenGL.GLUT import *

WIDTH = 800
HEIGHT = 600

def main():
    print('Starting GLFW context, OpenGL 3.3')
    
    glfw.init()
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    # The following 2 lines are CRUCIAL to get this work on Mac.
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
    
    window = glfw.create_window(WIDTH, HEIGHT, "LearnOpenGL", None, None)
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    
    width, height = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)
    
    vertices = np.array([[ 0.5,  0.5, 0.],
                         [ 0.5, -0.5, 0.],
                         [-0.5, -0.5, 0.],
                         [-0.5,  0.5, 0.]], dtype=GLfloat)
    indices = np.array([[0, 1, 3],
                        [1, 2, 3]], dtype=GLuint)
    
    _VAO = glGenVertexArrays(1)
    glBindVertexArray(_VAO)
    _VBO = vbo.VBO(data=vertices.tostring(), usage='GL_STATIC_DRAW', target='GL_ARRAY_BUFFER')
    _VBO.bind()
    _VBO.copy_data()
    _EBO = vbo.VBO(data=indices.tostring(), usage='GL_STATIC_DRAW', target='GL_ELEMENT_ARRAY_BUFFER')
    _EBO.bind()
    _EBO.copy_data()
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), _VBO)
    glEnableVertexAttribArray(0)
    _VBO.unbind()
    
    vertShaderSource = open('triangle.vert', 'r').read()
    vertShader = shaders.compileShader(vertShaderSource, GL_VERTEX_SHADER)
    fragShaderSource = open('triangle.frag', 'r').read()
    fragShader = shaders.compileShader(fragShaderSource, GL_FRAGMENT_SHADER)
    shaderProg = shaders.compileProgram(vertShader, fragShader)
    glBindVertexArray(0)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        glClearColor(0.2, 0.3, 0.3, 1.)
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shaderProg)
        glBindVertexArray(_VAO)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        
        glfw.swap_buffers(window)
        
    glfw.terminate()

def key_callback(window, key, scancode, action, mode):
    print(key)
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)
        
if __name__ == '__main__':
    main()
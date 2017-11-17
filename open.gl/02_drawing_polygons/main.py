import glfw
from OpenGL.GL import *
import numpy as np
from util import *

WIDTH = 800
HEIGHT = 600


class Triangle:
    def __init__(self):
        self.prepareWindow()
        
        self.vertices = np.array([[-0.5,  0.5, 1., 0., 0.],
                                  [ 0.5,  0.5, 0., 1., 0.],
                                  [ 0.5, -0.5, 0., 0., 1.],
                                  [-0.5, -0.5, 1., 1., 1.]], dtype=GLfloat)
        self.indices = np.array([[0, 1, 2],
                                 [2, 3, 0]], dtype=GLuint)
        self.loadSP()
        
    def __enter__(self):
        glUseProgram(self.shaderProg)
        glBindVertexArray(self._VAO)
        return self
        
    def __exit__(self, type, value, traceback):
        glUseProgram(0)
        glBindVertexArray(0)
        glDeleteProgram(self.shaderProg)
        glDeleteVertexArrays(1, (self._VAO,))
        glDeleteBuffers(1, (self._EBO,))
        glDeleteBuffers(1, (self._VBO,))
        
    def prepareWindow(self):
        self.window = glfw.create_window(WIDTH, HEIGHT, "LearnOpenGL", None, None)
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, key_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
    
        width, height = glfw.get_framebuffer_size(self.window)
        glViewport(0, 0, width, height)
        glClearColor(0., 0., 0., 1.)
        
    def loadSP(self):
        self._VAO = glGenVertexArrays(1)
        
        glBindVertexArray(self._VAO)
        self.shaderProg = make_shader_program('triangle.vert', 'triangle.frag')
        self._VBO = make_buffer_object(data=self.vertices.tostring(), 
                                       usage='GL_STATIC_DRAW', 
                                       target='GL_ARRAY_BUFFER')
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), self._VBO)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), self._VBO + 2 * sizeof(GLfloat))
        glEnableVertexAttribArray(1)
        self._EBO = make_buffer_object(data=self.indices.tostring(),
                                       usage='GL_STATIC_DRAW', 
                                       target='GL_ELEMENT_ARRAY_BUFFER')
        self._VBO.unbind()
        glBindVertexArray(0)
            
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glfw.swap_buffers(self.window)


def main():
    initGlfw()
    with Triangle() as triangle:
        while not glfw.window_should_close(triangle.window):
            glfw.poll_events()
            triangle.draw()
            
    glfw.terminate()


def key_callback(window, key, scancode, action, mode):
    print(key)
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)


if __name__ == '__main__':
    main()
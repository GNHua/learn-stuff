import glfw
from OpenGL.GL import *
import numpy as np
from util import *

WIDTH = 800
HEIGHT = 600
    
class Triangle:
    def __init__(self):
        self.prepareWindow()
        
        self.vertices = np.array([[ 0.5, -0.5, 0., 1., 0., 0.],
                                  [-0.5, -0.5, 0., 0., 1., 0.],
                                  [ 0. ,  0.5, 0., 0., 0., 1.]], dtype=GLfloat)
        self.indices = np.array([0, 1, 2], dtype=GLuint)
        self.loadSP()
    
    def prepareWindow(self):
        self.window = glfw.create_window(WIDTH, HEIGHT, 'LearnOpenGL', None, None)
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, key_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
    
        width, height = glfw.get_framebuffer_size(self.window)
        glViewport(0, 0, width, height)
        glClearColor(0.2, 0.3, 0.3, 1.)
        
    def loadSP(self):
        self.shaderProg = makeShaderProg('triangle.vert', 'triangle.frag', validate=False)
        self._VAO = glGenVertexArrays(1)
        
        glBindVertexArray(self._VAO)
        _VBO = makeVBO(self.vertices)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), _VBO)
        glEnableVertexAttribArray(0)
        _EBO = makeEBO(self.indices)
        _VBO.unbind()
        glBindVertexArray(0)
            
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        with self.shaderProg:
            glBindVertexArray(self._VAO)
            glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, None)
            glBindVertexArray(0)
        glfw.swap_buffers(self.window)
    
def main():
    initGlfw()
    triangle = Triangle()
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
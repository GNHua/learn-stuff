import glfw
from OpenGL.GL import *
import numpy as np
from PIL import Image
from util import *

WIDTH = 800
HEIGHT = 600
    
class Triangle:
    def __init__(self):
        self.prepareWindow()
                                    # Positions       # Colors         # Texture Coords
        self.vertices = np.array([[ 1.0,  1.0, 0.0,   1.0, 0.0, 0.0,   1.0, 1.0],   # Top Right
                                  [ 1.0, -1.0, 0.0,   0.0, 1.0, 0.0,   1.0, 0.0],   # Bottom Right
                                  [-1.0, -1.0, 0.0,   0.0, 0.0, 1.0,   0.0, 0.0],   # Bottom Left
                                  [-1.0,  1.0, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0]],  # Top Left 
                                  dtype=GLfloat)
        self.indices = np.array([[0, 1, 3],
                                 [1, 2, 3]], dtype=GLuint)
        self.shaderProg = makeShaderProg('texture.vert', 'texture.frag', validate=False)
        self.loadVAO()
        self.texture1 = self.makeTexture('container.jpg')
        self.texture2 = self.makeTexture('awesomeface.png')
    
    def prepareWindow(self):
        self.window = glfw.create_window(WIDTH, HEIGHT, "LearnOpenGL", None, None)
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, key_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
    
        width, height = glfw.get_framebuffer_size(self.window)
        glViewport(0, 0, width, height)
        glClearColor(0.2, 0.3, 0.3, 1.)
        
    def loadVAO(self):
        self.VAO = glGenVertexArrays(1)
        with bindVAO(self.VAO):
            _VBO = makeVBO(self.vertices)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), _VBO)
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), _VBO + 3 * sizeof(GLfloat))
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), _VBO + 6 * sizeof(GLfloat))
            glEnableVertexAttribArray(2)
            _VBO.unbind()
            _EBO = makeEBO(self.indices)
            
    def makeTexture(self, image):
        im = Image.open(image)
        w, h = im.size
        try:
            im_bytes = im.tobytes("raw", "RGBA", 0, -1)
        except SystemError:
            im_bytes = im.tobytes("raw", "RGBX", 0, -1)
        
        texture = glGenTextures(1)
        with bindTexture(GL_TEXTURE_2D, texture):
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, im_bytes)
            glGenerateMipmap(GL_TEXTURE_2D)
            
        return texture
            
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        with self.shaderProg, bindVAO(self.VAO), \
          bindTexture(GL_TEXTURE0, GL_TEXTURE_2D, self.texture1), \
          bindTexture(GL_TEXTURE1, GL_TEXTURE_2D, self.texture2):
            glUniform1i(glGetUniformLocation(self.shaderProg, "ourTexture1"), 0);
            glUniform1i(glGetUniformLocation(self.shaderProg, "ourTexture2"), 1);
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
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
import sys, glfw
from OpenGL.GL import *
import numpy as np
from PIL import Image
from util import *
sys.path.append('../')
from _transformations import translation_matrix, rotation_matrix
from _matrix import *

WIDTH = 800
HEIGHT = 600
    
class Triangle:
    def __init__(self):
        self.prepareWindow()
        self.vertices = np.loadtxt('vertices.csv', delimiter=',', dtype=GLfloat)
        self.cubePositions = np.loadtxt('cube_position.csv', delimiter=',', dtype=GLfloat)
        self.shaderProg = makeShaderProg('texture.vert', 'texture.frag', validate=False)
        self.loadVAO()
        self.texture1 = self.makeTexture('../images/container.jpg')
        self.texture2 = self.makeTexture('../images/awesomeface.png')
    
    def prepareWindow(self):
        self.window = glfw.create_window(WIDTH, HEIGHT, "LearnOpenGL", None, None)
        glfw.make_context_current(self.window)
        glfw.set_key_callback(self.window, key_callback)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
    
        width, height = glfw.get_framebuffer_size(self.window)
        glViewport(0, 0, width, height)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.2, 0.3, 0.3, 1.)
        
    def loadVAO(self):
        self.VAO = glGenVertexArrays(1)
        with bindVAO(self.VAO):
            _VBO = makeVBO(self.vertices)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), _VBO)
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(GLfloat), _VBO + 3 * sizeof(GLfloat))
            glEnableVertexAttribArray(1)
            _VBO.unbind()
            
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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        with self.shaderProg, bindVAO(self.VAO), \
          bindTexture(GL_TEXTURE0, GL_TEXTURE_2D, self.texture1), \
          bindTexture(GL_TEXTURE1, GL_TEXTURE_2D, self.texture2):
            glUniform1i(glGetUniformLocation(self.shaderProg, 'ourTexture1'), 0)
            glUniform1i(glGetUniformLocation(self.shaderProg, 'ourTexture2'), 1)
            
            view = translation_matrix([0, 0, -0.5]).T
            projection = perspective_matrix(np.radians(45), WIDTH/HEIGHT, 0.1, 100).T
            viewLoc = glGetUniformLocation(self.shaderProg, 'view')
            glUniformMatrix4fv(viewLoc, 1, GL_FALSE, view)
            projectionLoc = glGetUniformLocation(self.shaderProg, 'projection')
            glUniformMatrix4fv(projectionLoc, 1, GL_FALSE, projection)
            
            modelLoc = glGetUniformLocation(self.shaderProg, 'model')
            for i in range(10):
                model = translation_matrix(self.cubePositions[i]).T
                angle = 20 * i
                model = np.dot(rotation_matrix(angle, [1, 0.3, 0.5]).T, model)
                glUniformMatrix4fv(modelLoc, 1, GL_FALSE, model)
                glDrawArrays(GL_TRIANGLES, 0, 36)
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
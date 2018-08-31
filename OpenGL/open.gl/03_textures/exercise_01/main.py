import glfw
from OpenGL.GL import *
import numpy as np
from PIL import Image
from util import *
from shader import OurShaderProgram

import time


class Triangle:
    def __init__(self):
        self.window = prepare_window()
                                    # Positions  # Colors         # Texture Coords
        self.vertices = np.array([[-0.5,  0.5,   1.0, 0.0, 0.0,   0.0, 1.0],   # Top left
                                  [ 0.5,  0.5,   0.0, 1.0, 0.0,   1.0, 1.0],   # Top right
                                  [ 0.5, -0.5,   0.0, 0.0, 1.0,   1.0, 0.0],   # Bottom right
                                  [-0.5, -0.5,   1.0, 1.0, 1.0,   0.0, 0.0]],  # Bottom left 
                                  dtype=GLfloat)
        self.indices = np.array([[0, 1, 2],
                                 [2, 3, 0]], dtype=GLuint)
        self.make_vao()
        self.texture1 = self.make_texture('../../images/sample.png', unit=GL_TEXTURE0)
        self.shader_program.setInt('ourTexture1', 0)
        self.texture2 = self.make_texture('../../images/sample2.png', unit=GL_TEXTURE1)
        self.shader_program.setInt('ourTexture2', 1)
        self.shader_program.unuse()
        
    def __enter__(self):
        glBindVertexArray(self.vao)
        self.shader_program.use()
        return self
        
    def __exit__(self, type, value, traceback):
        self.shader_program.unuse()
        glBindVertexArray(0)
        self.shader_program.delete()
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.ebo,))
        glDeleteBuffers(1, (self.vbo,))
        
    def make_vao(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.shader_program = OurShaderProgram(vert='texture.vert', frag='texture.frag')
        self.shader_program.use()
        self.vbo = make_buffer_object(data=self.vertices.tostring(), 
                                      usage='GL_STATIC_DRAW', 
                                      target='GL_ARRAY_BUFFER')
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 7*sizeof(GLfloat), self.vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 7*sizeof(GLfloat), self.vbo+2*sizeof(GLfloat))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 7*sizeof(GLfloat), self.vbo+5*sizeof(GLfloat))
        glEnableVertexAttribArray(2)
        self.ebo = make_buffer_object(data=self.indices.tostring(), 
                                      usage='GL_STATIC_DRAW', 
                                      target='GL_ELEMENT_ARRAY_BUFFER')
        self.vbo.unbind()
        glBindVertexArray(0)
        
    def make_texture(self, image, unit=GL_TEXTURE0):
        im = Image.open(image)
        w, h = im.size
        try:
            im_bytes = im.tobytes("raw", "RGBA", 0, -1)
        except ValueError:
            im_bytes = im.tobytes("raw", "RGBX", 0, -1)
        
        texture = glGenTextures(1)
        with bindTexture(unit, GL_TEXTURE_2D, texture):
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, im_bytes)
            glGenerateMipmap(GL_TEXTURE_2D)
            
        return texture
            
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)
        glfw.swap_buffers(self.window)


def main():
    init_glfw()
    time_start = time.time()
    with Triangle() as triangle:
        with bindTexture(GL_TEXTURE0, GL_TEXTURE_2D, triangle.texture1), \
             bindTexture(GL_TEXTURE1, GL_TEXTURE_2D, triangle.texture2):
            uniTime = glGetUniformLocation(triangle.shader_program.id, 'time')
            while not glfw.window_should_close(triangle.window):
                glfw.poll_events()
                glUniform1f(uniTime, time.time()-time_start)
                triangle.draw()
    glfw.terminate()
    
    
if __name__ == '__main__':
    main()
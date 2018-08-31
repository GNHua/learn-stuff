import glfw
from OpenGL.GL import *
import numpy as np
from PIL import Image
import glm
import glm.gtc.matrix_transform as glm_mt

from util import *
from shader import OurShaderProgram


class Triangle:
    def __init__(self):
        self.window = prepare_window()
                                    # Positions        # Colors         # Texture Coords
        self.vertices = np.array([
            [-0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 0.0],
            [ 0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 0.0],
            [ 0.5,  0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
            [ 0.5,  0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
            [-0.5,  0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0],
            [-0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 0.0],

            [-0.5, -0.5,  0.5, 1.0, 1.0, 1.0, 0.0, 0.0],
            [ 0.5, -0.5,  0.5, 1.0, 1.0, 1.0, 1.0, 0.0],
            [ 0.5,  0.5,  0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
            [ 0.5,  0.5,  0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
            [-0.5,  0.5,  0.5, 1.0, 1.0, 1.0, 0.0, 1.0],
            [-0.5, -0.5,  0.5, 1.0, 1.0, 1.0, 0.0, 0.0],

            [-0.5,  0.5,  0.5, 1.0, 1.0, 1.0, 1.0, 0.0],
            [-0.5,  0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
            [-0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0],
            [-0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0],
            [-0.5, -0.5,  0.5, 1.0, 1.0, 1.0, 0.0, 0.0],
            [-0.5,  0.5,  0.5, 1.0, 1.0, 1.0, 1.0, 0.0],

            [ 0.5,  0.5,  0.5, 1.0, 1.0, 1.0, 1.0, 0.0],
            [ 0.5,  0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
            [ 0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0],
            [ 0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0],
            [ 0.5, -0.5,  0.5, 1.0, 1.0, 1.0, 0.0, 0.0],
            [ 0.5,  0.5,  0.5, 1.0, 1.0, 1.0, 1.0, 0.0],

            [-0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0],
            [ 0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
            [ 0.5, -0.5,  0.5, 1.0, 1.0, 1.0, 1.0, 0.0],
            [ 0.5, -0.5,  0.5, 1.0, 1.0, 1.0, 1.0, 0.0],
            [-0.5, -0.5,  0.5, 1.0, 1.0, 1.0, 0.0, 0.0],
            [-0.5, -0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0],

            [-0.5,  0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0],
            [ 0.5,  0.5, -0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
            [ 0.5,  0.5,  0.5, 1.0, 1.0, 1.0, 1.0, 0.0],
            [ 0.5,  0.5,  0.5, 1.0, 1.0, 1.0, 1.0, 0.0],
            [-0.5,  0.5,  0.5, 1.0, 1.0, 1.0, 0.0, 0.0],
            [-0.5,  0.5, -0.5, 1.0, 1.0, 1.0, 0.0, 1.0],
            
            [-1.0, -1.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0],
            [ 1.0, -1.0, -0.5, 0.0, 0.0, 0.0, 1.0, 0.0],
            [ 1.0,  1.0, -0.5, 0.0, 0.0, 0.0, 1.0, 1.0],
            [ 1.0,  1.0, -0.5, 0.0, 0.0, 0.0, 1.0, 1.0],
            [-1.0,  1.0, -0.5, 0.0, 0.0, 0.0, 0.0, 1.0],
            [-1.0, -1.0, -0.5, 0.0, 0.0, 0.0, 0.0, 0.0]], dtype=GLfloat)

        self.make_vao()
        self.texture1 = self.make_texture('../images/sample.png', unit=GL_TEXTURE0)
        self.shader_program.setInt('texKitten', 0)
        self.texture2 = self.make_texture('../images/sample2.png', unit=GL_TEXTURE1)
        self.shader_program.setInt('texPuppy', 1)
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
        glDeleteBuffers(1, (self.vbo,))
        
    def make_vao(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.shader_program = OurShaderProgram(vert='texture.vert', frag='texture.frag')
        self.shader_program.use()
        self.vbo = make_buffer_object(data=self.vertices.tostring(), 
                                      usage='GL_STATIC_DRAW', 
                                      target='GL_ARRAY_BUFFER')
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8*sizeof(GLfloat), self.vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8*sizeof(GLfloat), self.vbo+3*sizeof(GLfloat))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8*sizeof(GLfloat), self.vbo+6*sizeof(GLfloat))
        glEnableVertexAttribArray(2)
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
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        
        glEnable(GL_STENCIL_TEST)
        
        # Draw floor
        glStencilFunc(GL_ALWAYS, 1, 0xFF)
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
        glStencilMask(0xFF)
        glDepthMask(GL_FALSE)
        glClear(GL_STENCIL_BUFFER_BIT)

        glDrawArrays(GL_TRIANGLES, 36, 6)

        # Draw cube reflection
        glStencilFunc(GL_EQUAL, 1, 0xFF)
        glStencilMask(0x00)
        glDepthMask(GL_TRUE)
        
        


def main():
    init_glfw()
    with Triangle() as triangle:
        with bindTexture(GL_TEXTURE0, GL_TEXTURE_2D, triangle.texture1), \
             bindTexture(GL_TEXTURE1, GL_TEXTURE_2D, triangle.texture2):
            uni_model = triangle.shader_program.get_uniform_location('model')
            
            uni_view = triangle.shader_program.get_uniform_location('view')
            view = glm_mt.lookAt(np.array([2.5, 2.5, 2.5]),
                                 np.array([0.0, 0.0, 0.0]),
                                 np.array([0.0, 0.0, 1.0]))
            glUniformMatrix4fv(uni_view, 1, GL_FALSE, np.array(view, dtype=GLfloat))
            
            uni_proj = triangle.shader_program.get_uniform_location('proj')
            proj = glm_mt.perspective(np.radians(45.0), 4/3, 1.0, 10.0)
            glUniformMatrix4fv(uni_proj, 1, GL_FALSE, np.array(proj, dtype=GLfloat))
            
            uni_color = triangle.shader_program.get_uniform_location('overrideColor')
            
            while not glfw.window_should_close(triangle.window):
                glfw.poll_events()
                model = glm_mt.rotate(glm.mat4(), glfw.get_time()*np.pi, np.array([0., 0., 1.]))
                glUniformMatrix4fv(uni_model, 1, GL_FALSE, np.array(model, dtype=GLfloat))
                
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glDrawArrays(GL_TRIANGLES, 0, 36)
        
                glEnable(GL_STENCIL_TEST)
        
                # Draw floor
                glStencilFunc(GL_ALWAYS, 1, 0xFF)
                glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
                glStencilMask(0xFF)
                glDepthMask(GL_FALSE)
                glClear(GL_STENCIL_BUFFER_BIT)

                glDrawArrays(GL_TRIANGLES, 36, 6)

                # Draw cube reflection
                glStencilFunc(GL_EQUAL, 1, 0xFF)
                glStencilMask(0x00)
                glDepthMask(GL_TRUE)
                
                model = glm_mt.scale(
                            glm_mt.translate(model, np.array([0., 0., -1.])),
                            np.array([1., 1., -1.]))
                glUniformMatrix4fv(uni_model, 1, GL_FALSE, np.array(model, dtype=GLfloat))
                glUniform3f(uni_color, 0.3, 0.3, 0.3)
                glDrawArrays(GL_TRIANGLES, 0, 36)
                glUniform3f(uni_color, 1.0, 1.0, 1.0)
                
                glDisable(GL_STENCIL_TEST)
                glfw.swap_buffers(triangle.window)
    glfw.terminate()
    
    
if __name__ == '__main__':
    main()
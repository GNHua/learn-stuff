from OpenGL.GL import *
from OpenGL.GL import shaders


class OurShaderProgram(shaders.ShaderProgram):
    def __init__(vert, frag, **kwargs):
        with open(vert, 'r') as f:
            vert_shader_source = f.read()
        vert_shader = shaders.compileShader(vert_shader_source, GL_VERTEX_SHADER)
        with open(frag, 'r') as f:
            frag_shader_source = f.read()
        frag_shader = shaders.compileShader(frag_shader_source, GL_FRAGMENT_SHADER)
        self.id = shaders.compileProgram(vert_shader, frag_shader, **kwargs)
        
    # activate the shader
    # ------------------------------------------------------------------------
    def use(self):
        glUseProgram(self.id)
        
        
    def setInt(self, name, value):
        glUniform1i(glGetUniformLocation(self.id, name))

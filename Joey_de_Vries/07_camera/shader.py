from OpenGL.GL import *
from OpenGL.GL import shaders


class OurShaderProgram:
    def __init__(self, vert, frag, **kwargs):
        with open(vert, 'r') as f:
            vert_shader_source = f.read()
        vert_shader = shaders.compileShader(vert_shader_source, GL_VERTEX_SHADER)
        with open(frag, 'r') as f:
            frag_shader_source = f.read()
        frag_shader = shaders.compileShader(frag_shader_source, GL_FRAGMENT_SHADER)
        self.id = shaders.compileProgram(vert_shader, frag_shader, **kwargs)
        
    def use(self):
        glUseProgram(self.id)
        
    def unuse(self):
        glUseProgram(0)
        
    def delete(self):
        glDeleteProgram(self.id)
        
    def setBool(self, name, value):
        glUniform1i(glGetUniformLocation(self.id, name), value)
        
    def setInt(self, name, value):
        glUniform1i(glGetUniformLocation(self.id, name), value)
        
    def setFloat(self, name, value):
        glUniform1f(glGetUniformLocation(self.id, name), value)
        
    def setVec2(self, name, array):
        glUniform2fv(glGetUniformLocation(self.id, name), 1, array)
        
    def setVec3(self, name, array):
        glUniform3fv(glGetUniformLocation(self.id, name), 1, array)
        
    def setVec4(self, name, array):
        glUniform4fv(glGetUniformLocation(self.id, name), 1, array)
        
    def setMat2(self, name, array):
        glUniformMatrix2fv(glGetUniformLocation(self.id, name), 1, GL_FALSE, array)
        
    def setMat3(self, name, array):
        glUniformMatrix3fv(glGetUniformLocation(self.id, name), 1, GL_FALSE, array)
        
    def setMat4(self, name, array):
        glUniformMatrix4fv(glGetUniformLocation(self.id, name), 1, GL_FALSE, array)
        
    def get_uniform_location(self, name):
        return glGetUniformLocation(self.id, name)


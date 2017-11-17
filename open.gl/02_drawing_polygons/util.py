import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

__all__ = ['initGlfw', 'make_buffer_object', 'makeShaderProg']

def initGlfw():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    # The following 2 lines are CRUCIAL to get this work on Mac.
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
    
def make_buffer_object(data, usage, target):
    buffer_object = vbo.VBO(data=data, usage=usage, target=target)
    buffer_object.bind()
    buffer_object.copy_data()
    return buffer_object
    
def make_shader_program(vert, frag, **kwargs):
    with open(vert, 'r') as f:
        vert_shader_source = f.read()
    vert_shader = shaders.compileShader(vert_shader_source, GL_VERTEX_SHADER)
    with open(frag, 'r') as f:
        frag_shader_source = f.read()
    frag_shader = shaders.compileShader(frag_shader_source, GL_FRAGMENT_SHADER)
    shader_program = shaders.compileProgram(vert_shader, frag_shader, **kwargs)
    return shader_program
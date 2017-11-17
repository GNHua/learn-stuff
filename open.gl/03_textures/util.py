import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

__all__ = ['init_glfw', 
           'prepare_window', 
           'make_buffer_object', 
           'make_shader_program', 
           'bindVAO', 
           'bindTexture']

def initGlfw():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    # The following 2 lines are CRUCIAL to get this work on Mac.
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)


def prepareWindow():
    window = glfw.create_window(WIDTH, HEIGHT, "LearnOpenGL", None, None)
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_HIDDEN)

    width, height = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)
    glClearColor(0.2, 0.3, 0.3, 1.)
    return window


def key_callback(window, key, scancode, action, mode):
    print(key)
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)


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


class bindVAO:
    def __init__(self, vao):
        self.vao = vao
    def __enter__(self):
        glBindVertexArray(self.vao)
    def __exit__(self, type, value, traceback):
        glBindVertexArray(0)


class bindTexture:
    def __init__(self, *args):
        if len(args) == 2:
            self.unit = GL_TEXTURE0
            self.target, self.texture = args
        elif len(args) == 3:
            self.unit, self.target, self.texture = args
    def __enter__(self):
        glActiveTexture(self.unit)
        glBindTexture(self.target, self.texture)
    def __exit__(self, type, value, traceback):
        glBindTexture(self.target, 0)

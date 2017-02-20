import glfw
from OpenGL.GL import *

WIDTH = 800
HEIGHT = 600

def main():
    print('Starting GLFW context, OpenGL 3.3')
    
    glfw.init()
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    # The following 2 lines are CRUCIAL to get this work on Mac.
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
    
    window = glfw.create_window(WIDTH, HEIGHT, "LearnOpenGL", None, None)
    if not window:
        print('Failed to create GLFW window')
        glfw.terminate()
        return
        
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    
    width, height = glfw.get_framebuffer_size(window)
    glViewport(0, 0, width, height)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        glClearColor(0.2, 0.3, 0.3, 1.)
        glClear(GL_COLOR_BUFFER_BIT)
        
        glfw.swap_buffers(window)
        
    glfw.terminate()

def key_callback(window, key, scancode, action, mode):
    print(key)
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)
        
if __name__ == '__main__':
    main()
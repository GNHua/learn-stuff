from OpenGL.GL import *
import glfw
import HUtil as H
import sys
    
def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    # The following 2 lines are CRUCIAL to get this work on Mac.
    # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    # glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)
    glfw.window_hint(glfw.AUTO_ICONIFY, GL_FALSE)

    window = glfw.create_window(H.SCREEN_WIDTH, H.SCREEN_HEIGHT, "DLP 3D printer", None, None)
    if not window:
        logger.error('Failed to create GLFW window')
        glfw.terminate()
        return
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
    glfw.make_context_current(window)
    
    if not H.initGL():
        print('Unable to initialize graphics library!')
        return 1
    if not H.loadMedia():
        print('Unable to load media!')
        return 2
    
    while not glfw.window_should_close(window):
        glfw.poll_events()
        H.render(window)
        
    glfw.terminate()
    
def key_callback(window, key, scancode, action, mode):
    print(key)
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)
    
if __name__ == '__main__':
    main()
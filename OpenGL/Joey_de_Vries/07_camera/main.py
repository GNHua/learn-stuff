import sys
import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
import numpy as np
from PIL import Image
import glm
import glm.gtc.matrix_transform as glm_mt

import util
from shader import OurShaderProgram
import my_camera


SCR_WIDTH = 800
SCR_HEIGHT = 600

# camera
camera = my_camera.Camera(np.array([0, 0, 3], dtype=GLfloat))
print('----------')
lastX = SCR_WIDTH / 2
lastY = SCR_HEIGHT / 2
firstMouse = True

# timing
deltaTime = 0.0
lastFrame = 0.0


def init_glfw():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    # The following 2 lines are CRUCIAL to get this work on Mac.
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, GL_FALSE)


def prepare_window():
    window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", None, None)
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    
    # tell GLFW to capture our mouse
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    width, height = glfw.get_framebuffer_size(window)
    glClearColor(0.2, 0.3, 0.3, 1.)
    glEnable(GL_DEPTH_TEST)
    return window


def main():
    init_glfw()
    window = prepare_window()
    
    vertices = np.array(
       [[-0.5, -0.5, -0.5,  0.0, 0.0],
        [ 0.5, -0.5, -0.5,  1.0, 0.0],
        [ 0.5,  0.5, -0.5,  1.0, 1.0],
        [ 0.5,  0.5, -0.5,  1.0, 1.0],
        [-0.5,  0.5, -0.5,  0.0, 1.0],
        [-0.5, -0.5, -0.5,  0.0, 0.0],

        [-0.5, -0.5,  0.5,  0.0, 0.0],
        [ 0.5, -0.5,  0.5,  1.0, 0.0],
        [ 0.5,  0.5,  0.5,  1.0, 1.0],
        [ 0.5,  0.5,  0.5,  1.0, 1.0],
        [-0.5,  0.5,  0.5,  0.0, 1.0],
        [-0.5, -0.5,  0.5,  0.0, 0.0],

        [-0.5,  0.5,  0.5,  1.0, 0.0],
        [-0.5,  0.5, -0.5,  1.0, 1.0],
        [-0.5, -0.5, -0.5,  0.0, 1.0],
        [-0.5, -0.5, -0.5,  0.0, 1.0],
        [-0.5, -0.5,  0.5,  0.0, 0.0],
        [-0.5,  0.5,  0.5,  1.0, 0.0],

        [ 0.5,  0.5,  0.5,  1.0, 0.0],
        [ 0.5,  0.5, -0.5,  1.0, 1.0],
        [ 0.5, -0.5, -0.5,  0.0, 1.0],
        [ 0.5, -0.5, -0.5,  0.0, 1.0],
        [ 0.5, -0.5,  0.5,  0.0, 0.0],
        [ 0.5,  0.5,  0.5,  1.0, 0.0],

        [-0.5, -0.5, -0.5,  0.0, 1.0],
        [ 0.5, -0.5, -0.5,  1.0, 1.0],
        [ 0.5, -0.5,  0.5,  1.0, 0.0],
        [ 0.5, -0.5,  0.5,  1.0, 0.0],
        [-0.5, -0.5,  0.5,  0.0, 0.0],
        [-0.5, -0.5, -0.5,  0.0, 1.0],

        [-0.5,  0.5, -0.5,  0.0, 1.0],
        [ 0.5,  0.5, -0.5,  1.0, 1.0],
        [ 0.5,  0.5,  0.5,  1.0, 0.0],
        [ 0.5,  0.5,  0.5,  1.0, 0.0],
        [-0.5,  0.5,  0.5,  0.0, 0.0],
        [-0.5,  0.5, -0.5,  0.0, 1.0]], dtype=GLfloat
    )
    
    cubePositions = np.array(
       [[ 0.0,  0.0,  0.0],
        [ 2.0,  5.0, -15.0],
        [-1.5, -2.2, -2.5],
        [-3.8, -2.0, -12.3],
        [ 2.4, -0.4, -3.5],
        [-1.7,  3.0, -7.5],
        [ 1.3, -2.0, -2.5],
        [ 1.5,  2.0, -2.5],
        [ 1.5,  0.2, -1.5],
        [-1.3,  1.0, -1.5]], dtype=GLfloat
    )
    
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)
    VBO = vbo.VBO(data=vertices.tostring(), usage='GL_STATIC_DRAW', target='GL_ARRAY_BUFFER')
    VBO.bind()
    VBO.copy_data()
    
    ourShader = OurShaderProgram('camera.vert', 'camera.frag')
    
    # position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5*sizeof(GLfloat), VBO)
    glEnableVertexAttribArray(0)
    # texture coord attribute
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5*sizeof(GLfloat), VBO+3*sizeof(GLfloat))
    glEnableVertexAttribArray(1)
    
    texture1 = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture1)
    # set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image, create texture and generate mipmaps
    im = Image.open('../images/container.jpg')
    w, h = im.size
    try:
        im_bytes = im.tobytes("raw", "RGBA", 0, -1)
    except ValueError:
        im_bytes = im.tobytes("raw", "RGBX", 0, -1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, im_bytes)
    glGenerateMipmap(GL_TEXTURE_2D)
    
    texture2 = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture2)
    # set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    # load image, create texture and generate mipmaps
    im = Image.open('../images/awesomeface.png')
    w, h = im.size
    try:
        im_bytes = im.tobytes("raw", "RGBA", 0, -1)
    except ValueError:
        im_bytes = im.tobytes("raw", "RGBX", 0, -1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, im_bytes)
    glGenerateMipmap(GL_TEXTURE_2D)
    
    # tell opengl for each sampler to which texture unit it belongs 
    # to (only has to be done once)
    ourShader.use()
    ourShader.setInt('texture1', 0)
    ourShader.setInt('texture2', 1)
    
    # render loop
    global deltaTime
    global lastFrame
    while not glfw.window_should_close(window):
        # pre-frame time logic
        currentFrame = glfw.get_time()
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame
        
        # input
        processInput(window)
        
        # render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # bind textures on corresponding texture units
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, texture1)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, texture2)
        
        # camera/view transformation
        projection = glm_mt.perspective(np.radians(camera.Zoom), 
                                        SCR_WIDTH/SCR_HEIGHT, 0.1, 100.0)
        ourShader.setMat4('projection', np.array(projection, dtype=GLfloat))
        
        # render boxes
        view = camera.GetViewMatrix()
        ourShader.setMat4('view', np.array(view, dtype=GLfloat))
        
        for i in range(10):
            # calculate the model matrix for each object and pass 
            # it to shader before drawing
            model = glm_mt.translate(glm.mat4(), cubePositions[i])
            angle = 20.0 * i
            model = glm_mt.rotate(model, np.radians(angle), np.array([1, 0.3, 0.5]))
            ourShader.setMat4('model', np.array(model, dtype=GLfloat))
            glDrawArrays(GL_TRIANGLES, 0, 36)
            
        # glfw: swap buffers and poll IO events (keys pressed/released, 
        # mouse moved etc.)
        glfw.swap_buffers(window)
        glfw.poll_events()
        
    # optional: de-allocate all resources once they've outlived their purpose:
    ourShader.unuse()
    glBindVertexArray(0)
    ourShader.delete()
    glDeleteVertexArrays(1, (VAO,))
    glDeleteBuffers(1, (VBO,))
    
    # glfw: terminate, clearing all previously allocated GLFW resources.
    glfw.terminate()


def processInput(window):
    """
    process all input: query GLFW whether relevant keys are pressed/released 
    this frame and react accordingly
    """
    global deltaTime
    
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
        
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.ProcessKeyboard(camera.Camera_Movement.FORWARD, deltaTime)
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.ProcessKeyboard(camera.Camera_Movement.BACKWARD, deltaTime)
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.ProcessKeyboard(camera.Camera_Movement.LEFT, deltaTime)
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        camera.ProcessKeyboard(camera.Camera_Movement.RIGHT, deltaTime)


def framebuffer_size_callback(window, width, height):
    """
    glfw: whenever the window size changed (by OS or user resize) this 
    callback function executes
    """
    # make sure the viewport matches the new window dimensions; note that width and 
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height)


def mouse_callback(window, xpos, ypos):
    """
    glfw: whenever the mouse moves, this callback is called
    """
    global firstMouse
    global lastX
    global lastY
    
    if firstMouse:
        lastX = xpos
        lastY = ypos
        firstMouse = False
        
    xoffset = xpos - lastX
    yoffset = lastY - ypos # reversed since y-coordinates go from bottom to top
    
    lastX = xpos
    lastY = ypos
    
    camera.ProcessMouseMovement(xoffset, yoffset)


def scroll_callback(window, xoffset, yoffset):
    """
    glfw: whenever the mouse scroll wheel scrolls, this callback is called
    """
    camera.ProcessMouseScroll(yoffset)
    
    
if __name__ == '__main__':
    print('+++++++++++++')
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
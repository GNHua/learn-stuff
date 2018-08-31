from OpenGL.GL import *
import glfw
from HTexture import HTexture

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30
gCheckerBoardTexture = HTexture()

def initGL():
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0., SCREEN_WIDTH, 0., SCREEN_HEIGHT, 1., -1.)
   
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0., 0., 0., 1.)
    glEnable(GL_TEXTURE_2D)
    
    error = glGetError()
    if error != GL_NO_ERROR:
        print('Error initializing OpenGL')
        return False
    return True
    
def loadMedia():
    if not gCheckerBoardTexture.loadTextureFromFile(imageName='opengl.png'):
        print('Unable to load file texture!')
        return False
    return True
    
def update():
    pass
    
def render(window):
    glClear(GL_COLOR_BUFFER_BIT)
    x = (SCREEN_WIDTH - gCheckerBoardTexture.mTextureWidth)/2
    y = (SCREEN_HEIGHT - gCheckerBoardTexture.mTextureHeight)/2
    gCheckerBoardTexture.render(x, y)
    glfw.swap_buffers(window)
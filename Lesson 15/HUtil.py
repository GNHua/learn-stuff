from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from HTexture import HFRect, HTexture
import numpy as np

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30
gRepeatingTexture = HTexture()
gTexX, gTexY = 0., 0.
gTextureWrapType = 0

def initGL():
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0., SCREEN_WIDTH, 0., SCREEN_HEIGHT, 1., -1.)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0., 0., 0., 1.)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glDisable(GL_DEPTH_TEST)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    error = glGetError()
    if error != GL_NO_ERROR:
        print('Error initializing OpenGL')
        return False
    return True
    
def loadMedia():
    if not gRepeatingTexture.loadTextureFromFile('texture.png'):
        print('Unable to load repeating texture!')
        return False
    return True
    
def update():
    global gTexX, gTexY
    gTexX += 1
    gTexY += 1
    if gTexX >= gRepeatingTexture.mTextureWidth:
        gTexX = 0.
    if gTexY >= gRepeatingTexture.mTextureHeight:
        gTexY = 0.
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    textureRight = SCREEN_WIDTH / gRepeatingTexture.mTextureWidth
    textureBottom = SCREEN_HEIGHT / gRepeatingTexture.mTextureHeight
    glBindTexture(GL_TEXTURE_2D, gRepeatingTexture.mTextureID)
    glMatrixMode(GL_TEXTURE)
    glLoadIdentity()
    glTranslatef(gTexX / gRepeatingTexture.mTextureWidth, gTexY / gRepeatingTexture.mTextureHeight, 0.)
    
    glBegin(GL_QUADS)
    glTexCoord2f(           0.,            0. ); glVertex2f(           0.,            0. );
    glTexCoord2f( textureRight,            0. ); glVertex2f( SCREEN_WIDTH,            0. );
    glTexCoord2f( textureRight, textureBottom ); glVertex2f( SCREEN_WIDTH, SCREEN_HEIGHT );
    glTexCoord2f(           0., textureBottom ); glVertex2f(           0., SCREEN_HEIGHT );
    glEnd()
    glutSwapBuffers()
    
def handleKeys(key, x, y):
    global gTextureWrapType
    if key == b'q':
        gTextureWrapType += 1
        if gTextureWrapType >= 5:
            gTextureWrapType = 0
            
        glBindTexture(GL_TEXTURE_2D, gRepeatingTexture.mTextureID)
        if gTextureWrapType == 0:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            print( "%d: GL_REPEAT" % gTextureWrapType )
        elif gTextureWrapType == 1:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            print( "%d: GL_CLAMP" % gTextureWrapType )
        elif gTextureWrapType == 2:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
            print( "%d: GL_CLAMP_TO_BORDER" % gTextureWrapType )
        elif gTextureWrapType == 3:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            print( "%d: GL_CLAMP_TO_EDGE" % gTextureWrapType )
        elif gTextureWrapType == 4:
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT)
            print( "%d: GL_MIRRORED_REPEAT" % gTextureWrapType )
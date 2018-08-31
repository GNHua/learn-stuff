from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from HSpriteSheet import HSpriteSheet
from HFRect import HFRect

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30

gArrowSprites = HSpriteSheet()

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
    if not gArrowSprites.loadTextureFromFile("arrows.png"):
        print('Unable to load sprite texture!')
        return False
       
    # Top left 
    clipTL = HFRect(x=0, y=0, w=128, h=128)
    gArrowSprites.addClipSprite( clipTL )

    # Top right
    clipTR = HFRect(x=128, y=0, w=128, h=128)
    gArrowSprites.addClipSprite( clipTR )

    # Bottom left
    clipBL = HFRect(x=0, y=128, w=128, h=128)
    gArrowSprites.addClipSprite( clipBL )

    # Bottom right
    clipBR = HFRect(x=128, y=128, w=128, h=128)
    gArrowSprites.addClipSprite( clipBR )
    
    if not gArrowSprites.generateDataBuffer():
        print('Unable to clip sprite sheet!')
        return False
    return True
    
def update():
    pass
    
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Render top left arrow
    glLoadIdentity()
    glTranslatef( 64., 64., 0. )
    gArrowSprites.renderSprite( 0 )

    # Render top right arrow
    glLoadIdentity()
    glTranslatef( SCREEN_WIDTH - 64., 64., 0. )
    gArrowSprites.renderSprite( 1 )

    # Render bottom left arrow
    glLoadIdentity()
    glTranslatef( 64., SCREEN_HEIGHT - 64., 0. )
    gArrowSprites.renderSprite( 2 )

    # Render bottom right arrow
    glLoadIdentity()
    glTranslatef( SCREEN_WIDTH - 64., SCREEN_HEIGHT - 64., 0. )
    gArrowSprites.renderSprite( 3 )

    glutSwapBuffers()
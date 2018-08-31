from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from HTexture import HFRect, HTexture
import numpy as np

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
SCREEN_FPS = 30
gRotatingTexture = HTexture()
gAngle = 30.
gTransformationCombo = 0

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
    if not gRotatingTexture.loadTextureFromFile('texture.png'):
        print('Unable to load OpenGL texture!')
        return False
    return True
    
def update():
    global gAngle
    gAngle += 360 / SCREEN_FPS
    if gAngle > 360:
        gAngle -= 360
    
def render():
    global gAngle
    global gTransformationCombo
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    if gTransformationCombo == 0:
        glTranslatef( SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0. )
        glRotatef( gAngle, 0., 0., 1. )
        glScalef( 2., 2., 0. )
        glTranslatef( gRotatingTexture.mImageWidth / -2., gRotatingTexture.mImageHeight / -2., 0. )
    elif gTransformationCombo == 1:
        glTranslatef( SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0. )
        glRotatef( gAngle, 0., 0., 1. )
        glTranslatef( gRotatingTexture.mImageWidth / -2., gRotatingTexture.mImageHeight / -2., 0. )
        glScalef( 2., 2., 0. )
    elif gTransformationCombo == 2:
        glScalef( 2., 2., 0. )
        glTranslatef( SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0. )
        glRotatef( gAngle, 0., 0., 1. )
        glTranslatef( gRotatingTexture.mImageWidth / -2., gRotatingTexture.mImageHeight / -2., 0. )
    elif gTransformationCombo == 3:
        glTranslatef( SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0. )
        glRotatef( gAngle, 0., 0., 1. )
        glScalef( 2., 2., 0. )
    elif gTransformationCombo == 4:
        glRotatef( gAngle, 0., 0., 1. )
        glTranslatef( SCREEN_WIDTH / 2., SCREEN_HEIGHT / 2., 0. )
        glScalef( 2., 2., 0. )
        glTranslatef( gRotatingTexture.mImageWidth / -2., gRotatingTexture.mImageHeight / -2., 0. )
    gRotatingTexture.render(0., 0.)
    glutSwapBuffers()
    
def handleKeys(key, x, y):
    global gAngle
    global gTransformationCombo
    if key == b'q':
        gAngle = 0.
        gTransformationCombo += 1
        if gTransformationCombo > 4:
            gTransformationCombo = 0
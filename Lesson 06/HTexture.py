from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

class HTexture:
    def __init__(self):
        self.mTextureID = 0
        self.mTextureWidth = 0
        self.mTextureHeight = 0
        
    def loadTextureFromFile(self, imageName='texture.png'):
        im = Image.open(imageName)
        try:
            ix, iy, image = im.size[0], im.size[1], im.tobytes("raw", "RGBA", 0, -1)
        except SystemError:
            ix, iy, image = im.size[0], im.size[1], im.tobytes("raw", "RGBX", 0, -1)
        return self.loadTextureFromPixels32(image, ix, iy)
        
    def loadTextureFromPixels32(self, pixels, w, h):
        self.freeTexture()
        self.mTextureWidth = w
        self.mTextureHeight = h
        
        self.mTextureID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.mTextureID)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        error = glGetError()
        if error != GL_NO_ERROR:
            print("Error loading texture")
            return False
        return True
        
    def freeTexture(self):
        if self.mTextureID != 0:
            glDeleteTextures(1, self.mTextureID)
            self.mTextureID = 0
        self.mTextureWidth = 0
        self.mTextureHeight = 0
        
    def render(self, x, y):
        if self.mTextureID != 0:
            glLoadIdentity()
            glTranslatef(x, y, 0.)
            glBindTexture(GL_TEXTURE_2D, self.mTextureID)
            
            glBegin(GL_QUADS)
            glTexCoord2f( 0., 0. ); glVertex2f(                 0.,                  0. );
            glTexCoord2f( 1., 0. ); glVertex2f( self.mTextureWidth,                  0. );
            glTexCoord2f( 1., 1. ); glVertex2f( self.mTextureWidth, self.mTextureHeight );
            glTexCoord2f( 0., 1. ); glVertex2f(                 0., self.mTextureHeight );
            glEnd()
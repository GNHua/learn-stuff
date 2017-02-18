from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

class HFRect:
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.w = 0.
        self.h = 0.

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
        
    def render(self, x, y, clip=None):
        if self.mTextureID != 0:
            glLoadIdentity()
            texTop = 0.
            texBottom = 1.
            texLeft = 0.
            texRight = 1.
            quadWidth = self.mTextureWidth
            quadHeight = self.mTextureHeight
            
            if clip != None:
                texLeft = clip.x / self.mTextureWidth
                texRight = (clip.x + clip.w) / self.mTextureWidth
                texTop = clip.y / self.mTextureHeight
                texBottom = (clip.y + clip.h) / self.mTextureHeight
                quadWidth = clip.w
                quadHeight = clip.h
            
            glTranslatef(x, y, 0.)
            glBindTexture(GL_TEXTURE_2D, self.mTextureID)
            
            glBegin(GL_QUADS)
            glTexCoord2f(  texLeft,    texTop ); glVertex2f(        0.,         0. );
            glTexCoord2f( texRight,    texTop ); glVertex2f( quadWidth,         0. );
            glTexCoord2f( texRight, texBottom ); glVertex2f( quadWidth, quadHeight );
            glTexCoord2f(  texLeft, texBottom ); glVertex2f(        0., quadHeight );
            glEnd()
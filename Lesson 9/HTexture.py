from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np

def next_p2(num):
    temp = 1
    while (temp < num):
        temp <<= 1
    return temp
    
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
        self.mImageWidth = 0
        self.mImageHeight = 0
        self.mPixels = None
        
    def loadTextureFromFile(self, imageName='texture.png'):
        im = Image.open(imageName)
        imgWidth, imgHeight = im.size[0], im.size[1]
        ix, iy = next_p2(imgWidth), next_p2(imgHeight)
        paddedImage = Image.new('RGBA', (ix, iy), (0, 0, 0, 0))
        paddedImage.paste(im, (0, iy - imgHeight, imgWidth, iy))
        try:
            image = paddedImage.tobytes("raw", "RGBA", 0, -1)
        except SystemError:
            image = paddedImage.tobytes("raw", "RGBX", 0, -1)
        # paddedImage.save('padded.png')
        return self.loadTextureFromPixels32(image, imgWidth, imgHeight, ix, iy)
        
    def loadTextureFromPixels32(self, pixels, imgWidth, imgHeight, texWidth, texHeight):
        self.freeTexture()
        self.mTextureWidth = texWidth
        self.mTextureHeight = texHeight
        self.mImageWidth = imgWidth
        self.mImageHeight = imgHeight
        
        self.mTextureID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.mTextureID)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texWidth, texHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, pixels)
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
        self.mPixels = None
        self.mTextureWidth = 0
        self.mTextureHeight = 0
        self.mImageWidth = 0
        self.mImageHeight = 0
        
    def lock(self):
        if self.mPixels is None and self.mTextureID != 0:
            glBindTexture( GL_TEXTURE_2D, self.mTextureID )
            rawPixels = glGetTexImage( GL_TEXTURE_2D, 0, GL_RGBA, GL_UNSIGNED_BYTE )
            self.mPixels = np.frombuffer(rawPixels, dtype='S4').reshape(self.mTextureHeight, self.mTextureWidth)
            self.mPixels.flags.writeable = True
            glBindTexture( GL_TEXTURE_2D, 0 )
            return True
        return False
        
    def unlock(self):
        if self.mPixels is not None and self.mTextureID != 0:
            glBindTexture( GL_TEXTURE_2D, self.mTextureID )
            glTexSubImage2D( GL_TEXTURE_2D, 0, 0, 0, self.mTextureWidth, self.mTextureHeight, \
                GL_RGBA, GL_UNSIGNED_BYTE, np.ascontiguousarray(self.mPixels).data )
            self.mPixels = None
            glBindTexture( GL_TEXTURE_2D, 0 )
            return True
        return False
        
    def getPixel32(self, x, y):
        return self.mPixels[ y, x ]
        
    def setPixel32(self, x, y, pixel):
        self.mPixels[ y, x ] = pixel
        
    def render(self, x, y, clip = None):
        if self.mTextureID != 0:
            glLoadIdentity()
            texTop = 0.
            texBottom = self.mImageHeight / self.mTextureHeight
            texLeft = 0.
            texRight = self.mImageWidth / self.mTextureWidth
            quadWidth = self.mImageWidth
            quadHeight = self.mImageHeight
            
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
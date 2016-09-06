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
    def __init__(self, x=0., y=0., w=0., h=0.):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

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
        
    def loadPixelsFromFile(self, imageName='texture.png'):
        self.freeTexture()
        try:
            im = Image.open(imageName)
        except:
            return False
        imgWidth, imgHeight = im.size[0], im.size[1]
        ix, iy = next_p2(imgWidth), next_p2(imgHeight)
        paddedImage = Image.new('RGBA', (ix, iy), (0, 0, 0, 0))
        paddedImage.paste(im, (0, iy - imgHeight, imgWidth, iy))
        try:
            image = paddedImage.tobytes("raw", "RGBA", 0, -1)
        except SystemError:
            image = paddedImage.tobytes("raw", "RGBX", 0, -1)
        # paddedImage.save('padded.png')
        self.mImageWidth = imgWidth
        self.mImageHeight = imgHeight
        self.mPixels = np.frombuffer(image, dtype='S4').reshape(iy, ix)
        self.mPixels.flags.writeable = True
        return True
        
    def loadTextureFromFileWithColorKey(self, imName, rgba):
        if not self.loadPixelsFromFile(imName):
            return False
        self.mPixels[ (self.mPixels == rgba) | (self.mPixels == rgba[:-1]+b'\x00') ] \
            = b'\xFF\xFF\xFF\x00'
        return self.loadTextureFromPixels32(np.ascontiguousarray(self.mPixels).data, \
            self.mImageWidth, self.mImageHeight, self.mPixels.shape[1], self.mPixels.shape[0])
        
    def loadTextureFromPixels32(self, pixels, imgWidth, imgHeight, texWidth, texHeight):
        self.freeTexture()
        self.mTextureWidth = texWidth
        self.mTextureHeight = texHeight
        self.mImageWidth = imgWidth
        self.mImageHeight = imgHeight
        
        self.mTextureID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.mTextureID)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texWidth, texHeight, 0, GL_RGBA, \
            GL_UNSIGNED_BYTE, pixels)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
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
            self.mPixels = np.frombuffer(rawPixels, dtype='S4').reshape(self.mTextureHeight, \
                self.mTextureWidth)
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
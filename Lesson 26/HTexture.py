from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
import numpy as np
from HStruct import HVertexData2D
from OpenGL.arrays import vbo

def next_p2(num):
    temp = 1
    while (temp < num):
        temp <<= 1
    return temp

class HTexture:
    def __init__(self):
        self.mTextureID = 0
        self.mPixels = None
        self.mTextureWidth = 0
        self.mTextureHeight = 0
        self.mImageWidth = 0
        self.mImageHeight = 0
        self.mVBO = None
        self.mIBO = None
        
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
        self.initVBO()
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
        
    def initVBO(self):
        if self.mTextureID != 0 and self.mVBO is None:
            vData = []
            for i in range(4):
                vData.append(HVertexData2D())  
            iData = np.arange(4, dtype=GLuint)
            
            vDataBytes = vData[0].tobytes() + vData[1].tobytes() + vData[2].tobytes() + vData[3].tobytes()
            self.mVBO = vbo.VBO(data=vDataBytes, usage='GL_DYNAMIC_DRAW', target='GL_ARRAY_BUFFER')
            self.mIBO = vbo.VBO(data=iData.tobytes(), usage='GL_DYNAMIC_DRAW', target='GL_ELEMENT_ARRAY_BUFFER')
            
    def freeVBO(self):
        if self.mVBO is not None:
            self.mVBO.delete()
            self.mVBO = None
            self.mIBO.delete()
            self.mIBO = None
        
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
            
            if clip is not None:
                texLeft = clip.x / self.mTextureWidth
                texRight = (clip.x + clip.w) / self.mTextureWidth
                texTop = clip.y / self.mTextureHeight
                texBottom = (clip.y + clip.h) / self.mTextureHeight
                quadWidth = clip.w
                quadHeight = clip.h
                
            glTranslatef(x, y, 0.)
            
            vData = []
            for i in range(4):
                vData.append(HVertexData2D())

            # Texture coordinates
            vData[ 0 ].texCoord.s =  texLeft; vData[ 0 ].texCoord.t =    texTop;
            vData[ 1 ].texCoord.s = texRight; vData[ 1 ].texCoord.t =    texTop;
            vData[ 2 ].texCoord.s = texRight; vData[ 2 ].texCoord.t = texBottom;
            vData[ 3 ].texCoord.s =  texLeft; vData[ 3 ].texCoord.t = texBottom;

            # Vertex positions
            vData[ 0 ].position.x =        0.; vData[ 0 ].position.y =         0.;
            vData[ 1 ].position.x = quadWidth; vData[ 1 ].position.y =         0.;
            vData[ 2 ].position.x = quadWidth; vData[ 2 ].position.y = quadHeight;
            vData[ 3 ].position.x =        0.; vData[ 3 ].position.y = quadHeight;
            
            glBindTexture(GL_TEXTURE_2D, self.mTextureID)
            glEnableClientState( GL_VERTEX_ARRAY )
            glEnableClientState( GL_TEXTURE_COORD_ARRAY )
            
            self.mVBO.bind()
            vDataBytes = vData[0].tobytes() + vData[1].tobytes() + vData[2].tobytes() + vData[3].tobytes()
            self.mVBO.set_array(data=vDataBytes)
            self.mVBO.copy_data()
            glVertexPointer(2, GL_FLOAT, vData[0].size, self.mVBO + vData[0].posOffset)
            glTexCoordPointer(2, GL_FLOAT, vData[0].size, self.mVBO + vData[0].texOffset)
            
            self.mIBO.bind()
            glDrawElements( GL_QUADS, 4, GL_UNSIGNED_INT, self.mIBO )
            glDisableClientState( GL_TEXTURE_COORD_ARRAY )
            glDisableClientState( GL_VERTEX_ARRAY )
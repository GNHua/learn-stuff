from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy as np
from HVertexData2D import HVertexData2D
from HTexture import HTexture

class HSpriteSheet(HTexture):
    def __init__(self, *args, **kwargs):
        super().__init__()
        
        self.mVertexDataBuffer = None
        self.mIndexBuffers = None
        
        self.mClips = []
        
    def addClipSprite(self, newClip):
        self.mClips.append(newClip)
        return len(self.mClips) - 1
        
    def getClip(self, index):
        return self.mClips[index]
        
    def generateDataBuffer(self):
        if self.mTextureID != 0 and len(self.mClips) > 0:
            totalSprites = len(self.mClips)
            vertexData = []
            vertexDataBytes = b''
            for i in range(totalSprites * 4):
                vertexData.append(HVertexData2D())
            self.vertexDataSize = vertexData[0].size()
            self.vertexDataTexOffset = vertexData[0].texOffset()
            self.vertexDataPosOffset = vertexData[0].posOffset()
            
            self.mIndexBuffers = []
            spriteIndices = np.arange(4, dtype=GLuint)
            for i in range(totalSprites):
                if i != 0:
                    spriteIndices += 4
                # Top left
                vertexData[ spriteIndices[ 0 ] ].position.x = -self.mClips[ i ].w / 2.
                vertexData[ spriteIndices[ 0 ] ].position.y = -self.mClips[ i ].h / 2.

                vertexData[ spriteIndices[ 0 ] ].texCoord.s =  (self.mClips[ i ].x) / self.mTextureWidth
                vertexData[ spriteIndices[ 0 ] ].texCoord.t =  (self.mClips[ i ].y) / self.mTextureHeight

                # Top right
                vertexData[ spriteIndices[ 1 ] ].position.x =  self.mClips[ i ].w / 2.
                vertexData[ spriteIndices[ 1 ] ].position.y = -self.mClips[ i ].h / 2.

                vertexData[ spriteIndices[ 1 ] ].texCoord.s =  (self.mClips[ i ].x + self.mClips[ i ].w) / self.mTextureWidth
                vertexData[ spriteIndices[ 1 ] ].texCoord.t =  (self.mClips[ i ].y) / self.mTextureHeight

                # Bottom right
                vertexData[ spriteIndices[ 2 ] ].position.x =  self.mClips[ i ].w / 2.
                vertexData[ spriteIndices[ 2 ] ].position.y =  self.mClips[ i ].h / 2.

                vertexData[ spriteIndices[ 2 ] ].texCoord.s =  (self.mClips[ i ].x + self.mClips[ i ].w) / self.mTextureWidth
                vertexData[ spriteIndices[ 2 ] ].texCoord.t =  (self.mClips[ i ].y + self.mClips[ i ].h) / self.mTextureHeight

                # Bottom left
                vertexData[ spriteIndices[ 3 ] ].position.x = -self.mClips[ i ].w / 2.
                vertexData[ spriteIndices[ 3 ] ].position.y =  self.mClips[ i ].h / 2.

                vertexData[ spriteIndices[ 3 ] ].texCoord.s =  (self.mClips[ i ].x) / self.mTextureWidth
                vertexData[ spriteIndices[ 3 ] ].texCoord.t =  (self.mClips[ i ].y + self.mClips[ i ].h) / self.mTextureHeight
                
                for i in range(4):
                    vertexDataBytes += vertexData[ spriteIndices[ i ] ].tostring()
                
                indexBuffer = vbo.VBO(data=spriteIndices.tostring(), usage='GL_STATIC_DRAW', target='GL_ELEMENT_ARRAY_BUFFER')
                self.mIndexBuffers.append(indexBuffer)
                
            self.mVertexDataBuffer = vbo.VBO(data=vertexDataBytes, usage='GL_STATIC_DRAW', target='GL_ARRAY_BUFFER')
            
        elif self.mTextureID == 0:
            print('No texture to render with!')
            return False
        elif len(self.mClips) <= 0:
            print('No clips to generate vertex data from!')
            return False
        return True
        
    def freeSheet(self):
        if self.mVertexDataBuffer is not None:
            self.mVertexDataBuffer.delete()
            self.mVertexDataBuffer = None
            
        if self.mIndexBuffers is not None:
            for buf in self.mIndexBuffer:
                buf.delete()
            self.mIndexBuffers = None
            
        self.mClips = []
        
    def freeTexture(self):
        self.freeSheet()
        super().freeTexture()
        
    def renderSprite(self, index):
        if self.mVertexDataBuffer is not None:
            glBindTexture(GL_TEXTURE_2D, self.mTextureID)
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            self.mVertexDataBuffer.bind()
            glTexCoordPointer(2, GL_FLOAT, self.vertexDataSize, self.mVertexDataBuffer + self.vertexDataTexOffset)
            glVertexPointer(2, GL_FLOAT, self.vertexDataSize, self.mVertexDataBuffer + self.vertexDataPosOffset)
            
            self.mIndexBuffers[index].bind()
            glDrawElements( GL_QUADS, 4, GL_UNSIGNED_INT, None )
            
            glDisableClientState( GL_TEXTURE_COORD_ARRAY )
            glDisableClientState( GL_VERTEX_ARRAY )
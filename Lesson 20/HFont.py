from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import numpy as np
from HVertexData2D import HVertexData2D
from HSpriteSheet import HSpriteSheet

class HFont(HSpriteSheet):
    def __init__(self):
        self.mSpace = 0.
        self.mLineHeight = 0.
        self.mNewLine = 0.
        
    def loadBitmap(self, image):
        BLACK_PIXEL = GLuint(0xFF000000)
        self.freeFont()
        
        if self.loadPixelsFromFile(image):
            cellW = self.mImageWidth / 16.
            cellH = self.mImageHeight / 16.
            
            top = cellH
            bottom = 0
            aBottom = 0
            
            pX = 0
            pY = 0
            bX = 0
            bY = 0
            
            currentChar = 0
        
        
    def freeFont(self):
        self.freeTexture()
        self.mSpace = 0.
        self.mLineHeight = 0.
        self.mNewLine = 0.
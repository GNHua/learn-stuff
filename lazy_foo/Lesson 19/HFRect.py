from OpenGL.GL import *

class HFRect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def tostring(self):
        return toBytes(self.x) + toBytes(self.y) + toBytes(self.w) + toBytes(self.h)
        
    def size(self):
        return 4 * sizeof(GLfloat)
        
def toBytes(val):
    return bytes(GLfloat(val))
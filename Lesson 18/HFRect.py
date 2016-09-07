from OpenGL.GL import *

class HFRect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = GLfloat(x)
        self.y = GLfloat(y)
        self.w = GLfloat(w)
        self.h = GLfloat(h)
        
    def tostring(self):
        return bytes(self.x) + bytes(self.y) + bytes(self.w) + bytes(self.h)
        
    def size(self):
        return 4 * sizeof(GLfloat)
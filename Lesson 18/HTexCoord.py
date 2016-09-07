from OpenGL.GL import *

class HTexCoord:
    def __init__(self, s=0, t=0):
        self.s = GLfloat(s)
        self.t = GLfloat(t)
        
    def tostring(self):
        return bytes(self.s) + bytes(self.t)
        
    def size(self):
        return 2 * sizeof(GLfloat)
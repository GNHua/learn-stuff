from OpenGL.GL import *

class HTexCoord:
    def __init__(self, s=0, t=0):
        self.s = s
        self.t = t
        
    def tostring(self):
        return toBytes(self.s) + toBytes(self.t)
        
    def size(self):
        return 2 * sizeof(GLfloat)

def toBytes(val):
    return bytes(GLfloat(val))
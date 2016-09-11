from OpenGL.GL import *

class HVertexPos2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def tostring(self):
        return toBytes(self.x) + toBytes(self.y)
        
    def size(self):
        return 2 * sizeof(GLfloat)

def toBytes(val):
    return bytes(GLfloat(val))
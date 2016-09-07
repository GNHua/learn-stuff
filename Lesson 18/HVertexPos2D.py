from OpenGL.GL import *

class HVertexPos2D:
    def __init__(self, x=0, y=0):
        self.x = GLfloat(x)
        self.y = GLfloat(y)
        
    def tostring(self):
        return bytes(self.x) + bytes(self.y)
        
    def size(self):
        return 2 * sizeof(GLfloat)
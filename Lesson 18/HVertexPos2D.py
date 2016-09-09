from OpenGL.GL import *

class HVertexPos2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def tostring(self):
        return bytes(self.x) + bytes(self.y)
        
    def size(self):
        return 2 * sizeof(GLfloat)

    def get_x(self): return self.__x
    def set_x(self, value): self.__x = GLfloat(value)
    def del_x(self): del self.__x
    x = property(get_x, set_x, del_x)
    
    def get_y(self): return self.__y
    def set_y(self, value): self.__y = GLfloat(value)
    def del_y(self): del self.__y
    y = property(get_y, set_y, del_y)
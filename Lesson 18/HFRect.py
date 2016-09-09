from OpenGL.GL import *

class HFRect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def tostring(self):
        return bytes(self.x) + bytes(self.y) + bytes(self.w) + bytes(self.h)
        
    def size(self):
        return 4 * sizeof(GLfloat)
        
    def get_x(self): return self.__x
    def set_x(self, value): self.__x = GLfloat(value)
    def del_x(self): del self.__x
    x = property(get_x, set_x, del_x)
    
    def get_y(self): return self.__y
    def set_y(self, value): self.__y = GLfloat(value)
    def del_y(self): del self.__y
    y = property(get_y, set_y, del_y)

    def get_w(self): return self.__w
    def set_w(self, value): self.__w = GLfloat(value)
    def del_w(self): del self.__w
    w = property(get_w, set_w, del_w)
    
    def get_h(self): return self.__h
    def set_h(self, value): self.__h = GLfloat(value)
    def del_h(self): del self.__h
    h = property(get_h, set_h, del_h)
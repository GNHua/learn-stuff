from OpenGL.GL import *

class HTexCoord:
    def __init__(self, s=0, t=0):
        self.s = s
        self.t = t
        
    def tostring(self):
        return bytes(self.s) + bytes(self.t)
        
    def size(self):
        return 2 * sizeof(GLfloat)

    def get_s(self): return self.__s
    def set_s(self, value): self.__s = GLfloat(value)
    def del_s(self): del self.__s
    s = property(get_s, set_s, del_s)
    
    def get_t(self): return self.__t
    def set_t(self, value): self.__t = GLfloat(value)
    def del_t(self): del self.__t
    t = property(get_t, set_t, del_t)
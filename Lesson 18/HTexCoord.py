from OpenGL.GL import *

class HTexCoord:
    def __init__(self, s=0, t=0):
        self.s = s
        self.t = t
        
    def tostring(self):
        return bytes(self.s) + bytes(self.t)
        
    def size(self):
        return 2 * sizeof(GLfloat)

    def get_foo(self): return self.__foo
    def set_foo(self, value): self.__foo = GLfloat(value)
    def del_foo(self): del self.__foo
    s = property(get_foo, set_foo, del_foo)
    t = property(get_foo, set_foo, del_foo)
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

    def get_foo(self): return self.__foo
    def set_foo(self, value): self.__foo = GLfloat(value)
    def del_foo(self): del self.__foo
    x = property(get_foo, set_foo, del_foo)
    y = property(get_foo, set_foo, del_foo)
    w = property(get_foo, set_foo, del_foo)
    h = property(get_foo, set_foo, del_foo)
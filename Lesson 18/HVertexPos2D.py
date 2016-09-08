from OpenGL.GL import *

class HVertexPos2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def tostring(self):
        return bytes(self.x) + bytes(self.y)
        
    def size(self):
        return 2 * sizeof(GLfloat)

    def get_foo(self): return self.__foo
    def set_foo(self, value): self.__foo = GLfloat(value)
    def del_foo(self): del self.__foo
    x = property(get_foo, set_foo, del_foo)
    y = property(get_foo, set_foo, del_foo)
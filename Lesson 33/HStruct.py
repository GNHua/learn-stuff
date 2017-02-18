from OpenGL.GL import GLfloat, sizeof
from struct import pack

class BaseStruct:
    def __init__(self, attr_list):
        self.attr_list = attr_list
        for i in attr_list:
            setattr(self, i, 0.)
            
    @property
    def bytes(self):
        return pack('f' * len(self.attr_list), *[self.__dict__[key] for key in self.attr_list])
        
    @property
    def size(self):
        return len(self.attr_list) * sizeof(GLfloat)
            
class HVertexPos2D(BaseStruct):
    def __init__(self, x=0., y=0.):
        super().__init__(attr_list=['x', 'y'])
        self.x, self.y = x, y

class HColorRGBA(BaseStruct):
    def __init__(self, r=0., g=0., b=0., a=0.):
        super().__init__(attr_list=['r', 'g', 'b', 'a'])
        self.r, self.g, self.b, self.a = r, g, b, a
        
class HMultiColorVertex2D:
    size = 6 * sizeof(GLfloat)
    posOffset = 0
    colorOffset = 2 * sizeof(GLfloat)
    
    def __init__(self):
        self.pos = HVertexPos2D()
        self.rgba = HColorRGBA()
        
    def __add__(self, other):
        if isinstance(other, HMultiColorVertex2D):
            return self.pos.bytes + self.rgba.bytes + other.pos.bytes + other.rgba.bytes
        elif isinstance(other, bytes):
            return self.pos.bytes + self.rgba.bytes + other
            
    def __radd__(self, other):
        if isinstance(other, HMultiColorVertex2D):
            return other.pos.bytes + other.rgba.bytes + self.pos.bytes + self.rgba.bytes
        elif isinstance(other, bytes):
            return other + self.pos.bytes + self.rgba.bytes
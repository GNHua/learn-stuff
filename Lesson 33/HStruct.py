from inspect import Parameter, Signature
from OpenGL.GL import GLfloat, sizeof
from struct import pack

def make_signature(names):
    return Signature(Parameter(name, Parameter.POSITIONAL_OR_KEYWORD, default=0.)
                               for name in names)

class MetaStruct(type):
    def __new__(cls, name, bases, clsdict):
        clsobj = super().__new__(cls, name, bases, clsdict)
        sig = make_signature(clsobj._fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj

class BaseStruct(metaclass=MetaStruct):
    _fields = []
    def __init__(self, *args, **kwargs):
        bound = self.__signature__.bind(*args, **kwargs)
        bound.apply_defaults()
        for name, val in bound.arguments.items():
            setattr(self, name, val)
            
    @property
    def bytes(self):
        return pack('f' * len(self._fields), *[self.__dict__[key] for key in self._fields])
        
    @property
    def size(self):
        return len(self._fields) * sizeof(GLfloat)
        
    def __add__(self, other):
        if isinstance(other, BaseStruct):
            return self.bytes + other.bytes
        elif isinstance(other, bytes):
            return self.bytes + other
            
    def __radd__(self, other):
        if isinstance(other, BaseStruct):
            return other.bytes + self.bytes
        elif isinstance(other, bytes):
            return other + self.bytes
            
class HVertexPos2D(BaseStruct):
    _fields = ['x', 'y']

class HColorRGBA(BaseStruct):
    _fields = ['r', 'g', 'b', 'a']
        
class HMultiColorVertex2D:
    size = 6 * sizeof(GLfloat)
    posOffset = 0
    colorOffset = 2 * sizeof(GLfloat)
    
    def __init__(self):
        self.pos = HVertexPos2D()
        self.rgba = HColorRGBA()
        
    def __add__(self, other):
        if isinstance(other, HMultiColorVertex2D):
            return self.pos + self.rgba + other.pos + other.rgba
        elif isinstance(other, bytes):
            return self.pos + self.rgba + other
            
    def __radd__(self, other):
        if isinstance(other, HMultiColorVertex2D):
            return other.pos + other.rgba + self.pos + self.rgba
        elif isinstance(other, bytes):
            return other + self.pos + self.rgba
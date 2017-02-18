from OpenGL.GL import GLfloat, sizeof
from struct import pack
        
class HVertexPos2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def bytes(self):
        return pack('ff', self.x, self.y)

    @property
    def size(self):
        return 2 * sizeof(GLfloat)
        
    def __add__(self, other):
        if isinstance(other, HVertexPos2D):
            return self.bytes + other.bytes
        elif isinstance(other, bytes):
            return self.bytes + other
            
    def __radd__(self, other):
        if isinstance(other, HVertexPos2D):
            return other.bytes + self.bytes
        elif isinstance(other, bytes):
            return other + self.bytes
from OpenGL.GL import GLfloat, sizeof
from struct import pack

class HFRect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def tobytes(self):
        return pack('ffff', self.x, self.y, self.w, self.h)
        
    @property
    def size(self):
        return 4 * sizeof(GLfloat)
        
class HVertexPos2D:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def tobytes(self):
        return pack('ff', self.x, self.y)

    @property
    def size(self):
        return 2 * sizeof(GLfloat)
        
class HTexCoord:
    def __init__(self, s=0, t=0):
        self.s = s
        self.t = t
        
    def tobytes(self):
        return pack('ff', self.s, self.t)
        
    @property
    def size(self):
        return 2 * sizeof(GLfloat)
        
class HVertexData2D:
    def __init__(self):
        self.position = HVertexPos2D()
        self.texCoord = HTexCoord()
        
    def tobytes(self):
        return self.position.tobytes() + self.texCoord.tobytes()
        
    @property
    def size(self):
        return self.position.size + self.texCoord.size
        
    @property
    def posOffset(self):
        return 0
        
    @property
    def texOffset(self):
        return self.position.size
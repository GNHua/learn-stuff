from HVertexPos2D import HVertexPos2D
from HTexCoord import HTexCoord

class HVertexData2D:
    def __init__(self):
        self.position = HVertexPos2D()
        self.texCoord = HTexCoord()
        
    def tostring(self):
        return self.position.tostring() + self.texCoord.tostring()
        
    def size(self):
        return self.position.size() + self.texCoord.size()
        
    def posOffset(self):
        return 0
        
    def texOffset(self):
        return self.position.size()
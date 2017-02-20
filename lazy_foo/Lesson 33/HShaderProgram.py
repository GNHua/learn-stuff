from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from OpenGL.GL import shaders

class HShaderProgram:
    def __init__(self):
        self.mProgramID = None
        
    def __del__(self):
        self.freeProgram()
        
    def freeProgram(self):
        glDeleteProgram( self.mProgramID )
        
    def bind(self):
        # Use shader
        glUseProgram( self.mProgramID )
        
        error = glGetError()
        if error != GL_NO_ERROR:
            print('Error binding shader!')
            self.printProgramLog( self.mProgramID )
            return False
            
        return True
        
    def unbind(self):
        glUseProgram( None )
        
class HMultiColorPolygonProgram2D(HShaderProgram):
    def __init__(self):
        super().__init__()
        self.mVertexPos2DLocation = None
        self.mMultiColorLocation = None
        self.mProjectionMatrix = None
        self.mProjectionMatrixLocation = None
        self.mModelViewMatrix = None
        self.mModelViewMatrixLocation = None
        
    def loadProgram(self):        
        vertShaderSource = open('HMultiColorPolygonProgram2D.glvs', 'r').read()
        vertexShader = shaders.compileShader(vertShaderSource, GL_VERTEX_SHADER)
        fragShaderSource = open('HMultiColorPolygonProgram2D.glfs', 'r').read()
        fragexShader = shaders.compileShader(fragShaderSource, GL_FRAGMENT_SHADER)
        self.mProgramID = shaders.compileProgram(vertexShader, fragexShader)
        
        # Get variable location
        self.mVertexPos2DLocation = glGetAttribLocation(self.mProgramID, "HVertexPos2D")
        if self.mVertexPos2DLocation == -1:
            print("%s is not a valid glsl program variable!" % "HVertexPos2D")
        self.mMultiColorLocation = glGetAttribLocation(self.mProgramID, "HMultiColor")
        if self.mMultiColorLocation == -1:
            print("%s is not a valid glsl program variable!" % "HMultiColor")
        self.mProjectionMatrixLocation = glGetUniformLocation(self.mProgramID, "HProjectionMatrix")
        if self.mProjectionMatrixLocation == -1:
            print("%s is not a valid glsl program variable!" % "HProjectionMatrix")
        self.mModelViewMatrixLocation = glGetUniformLocation(self.mProgramID, "HModelViewMatrix")
        if self.mModelViewMatrixLocation == -1:
            print("%s is not a valid glsl program variable!" % "HModelViewMatrix")
            
        return True
        
    def setVertexPointer(self, stride, data):
        glVertexAttribPointer(self.mVertexPos2DLocation, 2, GL_FLOAT, GL_FALSE, stride, data)
        
    def setColorPointer(self, stride, data):
        glVertexAttribPointer(self.mMultiColorLocation, 4, GL_FLOAT, GL_FALSE, stride, data)
        
    def enableVertexPointer(self):
    	glEnableVertexAttribArray(self.mVertexPos2DLocation)

    def disableVertexPointer(self):
    	glDisableVertexAttribArray(self.mVertexPos2DLocation)

    def enableColorPointer(self):
    	glEnableVertexAttribArray(self.mMultiColorLocation)

    def disableColorPointer(self):
    	glDisableVertexAttribArray(self.mMultiColorLocation)
        
    def setProjection(self, matrix):
        self.mProjectionMatrix = matrix
        
    def setModelView(self, matrix):
        self.mModelViewMatrix = matrix
        
    def leftMultProjection(self, matrix):
        self.mProjectionMatrix = np.dot(matrix, self.mProjectionMatrix)
        
    def leftMultModelView(self, matrix):
        self.mModelViewMatrix = np.dot(matrix, self.mModelViewMatrix)
        
    def updateProjection(self):
        glUniformMatrix4fv(self.mProjectionMatrixLocation, 1, GL_FALSE, self.mProjectionMatrix)
        
    def updateModelView(self):
        glUniformMatrix4fv(self.mModelViewMatrixLocation, 1, GL_FALSE, self.mModelViewMatrix)
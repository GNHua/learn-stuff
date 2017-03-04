from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

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
        
    def printProgramLog(self, program):
        if glIsProgram( program ):
            infoLog = glGetProgramInfoLog( program )
            print(infoLog)
        else:
            print('Name %d is not a program' % program)
            
    def printShaderLog(self, shader):
        if glIsShader(shader):
            infoLog = glGetShaderInfoLog( shader )
            print(infoLog)
        else:
            print('Name %d is not a shader' % shader)
            
    def loadShaderFromFile(self, path, shaderType):
        shaderID = glCreateShader(shaderType)
        try:
            shaderSource = open(path, 'r').read()
        except FileNotFoundError:
            print('Unable to open file %s' % path)
            glDeleteShader(shaderID)
            return None
        glShaderSource(shaderID, shaderSource)
        glCompileShader(shaderID)
        
        if glGetShaderiv(shaderID, GL_COMPILE_STATUS) != GL_TRUE:
            print('Unable to compile shader %d!' % shaderID)
            self.printShaderLog(shaderID)
            glDeleteShader(shaderID)
            shaderID = None
        return shaderID
            
class HPlainPolygonProgram2D(HShaderProgram):
    def __init__(self):
        super().__init__()
        self.mPolygonColorLocation = 0
        
    def loadProgram(self):
        self.mProgramID = glCreateProgram()
        vertexShader = self.loadShaderFromFile('HPlainPolygonProgram2D.vert', GL_VERTEX_SHADER)
        if vertexShader is None:
            glDeleteProgram(self.mProgramID)
            self.mProgramID = None
            return False
        glAttachShader( self.mProgramID, vertexShader )

        fragmentShader = self.loadShaderFromFile('HPlainPolygonProgram2D.frag', GL_FRAGMENT_SHADER)
        if fragmentShader is None:
            glDeleteShader(vertexShader)
            glDeleteProgram(self.mProgramID)
            self.mProgramID = None
            return False
        glAttachShader( self.mProgramID, fragmentShader )

        # Link program
        glLinkProgram( self.mProgramID )

        if glGetProgramiv( self.mProgramID, GL_LINK_STATUS ) != GL_TRUE:
            print('Error linking program %d!' % self.mProgramID)
            self.printProgramLog(self.mProgramID)
            glDeleteShader(vertexShader)
            glDeleteShader(fragmentShader)
            glDeleteProgram(self.mProgramID)
            self.mProgramID = None
            return False

        glDeleteShader(vertexShader)
        glDeleteShader(fragmentShader)
        
        # Get variable location
        self.mPolygonColorLocation = glGetUniformLocation(self.mProgramID, "HPolygonColor")
        if self.mPolygonColorLocation == -1:
            print( "%s is not a valid glsl program variable!" % "HPolygonColor" )
            
        return True
        
    def setColor(self, r, g, b, a):
        glUniform4f(self.mPolygonColorLocation, r, g, b, a)
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
            
class HPlainPolygonProgram2D(HShaderProgram):
    def loadProgram(self):
        # Generate program
        self.mProgramID = glCreateProgram()

        # Create vertex shader
        vertexShader = glCreateShader( GL_VERTEX_SHADER )

        # Get vertex source
        vertexShaderSource = "void main() { gl_Position = gl_Vertex; }"

        # Set vertex source
        glShaderSource( vertexShader, vertexShaderSource )

        # Compile vertex source
        glCompileShader( vertexShader )

        # Check vertex shader for errors
        if glGetShaderiv(vertexShader, GL_COMPILE_STATUS) != GL_TRUE:
            print('Unable to compile vertex shader %d!' % vertexShader)
            self.printShaderLog(vertexShader)
            return False

        # Attach vertex shader to program
        glAttachShader( self.mProgramID, vertexShader )

        # Create fragment shader
        fragmentShader = glCreateShader( GL_FRAGMENT_SHADER )
        fragmentShaderSource = "void main() { gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 ); }"
        glShaderSource( fragmentShader, fragmentShaderSource )
        glCompileShader( fragmentShader )

        if glGetShaderiv(fragmentShader, GL_COMPILE_STATUS) != GL_TRUE:
            print('Unable to compile vertex shader %d!' % fragmentShader)
            self.printShaderLog(fragmentShader)
            return False

        glAttachShader( self.mProgramID, fragmentShader )

        # Link program
        glLinkProgram( self.mProgramID )

        if glGetProgramiv( self.mProgramID, GL_LINK_STATUS ) != GL_TRUE:
            print('Error linking program %d!' % self.mProgramID)
            self.printProgramLog(self.mProgramID)
            return False

        return True
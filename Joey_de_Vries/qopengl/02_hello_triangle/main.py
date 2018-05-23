from PyQt5 import QtGui, QtWidgets
import numpy as np
from ctypes import c_float, c_uint, sizeof

WIDTH = 800
HEIGHT = 600
GLfloat = c_float
GLuint = c_uint


class Window(QtGui.QOpenGLWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make sure to set the Surface Format in `__init__`.
        # Otherwise, it won't work.
        format = QtGui.QSurfaceFormat()
        format.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
        format.setProfile(QtGui.QSurfaceFormat.CoreProfile)
        format.setVersion(4, 1)
        self.setFormat(format)
    
    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.glViewport(0, 0, WIDTH, HEIGHT)
        self.gl.glClearColor(0.2, 0.3, 0.3, 1.)
        
        self.vertices = np.array([[ 0.5,  0.5, 0.],
                                  [ 0.5, -0.5, 0.],
                                  [-0.5, -0.5, 0.],
                                  [-0.5,  0.5, 0.]], dtype=GLfloat)
        self.indices1 = np.array([1, 2, 3], dtype=GLuint)
        self.indices2 = np.array([0, 1, 2], dtype=GLuint)
        
        vertShader = QtGui.QOpenGLShader(QtGui.QOpenGLShader.Vertex)
        vertShader.compileSourceFile('triangle.vert')
        vertShader = QtGui.QOpenGLShader(QtGui.QOpenGLShader.Fragment)
        vertShader.compileSourceFile('triangle.frag')
        
        ########################################################
        # Create a shader program
        self.shaderProg = QtGui.QOpenGLShaderProgram()
        self.shaderProg.create()
        self.shaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Vertex, 'triangle.vert')
        self.shaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Fragment, 'triangle.frag')
        self.shaderProg.link()
        ########################################################
        
        ########################################################
        # create a Vertex Array Object with vertice information
        self.VAO1 = QtGui.QOpenGLVertexArrayObject()
        self.VAO1.create()
        self.VAO1.bind()
        
        VBO = QtGui.QOpenGLBuffer(QtGui.QOpenGLBuffer.VertexBuffer)
        VBO.create()
        VBO.setUsagePattern(QtGui.QOpenGLBuffer.StaticDraw)
        data = self.vertices.tostring()
        VBO.bind()
        VBO.allocate(data, len(data))
        self.gl.glVertexAttribPointer(0, 3, self.gl.GL_FLOAT, 
            self.gl.GL_FALSE, 3*sizeof(GLfloat), 0)
        self.gl.glEnableVertexAttribArray(0)
        
        EBO = QtGui.QOpenGLBuffer(QtGui.QOpenGLBuffer.IndexBuffer)
        EBO.create()
        EBO.setUsagePattern(QtGui.QOpenGLBuffer.StaticDraw)
        data = self.indices1.tostring()
        EBO.bind()
        EBO.allocate(data, len(data))
        
        VBO.release()
        self.VAO1.release()
        ########################################################
        
        ########################################################
        # create another Vertex Array Object
        self.VAO2 = QtGui.QOpenGLVertexArrayObject()
        self.VAO2.create()
        self.VAO2.bind()
        
        VBO = QtGui.QOpenGLBuffer(QtGui.QOpenGLBuffer.VertexBuffer)
        VBO.create()
        VBO.setUsagePattern(QtGui.QOpenGLBuffer.StaticDraw)
        data = self.vertices.tostring()
        VBO.bind()
        VBO.allocate(data, len(data))
        self.gl.glVertexAttribPointer(0, 3, self.gl.GL_FLOAT, 
            self.gl.GL_FALSE, 3*sizeof(GLfloat), 0)
        self.gl.glEnableVertexAttribArray(0)
        
        EBO = QtGui.QOpenGLBuffer(QtGui.QOpenGLBuffer.IndexBuffer)
        EBO.create()
        EBO.setUsagePattern(QtGui.QOpenGLBuffer.StaticDraw)
        data = self.indices2.tostring()
        EBO.bind()
        EBO.allocate(data, len(data))
        
        VBO.release()
        self.VAO2.release()
        ########################################################
        
    def paintGL(self):
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT)
        self.shaderProg.bind()
        self.VAO1.bind()
        self.gl.glDrawElements(self.gl.GL_TRIANGLES, 3, 
            self.gl.GL_UNSIGNED_INT, None)
        self.VAO2.bind()
        self.gl.glDrawElements(self.gl.GL_TRIANGLES, 3,
            self.gl.GL_UNSIGNED_INT, None)
        self.VAO2.release()


if __name__ == '__main__':
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    
    window = Window()
    window.resize(640, 400)
    window.show()
    
    sys.exit(app.exec_())

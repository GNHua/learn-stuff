from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np
from ctypes import c_float, c_uint, sizeof

GLfloat = c_float
GLuint = c_uint

WIDTH = 800
HEIGHT = 600


class Window(QtGui.QOpenGLWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setTitle('LearnOpenGL')
        
                                    # Positions       # Colors         # Texture Coords
        self.vertices = np.array([[ 1.0,  1.0, 0.0,   1.0, 0.0, 0.0,   1.0, 1.0],   # Top Right
                                  [ 1.0, -1.0, 0.0,   0.0, 1.0, 0.0,   1.0, 0.0],   # Bottom Right
                                  [-1.0, -1.0, 0.0,   0.0, 0.0, 1.0,   0.0, 0.0],   # Bottom Left
                                  [-1.0,  1.0, 0.0,   1.0, 1.0, 0.0,   0.0, 1.0]],  # Top Left 
                                  dtype=GLfloat)
        self.indices = np.array([[0, 1, 3],
                                 [1, 2, 3]], dtype=GLuint)
        
    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.glViewport(0, 0, WIDTH, HEIGHT)
        self.gl.glClearColor(0.2, 0.3, 0.3, 1.)
        
        ########################################################
        # Create a shader program
        
        self.shaderProg = QtGui.QOpenGLShaderProgram()
        self.shaderProg.create()
        self.shaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Vertex, 'texture.vert')
        self.shaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Fragment, 'texture.frag')
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
            self.gl.GL_FALSE, 8*sizeof(GLfloat), 0)
        self.gl.glEnableVertexAttribArray(0)
        self.gl.glVertexAttribPointer(1, 3, self.gl.GL_FLOAT, 
            self.gl.GL_FALSE, 8*sizeof(GLfloat), 3*sizeof(GLfloat))
        self.gl.glEnableVertexAttribArray(1)
        self.gl.glVertexAttribPointer(2, 2, self.gl.GL_FLOAT, 
            self.gl.GL_FALSE, 8*sizeof(GLfloat), 6*sizeof(GLfloat))
        self.gl.glEnableVertexAttribArray(2)
        
        EBO = QtGui.QOpenGLBuffer(QtGui.QOpenGLBuffer.IndexBuffer)
        EBO.create()
        EBO.setUsagePattern(QtGui.QOpenGLBuffer.StaticDraw)
        data = self.indices.tostring()
        EBO.bind()
        EBO.allocate(data, len(data))
        
        VBO.release()
        self.VAO1.release()
        ########################################################
        
        ########################################################
        # creates a texture
        
        im1 = QtGui.QImage('../images/awesomeface.png').mirrored()
        self.texture1 = QtGui.QOpenGLTexture(im1)
        self.texture1.create()
        self.texture1.setMinMagFilters(QtGui.QOpenGLTexture.Linear,
                                       QtGui.QOpenGLTexture.Linear)
        self.texture1.setWrapMode(QtGui.QOpenGLTexture.Repeat)
        ########################################################
        
        ########################################################
        # creates a texture
        
        im2 = QtGui.QImage('../images/container.jpg')
        self.texture2 = QtGui.QOpenGLTexture(im2)
        self.texture2.create()
        self.texture2.setMinMagFilters(QtGui.QOpenGLTexture.Linear,
                                       QtGui.QOpenGLTexture.Linear)
        self.texture2.setWrapMode(QtGui.QOpenGLTexture.Repeat)
        ########################################################
        
    def paintGL(self):
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT)
        self.shaderProg.bind()
        self.VAO1.bind()
        self.gl.glActiveTexture(self.gl.GL_TEXTURE0)
        self.texture1.bind()
        self.gl.glActiveTexture(self.gl.GL_TEXTURE1)
        self.texture2.bind()
        self.shaderProg.setUniformValue("ourTexture1", 0)
        self.shaderProg.setUniformValue("ourTexture2", 1)
        
        self.gl.glDrawElements(self.gl.GL_TRIANGLES, 6,
            self.gl.GL_UNSIGNED_INT, None)
        self.VAO1.release()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            sys.exit()
        event.accept()


if __name__ == '__main__':
    import sys
    
    # Set format here, otherwise it throws error
    # `QCocoaGLContext: Falling back to unshared context.`
    # on Mac when use QOpenGLWidgets
    # https://doc.qt.io/qt-5/qopenglwidget.html#details last paragraph
    format = QtGui.QSurfaceFormat()
    format.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
    format.setProfile(QtGui.QSurfaceFormat.CoreProfile)
    format.setVersion(4, 1)
    QtGui.QSurfaceFormat.setDefaultFormat(format)
    
    app = QtWidgets.QApplication(sys.argv)
    
    window = Window()
    window.resize(640, 400)
    window.show()
    
    sys.exit(app.exec_())

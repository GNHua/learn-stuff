from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np
from ctypes import c_float, c_uint, sizeof
import time
import math

GLfloat = c_float
GLuint = c_uint

WIDTH = 800
HEIGHT = 600


class Window(QtGui.QOpenGLWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setTitle('LearnOpenGL')
        
        self.vertices = np.array(
           [[-0.5, -0.5, -0.5,  0.0, 0.0],
            [ 0.5, -0.5, -0.5,  1.0, 0.0],
            [ 0.5,  0.5, -0.5,  1.0, 1.0],
            [ 0.5,  0.5, -0.5,  1.0, 1.0],
            [-0.5,  0.5, -0.5,  0.0, 1.0],
            [-0.5, -0.5, -0.5,  0.0, 0.0],

            [-0.5, -0.5,  0.5,  0.0, 0.0],
            [ 0.5, -0.5,  0.5,  1.0, 0.0],
            [ 0.5,  0.5,  0.5,  1.0, 1.0],
            [ 0.5,  0.5,  0.5,  1.0, 1.0],
            [-0.5,  0.5,  0.5,  0.0, 1.0],
            [-0.5, -0.5,  0.5,  0.0, 0.0],

            [-0.5,  0.5,  0.5,  1.0, 0.0],
            [-0.5,  0.5, -0.5,  1.0, 1.0],
            [-0.5, -0.5, -0.5,  0.0, 1.0],
            [-0.5, -0.5, -0.5,  0.0, 1.0],
            [-0.5, -0.5,  0.5,  0.0, 0.0],
            [-0.5,  0.5,  0.5,  1.0, 0.0],

            [ 0.5,  0.5,  0.5,  1.0, 0.0],
            [ 0.5,  0.5, -0.5,  1.0, 1.0],
            [ 0.5, -0.5, -0.5,  0.0, 1.0],
            [ 0.5, -0.5, -0.5,  0.0, 1.0],
            [ 0.5, -0.5,  0.5,  0.0, 0.0],
            [ 0.5,  0.5,  0.5,  1.0, 0.0],

            [-0.5, -0.5, -0.5,  0.0, 1.0],
            [ 0.5, -0.5, -0.5,  1.0, 1.0],
            [ 0.5, -0.5,  0.5,  1.0, 0.0],
            [ 0.5, -0.5,  0.5,  1.0, 0.0],
            [-0.5, -0.5,  0.5,  0.0, 0.0],
            [-0.5, -0.5, -0.5,  0.0, 1.0],

            [-0.5,  0.5, -0.5,  0.0, 1.0],
            [ 0.5,  0.5, -0.5,  1.0, 1.0],
            [ 0.5,  0.5,  0.5,  1.0, 0.0],
            [ 0.5,  0.5,  0.5,  1.0, 0.0],
            [-0.5,  0.5,  0.5,  0.0, 0.0],
            [-0.5,  0.5, -0.5,  0.0, 1.0]], dtype=GLfloat
        )
        self.cubePositions = np.array(
           [[ 0.0,  0.0,  0.0],
            [ 2.0,  5.0, -15.0],
            [-1.5, -2.2, -2.5],
            [-3.8, -2.0, -12.3],
            [ 2.4, -0.4, -3.5],
            [-1.7,  3.0, -7.5],
            [ 1.3, -2.0, -2.5],
            [ 1.5,  2.0, -2.5],
            [ 1.5,  0.2, -1.5],
            [-1.3,  1.0, -1.5]], dtype=GLfloat
        )
        
    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.glViewport(0, 0, WIDTH, HEIGHT)
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glClearColor(0.2, 0.3, 0.3, 1.)
        
        ########################################################
        # Create a shader program
        
        self.shaderProg = QtGui.QOpenGLShaderProgram()
        self.shaderProg.create()
        self.shaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Vertex, 'camera.vert')
        self.shaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Fragment, 'camera.frag')
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
            self.gl.GL_FALSE, 5*sizeof(GLfloat), 0)
        self.gl.glEnableVertexAttribArray(0)
        self.gl.glVertexAttribPointer(1, 2, self.gl.GL_FLOAT, 
            self.gl.GL_FALSE, 5*sizeof(GLfloat), 3*sizeof(GLfloat))
        self.gl.glEnableVertexAttribArray(1)
        
        VBO.release()
        self.VAO1.release()
        ########################################################
        
        ########################################################
        # creates a texture
        
        im1 = QtGui.QImage('../../images/container.jpg')
        self.texture1 = QtGui.QOpenGLTexture(im1)
        self.texture1.create()
        self.texture1.setMinMagFilters(QtGui.QOpenGLTexture.Linear,
                                       QtGui.QOpenGLTexture.Linear)
        self.texture1.setWrapMode(QtGui.QOpenGLTexture.Repeat)
        ########################################################
        
        ########################################################
        # creates a texture
        
        im2 = QtGui.QImage('../../images/awesomeface.png').mirrored()
        self.texture2 = QtGui.QOpenGLTexture(im2)
        self.texture2.create()
        self.texture2.setMinMagFilters(QtGui.QOpenGLTexture.Linear,
                                       QtGui.QOpenGLTexture.Linear)
        self.texture2.setWrapMode(QtGui.QOpenGLTexture.Repeat)
        ########################################################
        
        self.startTime = time.time()
        
    def paintGL(self):
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT | \
                        self.gl.GL_DEPTH_BUFFER_BIT)
        self.shaderProg.bind()
        self.VAO1.bind()
        self.gl.glActiveTexture(self.gl.GL_TEXTURE0)
        self.texture1.bind()
        self.gl.glActiveTexture(self.gl.GL_TEXTURE1)
        self.texture2.bind()
        self.shaderProg.setUniformValue('texture1', 0)
        self.shaderProg.setUniformValue('texture2', 1)
        
        t = time.time() - self.startTime
        view = QtGui.QMatrix4x4()
        radius = 10.
        camX = math.sin(t) * radius
        camZ = math.cos(t) * radius
        view.lookAt(QtGui.QVector3D(camX, 0.0, camZ), 
                    QtGui.QVector3D( 0.0, 0.0,  0.0), 
                    QtGui.QVector3D( 0.0, 1.0,  0.0))
        self.shaderProg.setUniformValue('view', view)
        
        projection = QtGui.QMatrix4x4()
        projection.perspective(45., WIDTH/HEIGHT, 0.1, 100.)
        self.shaderProg.setUniformValue('projection', projection)
        
        for i in range(10):
            model = QtGui.QMatrix4x4()
            model.translate(*self.cubePositions[i])
            angle = 20 * i
            temp = QtGui.QMatrix4x4()
            temp.rotate(angle, 1., 0.3, 0.5)
            model *= temp
            self.shaderProg.setUniformValue('model', model)
            self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 36)
            
        self.VAO1.release()
        self.update()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            sys.exit()
        event.accept()
        
    def closeEvent(self, event):
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
    format.setDepthBufferSize(24)
    QtGui.QSurfaceFormat.setDefaultFormat(format)
    
    app = QtWidgets.QApplication(sys.argv)
    
    window = Window()
    window.resize(WIDTH, HEIGHT)
    window.show()
    
    sys.exit(app.exec_())

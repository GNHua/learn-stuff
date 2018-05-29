from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np
from ctypes import c_float, c_uint, sizeof
import time

from camera import CameraMovement, Camera

GLfloat = c_float
GLuint = c_uint

WIDTH = 800
HEIGHT = 600

# camera
camera = Camera(position = QtGui.QVector3D(0., 0., 3.), 
                up       = QtGui.QVector3D(0., 1., 0.))

firstMouse = True
lastX =  WIDTH / 2.0
lastY =  HEIGHT / 2.0

# timing
dateTime = 0. # time between current frame and last frame
lastFrame = 0.

lightPos = QtGui.QVector3D(12., 20., -2.)

class Window(QtGui.QOpenGLWindow):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.setTitle('LearnOpenGL')
        
        self.vertices = np.array(
           [[-0.5, -0.5, -0.5,  0.0,  0.0, -1.0],
            [ 0.5, -0.5, -0.5,  0.0,  0.0, -1.0],
            [ 0.5,  0.5, -0.5,  0.0,  0.0, -1.0],
            [ 0.5,  0.5, -0.5,  0.0,  0.0, -1.0],
            [-0.5,  0.5, -0.5,  0.0,  0.0, -1.0],
            [-0.5, -0.5, -0.5,  0.0,  0.0, -1.0],

            [-0.5, -0.5,  0.5,  0.0,  0.0,  1.0],
            [ 0.5, -0.5,  0.5,  0.0,  0.0,  1.0],
            [ 0.5,  0.5,  0.5,  0.0,  0.0,  1.0],
            [ 0.5,  0.5,  0.5,  0.0,  0.0,  1.0],
            [-0.5,  0.5,  0.5,  0.0,  0.0,  1.0],
            [-0.5, -0.5,  0.5,  0.0,  0.0,  1.0],

            [-0.5,  0.5,  0.5, -1.0,  0.0,  0.0],
            [-0.5,  0.5, -0.5, -1.0,  0.0,  0.0],
            [-0.5, -0.5, -0.5, -1.0,  0.0,  0.0],
            [-0.5, -0.5, -0.5, -1.0,  0.0,  0.0],
            [-0.5, -0.5,  0.5, -1.0,  0.0,  0.0],
            [-0.5,  0.5,  0.5, -1.0,  0.0,  0.0],

            [ 0.5,  0.5,  0.5,  1.0,  0.0,  0.0],
            [ 0.5,  0.5, -0.5,  1.0,  0.0,  0.0],
            [ 0.5, -0.5, -0.5,  1.0,  0.0,  0.0],
            [ 0.5, -0.5, -0.5,  1.0,  0.0,  0.0],
            [ 0.5, -0.5,  0.5,  1.0,  0.0,  0.0],
            [ 0.5,  0.5,  0.5,  1.0,  0.0,  0.0],

            [-0.5, -0.5, -0.5,  0.0, -1.0,  0.0],
            [ 0.5, -0.5, -0.5,  0.0, -1.0,  0.0],
            [ 0.5, -0.5,  0.5,  0.0, -1.0,  0.0],
            [ 0.5, -0.5,  0.5,  0.0, -1.0,  0.0],
            [-0.5, -0.5,  0.5,  0.0, -1.0,  0.0],
            [-0.5, -0.5, -0.5,  0.0, -1.0,  0.0],

            [-0.5,  0.5, -0.5,  0.0,  1.0,  0.0],
            [ 0.5,  0.5, -0.5,  0.0,  1.0,  0.0],
            [ 0.5,  0.5,  0.5,  0.0,  1.0,  0.0],
            [ 0.5,  0.5,  0.5,  0.0,  1.0,  0.0],
            [-0.5,  0.5,  0.5,  0.0,  1.0,  0.0],
            [-0.5,  0.5, -0.5,  0.0,  1.0,  0.0]], dtype=GLfloat
        )
        
    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.glViewport(0, 0, WIDTH, HEIGHT)
        self.gl.glEnable(self.gl.GL_DEPTH_TEST)
        self.gl.glClearColor(0.1, 0.1, 0.1, 1.)
        
        ########################################################
        # Create a shader program
        
        self.lightingShaderProg = QtGui.QOpenGLShaderProgram()
        self.lightingShaderProg.create()
        self.lightingShaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Vertex, '2.1.basic_lighting.vert')
        self.lightingShaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Fragment, '2.1.basic_lighting.frag')
        self.lightingShaderProg.link()
        ########################################################
        
        ########################################################
        # Create a shader program
        
        self.lampShaderProg = QtGui.QOpenGLShaderProgram()
        self.lampShaderProg.create()
        self.lampShaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Vertex, '2.1.lamp.vert')
        self.lampShaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Fragment, '2.1.lamp.frag')
        self.lampShaderProg.link()
        ########################################################
        
        
        ########################################################
        # create a Vertex Array Object with vertice information
        
        self.cubeVAO = QtGui.QOpenGLVertexArrayObject()
        self.cubeVAO.create()
        self.cubeVAO.bind()
        
        VBO = QtGui.QOpenGLBuffer(QtGui.QOpenGLBuffer.VertexBuffer)
        VBO.create()
        VBO.setUsagePattern(QtGui.QOpenGLBuffer.StaticDraw)
        data = self.vertices.tostring()
        VBO.bind()
        VBO.allocate(data, len(data))
        self.gl.glVertexAttribPointer(0, 3, self.gl.GL_FLOAT, 
            self.gl.GL_FALSE, 6*sizeof(GLfloat), 0)
        self.gl.glEnableVertexAttribArray(0)
        self.gl.glVertexAttribPointer(1, 3, self.gl.GL_FLOAT, 
            self.gl.GL_FALSE, 6*sizeof(GLfloat), 0)
        self.gl.glEnableVertexAttribArray(1)
        
        VBO.release()
        self.cubeVAO.release()
        ########################################################
        
        ########################################################
        # create a Vertex Array Object with vertice information
        
        self.lightVAO = QtGui.QOpenGLVertexArrayObject()
        self.lightVAO.create()
        self.lightVAO.bind()
        
        VBO.bind()
        self.gl.glVertexAttribPointer(0, 3, self.gl.GL_FLOAT, 
            self.gl.GL_FALSE, 6*sizeof(GLfloat), 0)
        self.gl.glEnableVertexAttribArray(0)
        
        VBO.release()
        self.lightVAO.release()
        ########################################################
        
    def paintGL(self):
        currentFrame = time.time()
        global deltaTime, lastFrame
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame
        
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT | \
                        self.gl.GL_DEPTH_BUFFER_BIT)
                        
        self.lightingShaderProg.bind()
        self.lightingShaderProg.setUniformValue('objectColor', 1., 0.5, 0.31)
        self.lightingShaderProg.setUniformValue('lightColor', 1., 1., 1.)
        self.lightingShaderProg.setUniformValue('lightPos', lightPos)
        projection = QtGui.QMatrix4x4()
        projection.perspective(camera.zoom, WIDTH/HEIGHT, 0.1, 100.)
        self.lightingShaderProg.setUniformValue('projection', projection)
        self.lightingShaderProg.setUniformValue('view', camera.viewMatrix)
        self.lightingShaderProg.setUniformValue('model', QtGui.QMatrix4x4())

        self.cubeVAO.bind()
        self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 36)
        
        self.lampShaderProg.bind()
        self.lampShaderProg.setUniformValue('projection', projection)
        self.lampShaderProg.setUniformValue('view', camera.viewMatrix)
        model = QtGui.QMatrix4x4()
        model.translate(lightPos)
        model.scale(0.2)
        self.lampShaderProg.setUniformValue('model', model)

        self.lightVAO.bind()
        self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 36)
        
        self.update()
        
    def keyPressEvent(self, event):
        global deltaTime
        
        if event.key() == QtCore.Qt.Key_Escape:
            sys.exit()
        elif event.key() == QtCore.Qt.Key_W:
            camera.processKeyboard(CameraMovement.FORWARD, deltaTime)
        elif event.key() == QtCore.Qt.Key_S:
            camera.processKeyboard(CameraMovement.BACKWARD, deltaTime)
        elif event.key() == QtCore.Qt.Key_A:
            camera.processKeyboard(CameraMovement.LEFT, deltaTime)
        elif event.key() == QtCore.Qt.Key_D:
            camera.processKeyboard(CameraMovement.RIGHT, deltaTime)
            
        event.accept()
        
    def mouseMoveEvent(self, event):
        global firstMouse, lastX, lastY
        
        if firstMouse:
            lastX, lastY = event.globalX(), event.globalY()
            firstMouse = False
            
        xoffset = event.globalX() - lastX
        yoffset = lastY - event.globalY()
        lastX, lastY = event.globalX(), event.globalY()
        
        camera.processMouseMovement(xoffset, yoffset)
        event.accept()
        
    def wheelEvent(self, event):
        camera.processMouseScroll(event.angleDelta().y())
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

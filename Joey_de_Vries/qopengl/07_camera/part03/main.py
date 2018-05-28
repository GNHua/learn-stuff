from PyQt5 import QtGui, QtCore, QtWidgets
import numpy as np
from ctypes import c_float, c_uint, sizeof
import time
import math

GLfloat = c_float
GLuint = c_uint

WIDTH = 800
HEIGHT = 600

# camera
cameraPos   = QtGui.QVector3D(0.0, 0.0,  3.0)
cameraFront = QtGui.QVector3D(0.0, 0.0, -1.0)
cameraUp    = QtGui.QVector3D(0.0, 1.0,  0.0)

firstMouse = True
yaw   = -90.0	# yaw is initialized to -90.0 degrees since a yaw of 0.0 results in a direction vector pointing to the right so we initially rotate a bit to the left.
pitch =  0.0
lastX =  800.0 / 2.0
lastY =  600.0 / 2.0
fov   =  45.0

# timing
dateTime = 0. # time between current frame and last frame
lastFrame = 0.

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
            QtGui.QOpenGLShader.Vertex, '7.3.camera.vert')
        self.shaderProg.addShaderFromSourceFile(
            QtGui.QOpenGLShader.Fragment, '7.3.camera.frag')
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
        
        currentFrame = time.time()
        global deltaTime, lastFrame
        deltaTime = currentFrame - lastFrame
        lastFrame = currentFrame
        
        view = QtGui.QMatrix4x4()
        view.lookAt(cameraPos, cameraPos+cameraFront, cameraUp)
        self.shaderProg.setUniformValue('view', view)
        
        projection = QtGui.QMatrix4x4()
        projection.perspective(fov, WIDTH/HEIGHT, 0.1, 100.)
        self.shaderProg.setUniformValue('projection', projection)
        
        for i in range(10):
            model = QtGui.QMatrix4x4()
            model.translate(*self.cubePositions[i])
            angle = 20. * i
            temp = QtGui.QMatrix4x4()
            temp.rotate(angle, 1., 0.3, 0.5)
            model *= temp
            self.shaderProg.setUniformValue('model', model)
            self.gl.glDrawArrays(self.gl.GL_TRIANGLES, 0, 36)
            
        self.VAO1.release()
        self.update()
        
    def keyPressEvent(self, event):
        global cameraPos, cameraFront, cameraUp, deltaTime
        cameraSpeed = 2.5 * deltaTime
        
        if event.key() == QtCore.Qt.Key_Escape:
            sys.exit()
        elif event.key() == QtCore.Qt.Key_W:
            cameraPos += cameraSpeed * cameraFront
        elif event.key() == QtCore.Qt.Key_S:
            cameraPos -= cameraSpeed * cameraFront
        elif event.key() == QtCore.Qt.Key_A:
            temp = QtGui.QVector3D.crossProduct(cameraFront, cameraUp).normalized()
            cameraPos -= temp * cameraSpeed
        elif event.key() == QtCore.Qt.Key_D:
            temp = QtGui.QVector3D.crossProduct(cameraFront, cameraUp).normalized()
            cameraPos += temp * cameraSpeed
            
        event.accept()
        
    def mouseMoveEvent(self, event):
        global firstMouse, yaw, pitch, lastX, lastY, cameraFront
        
        if firstMouse:
            lastX, lastY = event.globalX(), event.globalY()
            firstMouse = False
            
        xoffset = event.globalX() - lastX
        yoffset = lastY - event.globalY()
        lastX, lastY = event.globalX(), event.globalY()
        
        sensitivity = 0.1
        xoffset *= sensitivity
        yoffset *= sensitivity
        
        yaw += xoffset
        pitch += yoffset
        
        if pitch > 89.:
            pitch = 89.
        if pitch < -89.:
            pitch = -89.
            
        front = QtGui.QVector3D(
            math.cos(math.radians(yaw)) * math.cos(math.radians(pitch)), 
            math.sin(math.radians(pitch)),
            math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
        )
        cameraFront = front.normalized()
        
        event.accept()
        
    def wheelEvent(self, event):
        global fov
        
        if fov >= 1. and fov <= 45.:
            fov -= event.angleDelta().y()
        elif fov < 1.:
            fov = 1.
        elif fov > 45.:
            fov = 45.
            
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

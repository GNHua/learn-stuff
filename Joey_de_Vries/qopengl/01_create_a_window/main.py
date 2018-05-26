from PyQt5 import QtGui, QtCore, QtWidgets

WIDTH = 800
HEIGHT = 600


class Window(QtGui.QOpenGLWindow):
    
    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.glViewport(0, 0, WIDTH, HEIGHT)
        self.gl.glClearColor(0.2, 0.3, 0.3, 1.)
        
    def paintGL(self):
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT)
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            sys.exit()
        event.accept()


if __name__ == '__main__':
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    
    # Set format here, otherwise it throws error
    # `QCocoaGLContext: Falling back to unshared context.`
    # when use QOpenGLWidgets
    format = QtGui.QSurfaceFormat()
    format.setRenderableType(QtGui.QSurfaceFormat.OpenGL)
    format.setProfile(QtGui.QSurfaceFormat.CoreProfile)
    format.setVersion(4, 1)
    format.setStencilBufferSize(8)
    QtGui.QSurfaceFormat.setDefaultFormat(format)
    
    window = Window()
    window.resize(640, 400)
    window.show()
    
    sys.exit(app.exec_())

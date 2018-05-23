from PyQt5 import QtGui, QtWidgets

WIDTH = 800
HEIGHT = 600


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
        
    def paintGL(self):
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT)


if __name__ == '__main__':
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    
    window = Window()
    window.resize(640, 400)
    window.show()
    
    sys.exit(app.exec_())

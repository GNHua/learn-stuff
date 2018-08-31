from PyQt5 import QtGui, QtWidgets


class Window(QtGui.QOpenGLWindow):
    
    def initializeGL(self):
        self.gl = self.context().versionFunctions()
        self.gl.glClearColor(0., 0., 0., 1.)
        
    def paintGL(self):
        self.gl.glClear(self.gl.GL_COLOR_BUFFER_BIT)


if __name__ == '__main__':
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    
    window = Window()
    window.resize(640, 400)
    window.show()
    
    sys.exit(app.exec_())
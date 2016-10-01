from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

class GlWin:
    def __init__(self):
        self.i = 1
    
    def initGL(self):    
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
    
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClearColor(0., 0., 0., 1.)
    
        error = glGetError()
        if error != GL_NO_ERROR:
            print('Error initializing OpenGL')
            return False
        return True
    
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT)
    
        glBegin( GL_QUADS )
        glVertex2f( -0.1 * self.i, -0.1 * self.i )
        glVertex2f(  0.1 * self.i, -0.1 * self.i )
        glVertex2f(  0.1 * self.i,  0.1 * self.i )
        glVertex2f( -0.1 * self.i,  0.1 * self.i )
        glEnd()
    
        glutSwapBuffers()
    
    def main(self):
        glutInit(sys.argv)
        glutInitContextVersion(2, 1)
        glutInitDisplayMode(GLUT_DOUBLE)
        glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        # glutFullScreen()
        glutCreateWindow(b'OpenGL')

        if not self.initGL():
            print('Unable to initialize graphics library!')
            return 1
    
        glutDisplayFunc(self.render)
        glutMainLoopEvent()
        
    
if __name__ == '__main__':
    g = GlWin()
    g.main()
    for i in range(5):
        # glutPostRedisplay()
        g.render()
        g.i += 1
        time.sleep(0.5)
    print('before leave main loop')
    glutLeaveMainLoop()
    print('after leave main loop')
    g.i = 9
    
    time.sleep(3)
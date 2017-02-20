from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()
    
def handleKeys(key, x, y):
    pass

def main():
    glutInit(sys.argv)
    glutInitContextVersion(3, 3)
    glutInitDisplayMode( GLUT_DOUBLE )
    glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
    glutCreateWindow(b'OpenGL')
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    glClearColor(0., 0., 0., 1.)
    glutDisplayFunc(render)
    glutKeyboardFunc(handleKeys)
    glutMainLoop()
    return 0
    
if __name__ == '__main__':
    main()
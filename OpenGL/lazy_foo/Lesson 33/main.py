from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import HUtil as H
import sys

def runMainLoop(val):
    H.update()
    H.render()
    glutTimerFunc(int(1000/H.SCREEN_FPS), runMainLoop, val)
    
def main():
    glutInit(sys.argv)
    glutInitContextVersion(3, 1)
    glutInitDisplayMode( GLUT_DOUBLE )
    glutInitWindowSize(H.SCREEN_WIDTH, H.SCREEN_HEIGHT)
    # glutFullScreen()
    glutCreateWindow(b'OpenGL')
    
    if not H.initGL():
        print('Unable to initialize graphics library!')
        return 1
    if not H.loadGP():
        print('Unable to load shader program!')
        return 1
    if not H.loadMedia():
        print('Unable to load media!')
        return 2
        
    glutDisplayFunc(H.render)
    glutTimerFunc(int(1000/H.SCREEN_FPS), runMainLoop, 0)
    glutMainLoop()
    return 0
    
if __name__ == '__main__':
    main()
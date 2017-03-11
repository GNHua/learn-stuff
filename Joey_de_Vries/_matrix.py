import numpy as np

__all__ = ['perspective_matrix']

def perspective_matrix(fov, aspect, near, far):
    '''
    Return the following matrix
    |   fov                                  |
    |  ------   0       0            0       |
    |  aspect                                |
    |                                        |
    |                                        |
    |     0     f       0            0       |
    |                                        |
    |                                        |
    |                Near+Far    2*Near*Far  |
    |     0     0   ----------  ------------ |
    |                Near-Far     Near-Far   |
    |                                        |
    |                                        |
    |     0     0       -1           0       |
    '''
    M = np.identity(4)
    M[0,0] = fov / aspect
    M[1,1] = fov
    M[2,2] = (near + far) / (near - far)
    M[2,3] = 2 * near * far / (near - far)
    M[3,2] = -1
    return M
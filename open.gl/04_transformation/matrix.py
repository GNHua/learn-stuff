import numpy as np
from OpenGL.GL import GLfloat

import transformations as tf


__all__ = ['perspective_matrix']


def perspective_RH(fov, aspect, near, far, dtype=GLfloat):
    '''
    Return the following matrix
    |  cot(fov/2)                               |
    |  ----------       0           0        0  |
    |    aspect                                 |
    |                                           |
    |     0         cot(fov/2)      0        0  |
    |                                           |
    |                                           |
    |                           near+far        |
    |     0             0       --------    -1  |
    |                           near-far        |
    |                                           |
    |                          2*near*far       |
    |     0             0      ----------    0  |
    |                           near-far        |
    '''
    M = np.zeros((4, 4), dtype=dtype)
    
    M[0,0] = 1 / (aspect * np.tan(fov/2))
    M[1,1] = 1/ np.tan(fov/2)
    M[2,2] = (near + far) / (near - far)
    M[2,3] = 2 * near * far / (near - far)
    M[3,2] = -1
    return M


def look_at_RH(eye, center, up, dtype=GLfloat):
    '''
    Vec3 f, s, u
    
    f = normalize(center - eye)
    s = normalize(f × up)
    u = s × f
    
    Return the following matrix
    |   s.x         u.x        -f.x         0  |
    |   s.y         u.y        -f.y         0  |
    |   s.z         u.z        -f.z         0  |
    |  -s • eye    -u • eye     f • eye     1  |
    '''    
    M = np.identity(4, dtype=dtype)
    f = tf.unit_vector( center - up)
    s = tf.unit_vector( np.cross(f, up) )
    u = np.cross( s, f )

    M[:3, 0] = s
    M[:3, 1] = u
    M[:3, 2] = -f
    M[3, 0] = -np.dot(s, eye)
    M[3, 1] = -np.dot(u, eye)
    M[3, 2] =  np.dot(f, eye)
    return M
    

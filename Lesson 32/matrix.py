import numpy as np
from OpenGL.GL import GLfloat

def make_ortho_matrix(left, right, bottom, top, near, far):
    return np.array([[2/(right-left),              0,             0, -(right+left)/(right-left)],
                     [             0, 2/(top-bottom),             0, -(top+bottom)/(top-bottom)],
                     [             0,              0, -2/(far-near),     -(far+near)/(far-near)],
                     [             0,              0,             0,                          1]], dtype=GLfloat)
from enum import Enum, auto
from PyQt5.QtGui import QVector3D, QMatrix4x4
import math


class CameraMovement(Enum):
    """Defines several possible options for camera movement. 
    Used as abstraction to stay away from window-system specific 
    input methods.
    """
    FORWARD = auto()
    BACKWARD = auto()
    LEFT = auto()
    RIGHT = auto()


# Default camera values
YAW         = -90.0
PITCH       =   0.0
SPEED       =   2.5
SENSITIVITY =   0.1
ZOOM        =  45.0


class Camera:
    
    def __init__(self, position, up):
        self.position = position
        self.worldUp = up
        self.yaw = YAW
        self.pitch = PITCH
        self.movementSpeed = SPEED
        self.mouseSensitivity = SENSITIVITY
        self.zoom = ZOOM
        self.__updateCameraVectors()
        
    @property
    def viewMatrix(self):
        view = QMatrix4x4()
        view.lookAt(self.position, self.position+self.front, self.up)
        return view
        
    def processKeyboard(self, direction, deltaTime):
        velocity = self.movementSpeed * deltaTime
        if direction == CameraMovement.FORWARD:
            self.position += self.front * velocity
        elif direction == CameraMovement.BACKWARD:
            self.position -= self.front * velocity
        elif direction == CameraMovement.LEFT:
            self.position -= self.right * velocity
        elif direction == CameraMovement.RIGHT:
            self.position += self.right * velocity
            
    def processMouseMovement(self, xoffset, yoffset, constrainPitch=True):
        xoffset *= self.mouseSensitivity
        yoffset *= self.mouseSensitivity
        
        self.yaw   += xoffset
        self.pitch += yoffset
        
        if constrainPitch:
            if self.pitch > 89.:
                self.pitch = 89.
            if self.pitch < -89.:
                self.pitch = -89.
                
        self.__updateCameraVectors()
        
    def processMouseScroll(self, yoffset):
        if self.zoom >= 1. and self.zoom <= 45.:
            self.zoom -= yoffset
        elif self.zoom < 1.:
            self.zoom = 1.
        elif self.zoom > 45.:
            self.zoom = 45.
            
    def __updateCameraVectors(self):
        self.front = QVector3D(
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        )
        self.front.normalize()
        
        self.right = QVector3D.crossProduct(self.front, self.worldUp).normalized()
        self.up    = QVector3D.crossProduct(self.right, self.front).normalized()








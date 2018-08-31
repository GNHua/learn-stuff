import enum
import numpy as np
from OpenGL.GL import GLfloat
import glm
import glm.gtc.matrix_transform as glm_mt



class Camera_Movement(enum.Enum):
    """
    Defines several possible options for camera movement. 
    Used as abstraction to stay away from window-system 
    specific input methods
    """
    FORWARD = enum.auto()
    BACKWARD = enum.auto()
    LEFT = enum.auto()
    RIGHT = enum.auto()


# Default camera values
YAW         = -90.0
PITCH       = 0.
SPEED       = 2.5
SENSITIVTY  = 0.1
ZOOM        = 45.


class Camera:
    """
    An abstract camera class that processes input and calculates 
    the corresponding Eular Angles, Vectors and Matrices for use 
    in OpenGL.
    
    Camera Attributes
        attr::Position
        attr::Front
        attr::Up
        attr::Right
        attr::WorldUp
    Eular Angles
        attr::Yaw
        attr::Pitch
    Camera options
        attr::MovementSpeed
        attr::MouseSensitivity
        attr::Zoom
    """
    def __init__(self, 
                 position=np.array([0,0,0], dtype=GLfloat), 
                 up =np.array([0,1,0], dtype=GLfloat), 
                 yaw = YAW, 
                 pitch = PITCH):
        self.Front = np.array([0,0,-1], dtype=GLfloat)
        self.MovementSpeed = SPEED
        self.MouseSensitivity = SENSITIVTY
        self.Zoom = ZOOM
        self.Position = position
        self.WorldUp = up
        
        self.Yaw = yaw
        self.Pitch = pitch
        self.updateCameraVectors()
        
    def updateCameraVectors(self):
        """
        Calculates the front vector from the Camera's (updated) Eular Angles.
        """
        # Calculate the new Front vector
        x = np.cos(np.radians(self.Yaw)) * np.cos(np.radians(self.Pitch))
        y = np.sin(np.radians(self.Pitch))
        z = np.sin(np.radians(self.Yaw)) * np.cos(np.radians(self.Pitch))
        
        front = np.array([x, y, z], dtype=GLfloat)
        print(front)
        self.Front = front / np.sqrt(x**2 + y**2 + z**2)
        print(self.Front)
        
        temp = np.cross(self.Front, self.WorldUp)
        self.Right = temp / np.sqrt(temp[0]**2 + temp[1]**2 + temp[2]**2)
        print(self.Right)
        
        temp = np.cross(self.Right, self.Front)
        self.Up = temp / np.sqrt(temp[0]**2 + temp[1]**2 + temp[2]**2)
        print(self.Up)
        
        
        
        
        # front = glm.vec3(x, y, z)
        # print('*=========')
        # self.Front = np.array(glm.normalize(front), dtype=GLfloat)
        # print(self.Front)
        # print('#=========')
        #
        # # Also re-calculate the Right and Up vector
        # # Normalize the vectors, because their length gets closer to 0 the more you
        # # look up or down which results in slower movement.
        # print('**=========')
        # temp = np.cross(self.Front, self.WorldUp)
        # print(temp)
        # print('##=========')
        # self.Right = np.array(glm.normalize(glm.vec3(temp)), dtype=GLfloat)
        #
        # print('***=========')
        # temp = np.cross(self.Right, self.Front)
        # print(temp)
        # self.Up = np.array(glm.normalize(glm.vec3(temp)), dtype=GLfloat)
        # print('###=========')
        
    def GetViewMatrix(self):
        """
        Returns the view matrix calculated using Eular Angles and 
        the LookAt Matrix.
        """
        return glm_mt.lookAt(self.Position, self.Position+self.Front, self.Up)
        
    def ProcessKeyBoard(self, direction, deltaTime):
        """
        Processes input received from any keyboard-like input system. 
        Accepts input parameter in the form of camera defined ENUM 
        (to abstract it from windowing systems).
        """
        velocity = self.MovementSpeed * deltaTime
        if direction == Camera_Movement.FORWARD:
            self.Position += self.Front * velocity
        if direction == Camera_Movement.BACKWARD:
            self.Position -= self.Front * velocity
        if direction == Camera_Movement.LEFT:
            self.Position -= self.Right * velocity
        if direction == Camera_Movement.RIGHT:
            self.Position += self.Right * velocity
            
    def ProcessMouseMovement(self, xoffset, yoffset, constrainPitch=True):
        """
        Processes input received from a mouse input system. Expects 
        the offset value in both the x and y direction.
        """
        xoffset *= self.MouseSensitivity
        yoffset *= self.MouseSensitivity
        
        self.Yaw   += xoffset
        self.Pitch += yoffset
        
        # Make sure that when pitch is out of bounds, screen doesn't get flipped
        if constrainPitch:
            if self.Pitch > 89.0:
                self.Pitch = 89.0
            if self.Pitch < -89.0:
                self.Pitch = -89.0
        
        # Update Front, Right and Up Vectors using the updated Eular angles
        self.updateCameraVectors()
        
    def ProcessMouseScroll(self, yoffset):
        """
        Processes input received from a mouse scroll-wheel event. 
        Only requires input on the vertical wheel-axis.
        """
        if self.Zoom >= 1.0 and self.Zoom <= 45.0:
            self.Zoom -= yoffset
        if self.Zoom <= 1.0:
            self.Zoom = 1.0
        if self.Zoom >= 45.0:
            self.Zoom = 45.0




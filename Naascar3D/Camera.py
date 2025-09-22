from Base3DObjects import Point, Vector
from math import *

# The ViewMatrix class holds the camera's coordinate frame and
# set's up a transformation concerning the camera's position
# and orientation


class Camera: # ViewMatrix:
    def __init__(self, shader, projection_matrix, camera_distance = 10.0, camera_height = 5.0, start_direction = Vector(0,0,1)):
        self.eye = Point(0, 0, 0)
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)

        self.shader = shader
        self.projection_matrix = projection_matrix
        self.camera_distance = camera_distance
        self.camera_height = camera_height

        self.follow_dir = start_direction
        self.camera_smoothness = 0.05

    ## MAKE OPERATIONS TO ADD LOOK, SLIDE, PITCH, YAW and ROLL ##
    def look_at(self, eye, center, up):
        self.eye = eye
        self.n = (eye - center)
        self.n.normalize()
        self.u = up.cross(self.n)
        self.u.normalize()
        self.v = self.n.cross(self.u)
        self.v.normalize()
    
    def slide(self, du, dv, dn):
        self.eye = self.eye + self.u * du + self.v * dv + self.n * dn
    
    def pitch(self, angle):
        c = cos(angle)
        s = sin(angle)
        new_v = self.v * c + self.n * s
        new_n = self.n * c - self.v * s
        self.v = new_v
        self.n = new_n
    
    def yaw(self, angle):
        c = cos(angle)
        s = sin(angle)
        new_u = self.u * c - self.n * s
        new_n = self.n * c + self.u * s
        self.u = new_u
        self.n = new_n
    
    def roll(self, angle):
        c = cos(angle)
        s = sin(angle)
        new_u = self.u * c + self.v * s
        new_v = self.v * c - self.u * s
        self.u = new_u
        self.v = new_v

    def rotate_around_point(self, point, angle):
        translated_eye = self.eye - point

        # Perform yaw rotation around the Y-axis
        c = cos(angle)
        s = sin(angle)
        new_x = translated_eye.x * c - translated_eye.z * s
        new_z = translated_eye.z * c + translated_eye.x * s
        rotated_eye = Point(new_x, translated_eye.y, new_z)

        # Translate the eye back to the original point
        self.eye = rotated_eye + point

        # Update the n and u vectors to reflect the rotation
        self.yaw(angle)

    def multiply_matrices(self, m1, m2):
        counter = 0
        new_matrix = [0] * 16
        for row in range(4):
            for col in range(4):
                for i in range(4):
                    new_matrix[counter] += m1[row*4 + i]*m2[col + 4*i]
                counter += 1
        return new_matrix

    def get_matrix(self):
        minusEye = Vector(-self.eye.x, -self.eye.y, -self.eye.z)
        return [self.u.x, self.u.y, self.u.z, minusEye.dot(self.u),
                self.v.x, self.v.y, self.v.z, minusEye.dot(self.v),
                self.n.x, self.n.y, self.n.z, minusEye.dot(self.n),
                0,        0,        0,        1]
    
    def update_pos(self, car_position, car_direction):
        # Position the camera behind and above the vehicle
        t = self.camera_smoothness
        self.follow_dir = Vector(
            self.follow_dir.x + (car_direction.x - self.follow_dir.x) * t,
            self.follow_dir.y + (car_direction.y - self.follow_dir.y) * t,
            self.follow_dir.z + (car_direction.z - self.follow_dir.z) * t
        )
        self.follow_dir.normalize()

        cam_position = Point(
            car_position.x - self.follow_dir.x * self.camera_distance,
            car_position.y + self.camera_height,
            car_position.z - self.follow_dir.z * self.camera_distance
        )
        look_at_position = Point(
            car_position.x + self.follow_dir.x,
            car_position.y,
            car_position.z + self.follow_dir.z
        )
        up_vector = Vector(0, 1, 0)

        self.look_at(cam_position, look_at_position, up_vector)
        self.shader.set_projection_view_matrix(
            self.multiply_matrices(self.projection_matrix.get_matrix(), self.get_matrix()))
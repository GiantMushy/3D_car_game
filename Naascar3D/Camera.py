from Base3DObjects import Point, Vector
from math import *

# The ViewMatrix class holds the camera's coordinate frame and
# set's up a transformation concerning the camera's position
# and orientation


class Camera: # ViewMatrix:
    CAMERA_DISTANCE = 10.0
    CAMERA_HEIGHT = 5.0
    def __init__(self, shader, projection_matrix, start_direction = Vector(0,0,1), start_position = (0,0)):
        self.eye = Point(0, 0, 0)
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)

        self.shader = shader
        self.projection_matrix = projection_matrix
        self.camera_height = self.CAMERA_HEIGHT

        
        # Simplified: keep a base distance and scale distance with speed
        self.base_distance = self.CAMERA_DISTANCE
        self.speed_distance_scale = 0.06    # distance added per unit speed
        self.min_distance = self.CAMERA_DISTANCE * 0.6
        self.max_distance = self.CAMERA_DISTANCE * 1.8

        # Keep mild direction smoothing so it is not too twitchy
        self.follow_dir = start_direction
        self.direction_smoothness = 0.08
        self.distance_smoothness = 0.12   # 0..1, higher = faster catch-up
        self.smoothed_distance = self.base_distance

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
        """ Not currently used, could be cool for special effects and just looking around """
        translated_eye = self.eye - point

        c = cos(angle)
        s = sin(angle)
        new_x = translated_eye.x * c - translated_eye.z * s
        new_z = translated_eye.z * c + translated_eye.x * s
        rotated_eye = Point(new_x, translated_eye.y, new_z)

        self.eye = rotated_eye + point

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
    
    def update_pos(self, car_position, car_direction, car_speed):
        # Position the camera behind and above the vehicle, with smoothing
        t = self.direction_smoothness
        self.follow_dir = Vector(
            self.follow_dir.x + (car_direction.x - self.follow_dir.x) * t,
            self.follow_dir.y + (car_direction.y - self.follow_dir.y) * t,
            self.follow_dir.z + (car_direction.z - self.follow_dir.z) * t
        )
        self.follow_dir.normalize()

        target_dist = self.base_distance + abs(car_speed) * self.speed_distance_scale
        if target_dist < self.min_distance: target_dist = self.min_distance
        if target_dist > self.max_distance: target_dist = self.max_distance

        # Smooth the distance (lag)
        ds = self.distance_smoothness
        self.smoothed_distance += (target_dist - self.smoothed_distance) * ds
        
        d = self.smoothed_distance
        eye = Point(
            car_position.x - self.follow_dir.x * d,
            car_position.y + self.camera_height,
            car_position.z - self.follow_dir.z * d
        )

        # Look slightly ahead of car
        center = Point(
            car_position.x + self.follow_dir.x * 2.0,
            car_position.y,
            car_position.z + self.follow_dir.z * 2.0
        )

        up = Vector(0, 1, 0)
        self.look_at(eye, center, up)

        self.shader.set_projection_view_matrix(
            self.multiply_matrices(self.projection_matrix.get_matrix(), self.get_matrix()))
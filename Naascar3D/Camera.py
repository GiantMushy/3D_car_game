from Base3DObjects import Point, Vector
from math import *

# The ViewMatrix class holds the camera's coordinate frame and
# set's up a transformation concerning the camera's position
# and orientation


class Camera: # ViewMatrix:
    CAMERA_DISTANCE = 10.0
    CAMERA_HEIGHT = 5.0
    def __init__(self, shader, projection_matrix, start_direction = (0,1), start_position = (0,0)):
        self.eye = Point(0, 0, 0)
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)

        self.shader = shader
        self.projection_matrix = projection_matrix
        self.camera_height = self.CAMERA_HEIGHT

        
        # Camera AUTOMATIC follow settings
        self.base_distance = self.CAMERA_DISTANCE
        self.speed_distance_scale = 0.06    # distance added per unit speed
        self.min_distance = self.CAMERA_DISTANCE * 0.6
        self.max_distance = self.CAMERA_DISTANCE * 1.8

        # Keep mild direction smoothing so it is not too twitchy
        self.follow_dir = Vector(start_direction[0], 0, start_direction[1])
        self.direction_smoothness = 0.08
        self.distance_smoothness = 0.12   # 0..1, higher = faster catch-up
        self.smoothed_distance = self.base_distance


        # Camera MANUAL control offsets
        self.pitch_offset = 0.0        # up/down look offset (radians)
        self.yaw_offset = 0.0          # left/right look offset (radians)
        self.distance_offset = 0.0     # manual distance adjustment
        self.height_offset = 0.0       # manual height adjustment
        
        # Control sensitivity
        self.pitch_speed = 1.5         # radians per second
        self.yaw_speed = 2.0           # radians per second
        self.distance_speed = 8.0      # units per second
        self.height_speed = 4.0        # units per second

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

    # Add methods to adjust camera manually:
    def adjust_pitch(self, delta_pitch):
        self.pitch_offset += delta_pitch
        # Clamp to prevent over-rotation
        max_pitch = radians(60)  # look up/down limit
        self.pitch_offset = max(-max_pitch, min(max_pitch, self.pitch_offset))

    def adjust_yaw(self, delta_yaw):
        self.yaw_offset += delta_yaw

    def adjust_distance(self, delta_distance):
        self.distance_offset += delta_distance

    def adjust_height(self, delta_height):
        self.height_offset += delta_height

    def reset_offsets(self):
        self.pitch_offset = 0.0
        self.yaw_offset = 0.0
        self.distance_offset = 0.0
        self.height_offset = 0.0

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
        # Direction smoothing (unchanged)
        t = self.direction_smoothness
        self.follow_dir = Vector(
            self.follow_dir.x + (car_direction.x - self.follow_dir.x) * t,
            self.follow_dir.y + (car_direction.y - self.follow_dir.y) * t,
            self.follow_dir.z + (car_direction.z - self.follow_dir.z) * t
        )
        self.follow_dir.normalize()

        # Distance smoothing (unchanged)
        target_dist = self.base_distance + abs(car_speed) * self.speed_distance_scale
        if target_dist < self.min_distance: target_dist = self.min_distance
        if target_dist > self.max_distance: target_dist = self.max_distance

        ds = self.distance_smoothness
        self.smoothed_distance += (target_dist - self.smoothed_distance) * ds
        
        # Apply manual distance and height offsets
        d = self.smoothed_distance + self.distance_offset
        height = self.camera_height + self.height_offset
        
        # Base camera position (behind car)
        base_eye = Point(
            car_position.x - self.follow_dir.x * d,
            car_position.y + height,
            car_position.z - self.follow_dir.z * d
        )
        
        # Apply manual yaw rotation around car
        if abs(self.yaw_offset) > 0.001:
            # Rotate camera position around car
            offset_vec = base_eye - car_position
            cos_yaw = cos(self.yaw_offset)
            sin_yaw = sin(self.yaw_offset)
            new_x = offset_vec.x * cos_yaw - offset_vec.z * sin_yaw
            new_z = offset_vec.x * sin_yaw + offset_vec.z * cos_yaw
            base_eye = Point(car_position.x + new_x, base_eye.y, car_position.z + new_z)
        
        # Look target (ahead of car, with yaw offset)
        look_dir = self.follow_dir.rotate_y(self.yaw_offset)
        center = Point(
            car_position.x + look_dir.x * 2.0,
            car_position.y,
            car_position.z + look_dir.z * 2.0
        )
        
        # Apply pitch offset by adjusting look target
        if abs(self.pitch_offset) > 0.001:
            center.y += sin(self.pitch_offset) * 5.0  # pitch sensitivity
        
        up = Vector(0, 1, 0)
        self.look_at(base_eye, center, up)

        self.shader.set_projection_view_matrix(
            self.multiply_matrices(self.projection_matrix.get_matrix(), self.get_matrix()))
        
    def update(self, arrow_keys, delta_time):
        if arrow_keys[0]:   # left
            self.adjust_yaw(-self.yaw_speed * delta_time)
        if arrow_keys[1]:   # right
            self.adjust_yaw(self.yaw_speed * delta_time)
        if arrow_keys[2]:   # up
            self.adjust_pitch(self.pitch_speed * delta_time)
        if arrow_keys[3]:   # down
            self.adjust_pitch(-self.pitch_speed * delta_time)
        
        if not any(arrow_keys):
            # smoothly return to neutral when no keys pressed
            self.yaw_offset -= self.yaw_offset * 0.1
            self.pitch_offset -= self.pitch_offset * 0.1
            if abs(self.yaw_offset) < 0.01:
                self.yaw_offset = 0.0
            if abs(self.pitch_offset) < 0.01:
                self.pitch_offset = 0.0
            

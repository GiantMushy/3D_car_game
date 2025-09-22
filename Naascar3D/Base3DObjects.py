
import random
from random import *

from OpenGL import GL, GLU, error

import math
from math import *


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def distance(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)
    
    def copy(self):
        return Vector(self.x, self.y, self.z)
    
    def rotate_y(self, angle):
        c = cos(angle)
        s = sin(angle)
        new_x = c * self.x - s * self.z
        new_z = s * self.x + c * self.z
        return Vector(new_x, self.y, new_z)

    def rotate_x(self, angle):
        c = cos(angle)
        s = sin(angle)
        new_y = c * self.y - s * self.z
        new_z = s * self.y + c * self.z
        return Vector(self.x, new_y, new_z)

    def rotate_z(self, angle):
        c = cos(angle)
        s = sin(angle)
        new_x = c * self.x - s * self.y
        new_y = s * self.x + c * self.y
        return Vector(new_x, new_y, self.z)
    
    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)



# ----------------------------------------------------------------------------------------------------
# ---------------------------------------RaceCar Objects----------------------------------------------
# ----------------------------------------------------------------------------------------------------

class Cube:
    def __init__(self):
        self.position_array = [
            -0.5, -0.5, -0.5, # back face
            -0.5,  0.5, -0.5,
             0.5,  0.5, -0.5,
             0.5, -0.5, -0.5,
             
            -0.5, -0.5,  0.5, # front face
            -0.5,  0.5,  0.5,
             0.5,  0.5,  0.5,
             0.5, -0.5,  0.5,

            -0.5, -0.5, -0.5, # bottom face
             0.5, -0.5, -0.5,
             0.5, -0.5,  0.5,
            -0.5, -0.5,  0.5,

            -0.5,  0.5, -0.5, # top face
             0.5,  0.5, -0.5,
             0.5,  0.5,  0.5,
            -0.5,  0.5,  0.5,

            -0.5, -0.5, -0.5, # left face
            -0.5, -0.5,  0.5,
            -0.5,  0.5,  0.5,
            -0.5,  0.5, -0.5,

             0.5, -0.5, -0.5, # right face
             0.5, -0.5,  0.5,
             0.5,  0.5,  0.5,
             0.5,  0.5, -0.5
             ]
        self.normal_array = [
             0.0,  0.0, -1.0, # back face
             0.0,  0.0, -1.0,
             0.0,  0.0, -1.0,
             0.0,  0.0, -1.0,

             0.0,  0.0,  1.0, # front face
             0.0,  0.0,  1.0,
             0.0,  0.0,  1.0,
             0.0,  0.0,  1.0,
             
             0.0, -1.0,  0.0, # bottom face
             0.0, -1.0,  0.0,
             0.0, -1.0,  0.0,
             0.0, -1.0,  0.0,

             0.0,  1.0,  0.0, # top face
             0.0,  1.0,  0.0,
             0.0,  1.0,  0.0,
             0.0,  1.0,  0.0,

             0.0, -1.0,  0.0, # left face
             0.0, -1.0,  0.0,
             0.0, -1.0,  0.0,
             0.0, -1.0,  0.0,

             1.0,  0.0,  0.0, # right face
             1.0,  0.0,  0.0,
             1.0,  0.0,  0.0,
             1.0,  0.0,  0.0
             ]

    def draw(self, shader):
        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 0, 4)
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 4, 4)
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 8, 4)
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 12, 4)
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 16, 4)
        GL.glDrawArrays(GL.GL_TRIANGLE_FAN, 20, 4)


class Sphere:
    def __init__(self, latitude_bands = 10, longitude_bands = 10):
        self.position_array = []
        self.normal_array = []

        for lat_number in range(0, latitude_bands + 1):
            theta = lat_number * pi / latitude_bands
            sin_theta = sin(theta)
            cos_theta = cos(theta)

            for long_number in range(0, longitude_bands + 1):
                phi = long_number * 2 * pi / longitude_bands
                sin_phi = sin(phi)
                cos_phi = cos(phi)

                x = cos_phi * sin_theta
                y = cos_theta
                z = sin_phi * sin_theta

                self.normal_array.append(x)
                self.normal_array.append(y)
                self.normal_array.append(z)
                self.position_array.append(x * 0.5)
                self.position_array.append(y * 0.5)
                self.position_array.append(z * 0.5)

        self.index_array = []
        for lat_number in range(0, latitude_bands):
            for long_number in range(0, longitude_bands):
                first = (lat_number * (longitude_bands + 1)) + long_number
                second = first + longitude_bands + 1
                self.index_array.append(first)
                self.index_array.append(second)
                self.index_array.append(first + 1)

                self.index_array.append(second)
                self.index_array.append(second + 1)
                self.index_array.append(first + 1)
    
    def draw(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)


class Wheel:
    def __init__(self, radius=1.0, width=1.0, segments=8):
        self.position_array = []
        self.normal_array = []
        self.index_array = []


        # Side vertices
        for i in range(segments + 1):
            angle = i * 2 * pi / segments
            z = radius * cos(angle)
            y = radius * sin(angle)

            # Left circle edge (x = 0)
            self.position_array.extend([0.0, y, z])
            self.normal_array.extend([0.0, y, z])

            # Right circle edge (x = +width)
            self.position_array.extend([width, y, z])
            self.normal_array.extend([0.0, y, z])

        # Side faces
        for i in range(segments):
            left1 = i * 2
            right1 = left1 + 1
            left2 = (i + 1) * 2
            right2 = left2 + 1

            self.index_array.extend([left2, right1, left1])
            self.index_array.extend([right1, right2, left2])

        # Center points for caps
        left_center_idx = len(self.position_array) // 3
        self.position_array.extend([0.0, 0.0, 0.0])
        self.normal_array.extend([-1.0, 0.0, 0.0])

        right_center_idx = left_center_idx + 1
        self.position_array.extend([width, 0.0, 0.0])
        self.normal_array.extend([1.0, 0.0, 0.0])

        # Left cap (x=0)
        for i in range(segments):
            edge1 = i * 2
            edge2 = ((i + 1) % segments) * 2
            self.index_array.extend([left_center_idx, edge2, edge1])

        # Right cap (x=width)
        for i in range(segments):
            edge1 = i * 2 + 1
            edge2 = ((i + 1) % segments) * 2 + 1
            self.index_array.extend([right_center_idx, edge1, edge2])

    def draw(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

class RaceCar:
    def __init__(self, scale=1.0,
                 body_color=(0.9, 0.1, 0.1),
                 cabin_color=(0.30, 0.80, 0.90),
                 wheel_color=(0.1, 0.1, 0.1),
                 steering_angle=0.0):
        self.scale = scale

        # Wheel / track geometry
        self.wheel_radius = 0.5 * scale
        self.wheel_width  = 0.5 * scale
        self.track = 1.8 * scale   # distance between wheel centers (x)

        self.front_axle_l = 0.50 * scale
        self.body_mid_l   = 1.90 * scale
        self.rear_axle_l  = 0.60 * scale
        self.total_l = self.front_axle_l + self.body_mid_l + self.rear_axle_l

        # Widths / heights
        self.axle_w   = self.track + 0.30 * scale   # axles a bit wider (front wing feel)
        self.axle_h   = 0.20 * scale
        self.body_w   = 1.00 * scale
        self.body_h   = 0.20 * scale
        self.cockpit_w = 0.8 * scale
        self.cockpit_h = 0.5 * scale
        self.cockpit_l = 1.2 * scale

        self.front_axle_z =  self.total_l * 0.5 - self.front_axle_l * 0.5
        self.rear_axle_z  = -self.total_l * 0.5 + self.rear_axle_l * 0.5
        self.body_mid_z = (self.front_axle_z + self.rear_axle_z) * 0.5
        self.cockpit_z = self.body_mid_z - 0.20 * scale

        # Wheel base derived from axle centers
        self.wheel_base = self.front_axle_z - self.rear_axle_z

        # Vertical placement (origin on ground y=0)
        self.axle_center_y = self.wheel_radius + self.axle_h * 0.5
        self.body_center_y = self.axle_center_y + self.axle_h * 0.5 + self.body_h * 0.5
        self.cockpit_center_y = self.body_center_y + self.body_h * 0.5 + self.cockpit_h * 0.1

        # Colors
        self.body_color = body_color      # used for axles + main body
        self.cabin_color = cabin_color    # used for cockpit
        self.wheel_color = wheel_color

        self.front_axle = Cube()
        self.mid_body   = Cube()
        self.rear_axle  = Cube()
        self.cockpit    = Sphere(latitude_bands=8, longitude_bands=8)
        self.wheel      = Wheel(radius=self.wheel_radius, width=self.wheel_width, segments=16)
        self.steering_angle = steering_angle

    def draw(self, shader, model_matrix, position=Point(0,0,0), yaw=0.0):
        def draw_part(obj, color, tx, ty, tz, sx=1.0, sy=1.0, sz=1.0, rotate_y=None):
            model_matrix.load_identity()
            model_matrix.add_translation(position.x, position.y, position.z)
            model_matrix.add_rotation_y(yaw)
            model_matrix.add_translation(tx, ty, tz)
            if rotate_y is not None:
                model_matrix.add_rotation_y(rotate_y)
            model_matrix.add_scale(sx, sy, sz)
            shader.set_model_matrix(model_matrix.matrix)
            shader.set_solid_color(*color)
            obj.draw(shader)

        # Front axle cube
        draw_part(
            self.front_axle, self.body_color,
            0.0, self.axle_center_y, self.front_axle_z,
            self.axle_w, self.axle_h, self.front_axle_l
        )

        # Rear axle cube
        draw_part(
            self.rear_axle, self.body_color,
            0.0, self.axle_center_y, self.rear_axle_z,
            self.axle_w * 0.9, self.axle_h * 1.1, self.rear_axle_l
        )

        # Central body
        draw_part(
            self.mid_body, self.body_color,
            0.0, self.body_center_y, self.body_mid_z,
            self.body_w, self.body_h, self.body_mid_l
        )

        # Cockpit
        draw_part(
            self.cockpit, self.cabin_color,
            0.0, self.cockpit_center_y, self.cockpit_z,
            self.cockpit_w, self.cockpit_h, self.cockpit_l
        )

        # Wheels (geometry spans x=[0..wheel_width], so shift so center aligns)
        wx_left_center  = -self.track * 0.5
        wx_right_center =  self.track * 0.5
        wx_left  = wx_left_center  - self.wheel_width * 0.5
        wx_right = wx_right_center - self.wheel_width * 0.5
        wy_center = self.wheel_radius
        wz_front  = self.front_axle_z
        wz_back   = self.rear_axle_z

        # Front-left
        draw_part(self.wheel, self.wheel_color, wx_left,  wy_center, wz_front, rotate_y=self.steering_angle)
        # Front-right
        draw_part(self.wheel, self.wheel_color, wx_right, wy_center, wz_front, rotate_y=self.steering_angle)

        # Rear-left
        draw_part(self.wheel, self.wheel_color, wx_left,  wy_center, wz_back)
        # Rear-right
        draw_part(self.wheel, self.wheel_color, wx_right, wy_center, wz_back)



# ----------------------------------------------------------------------------------------------------
# --------------------------------------RaceTrack Objects---------------------------------------------
# ----------------------------------------------------------------------------------------------------

class VerticalWall:
    def __init__(self, width = 1.0, height = 1.0, color=(0.5,0.5,0.5)):
        w = width
        h = height
        self.color = color
        self.position_array = [
            0.0, 0.0, 0.0,
            0.0, h,   0.0,
            w,   h,   0.0,
            w,   0.0, 0.0
            ]
        self.normal_array = [
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0
        ]
        self.index_array = [
            0, 1, 2,
            2, 3, 0
        ]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

class HorizontalWall:
    def __init__(self, width = 1.0, height = 1.0, color=(0.1,0.1,0.1)):
        w = width
        h = height
        self.color = color
        self.position_array = [
            0.0, 0.0, 0.0,
            0.0, h,   0.0,
            0.0, h,   w,
            0.0, 0.0, w
            ]
        self.normal_array = [-1.0, 0.0, 0.0] * 4
        self.index_array =  [0, 1, 2, 2, 3, 0]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

class FloorTile:
    def __init__(self, size = 1.0, color=(0.0,0.5,0.0)):
        self.color = color
        self.position_array = [
            0.0, 0.0, 0.0,
            size,0.0, 0.0,
            size,0.0, size,
            0.0, 0.0, size
            ]
        self.normal_array = [0.0, 1.0, 0.0] * 4
        self.index_array =  [0, 1, 2, 2, 3, 0]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

class FinishLine:
    # Centered checkered finish line (alternating black/white)
    def __init__(self, road_width=1.0, banks=0.0, tile_size=1.0, horizontal=True, color1=(1.0,1.0,1.0), color2=(0.0,0.0,0.0)):
        w = road_width
        b = banks
        self.color1 = color1
        self.color2 = color2
        self.horizontal = horizontal

        band_thickness = w / 10.0
        square_size = w / 20.0

        if band_thickness < 0.001:
            band_thickness = w * 0.1
        if square_size < 0.001:
            square_size = w * 0.1

        band_offset = (tile_size - band_thickness) * 0.5

        self.squares = []  # (positions, normals)

        num_squares = int(w / square_size)
        if num_squares < 1:
            num_squares = 1
            square_size = w

        if horizontal:
            z0 = band_offset
            z1 = band_offset + band_thickness
            for i in range(num_squares):
                x0 = b + i * square_size
                x1 = b + min(w, (i + 1) * square_size)
                positions = [
                    x0, 0.0, z0,
                    x0, 0.0, z1,
                    x1, 0.0, z1,
                    x1, 0.0, z0
                ]
                normals = [0.0, 1.0, 0.0] * 4
                self.squares.append((positions, normals))
        else:
            x0_n = band_offset
            x1_n = band_offset + band_thickness
            for i in range(num_squares):
                z0 = b + i * square_size
                z1 = b + min(w, (i + 1) * square_size)
                positions = [
                    x0_n, 0.0, z0,
                    x0_n, 0.0, z1,
                    x1_n, 0.0, z1,
                    x1_n, 0.0, z0
                ]
                normals = [0.0, 1.0, 0.0] * 4
                self.squares.append((positions, normals))

        self.indices = [0, 1, 2, 2, 3, 0]

    def draw(self, shader):
        for i, (pos, norms) in enumerate(self.squares):
            color = self.color1 if (i % 2 == 0) else self.color2
            shader.set_solid_color(*color)
            shader.set_position_attribute(pos)
            shader.set_normal_attribute(norms)
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, self.indices)


    def draw(self, shader):
        # Draw each square with alternating colors
        for i, (pos, norms) in enumerate(self.squares):
            color = self.color1 if (i % 2 == 0) else self.color2
            shader.set_solid_color(*color)
            shader.set_position_attribute(pos)
            shader.set_normal_attribute(norms)
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, self.indices)


class HorizontalRoad:
    def __init__(self, width = 1.0, tile_size = 1.0, banks = 1.0, color=(0.2,0.2,0.2)):
        w = width
        s = tile_size
        b = banks
        self.color = color
        self.position_array = [
            b,   0.0, 0.0,
            b,   0.0, s,
            w+b, 0.0, s,
            w+b, 0.0, 0.0
            ]
        self.normal_array = [0.0, 1.0, 0.0] * 4
        self.index_array =  [0, 1, 2, 2, 3, 0]

    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

class VerticalRoad:
    def __init__(self, width = 1.0, tile_size = 0.1, banks = 1.0, color=(0.2,0.2,0.2)):
        w = width
        s = tile_size
        b = banks
        self.color = color
        self.position_array = [
            0.0, 0.0, b,
            s,   0.0, b,
            s,   0.0, w+b,
            0.0, 0.0, w+b
            ]
        self.normal_array = [0.0, 1.0, 0.0] * 4
        self.index_array =  [0, 1, 2, 2, 3, 0]

    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

class LeftTurnRoad:
    def __init__(self, width = 1.0, tile_size = 0.1, banks = 1.0, color=(0.2,0.2,0.2)):
        w = width
        s = tile_size
        b = banks
        self.color = color
        self.position_array = [
            0.0, 0.0, w+b,
            0.0, 0.0, b,
            w,   0.0, w,
            b,   0.0, 0.0,
            w+b, 0.0, 0.0
            ]
        self.normal_array = [0.0, 1.0, 0.0] * 5
        self.index_array = [
            0, 1, 2,
            1, 2, 3,
            2, 3, 4
        ]

    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

class RightTurnRoad:
    def __init__(self, width = 1.0, tile_size = 0.1, banks = 1.0, color=(0.2,0.2,0.2)):
        w = width
        s = tile_size
        b = banks
        self.color = color
        self.position_array = [
            0.0, 0.0, b,
            0.0, 0.0, b+w,
            w,   0.0, w,
            b,   0.0, s,
            w+b, 0.0, s
            ]
        self.normal_array = [0.0, 1.0, 0.0] * 5
        self.index_array = [
            0, 1, 2,
            1, 2, 3,
            2, 3, 4
        ]

    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)
    
class DownLeftTurnRoad:
    def __init__(self, width = 1.0, tile_size = 0.1, banks = 1.0, color=(0.2,0.2,0.2)):
        w = width
        s = tile_size
        b = banks
        self.color = color
        self.position_array = [
            s,   0.0, w+b,
            s,   0.0, b,
            s-w, 0.0, w,
            s-b, 0.0, 0.0,
            b,   0.0, 0.0
            ]
        self.normal_array = [0.0, 1.0, 0.0] * 5
        self.index_array = [
            0, 1, 2,
            1, 2, 3,
            2, 3, 4
        ]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

class DownRightTurnRoad:
    def __init__(self, width = 1.0, tile_size = 0.1, banks = 1.0, color=(0.2,0.2,0.2)):
        w = width
        s = tile_size
        b = banks
        self.color = color
        self.position_array = [
            s,   0.0, b,
            s,   0.0, w+b,
            s-w, 0.0, s-w,
            s-b, 0.0, s,
            b,   0.0, s
            ]
        self.normal_array = [0.0, 1.0, 0.0] * 5
        self.index_array = [
            0, 1, 2,
            1, 2, 3,
            2, 3, 4
        ]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------Pickup Objects----------------------------------------------
# ----------------------------------------------------------------------------------------------------

class Pickup:
    def __init__(self, scale = 1.0, type = "speed_boost", color=(1.0, 0.84, 0.0)):
        self.scale = scale
        self.type = type
        self.color = color
        self.body = Sphere(latitude_bands=6, longitude_bands=6)

        # Animation state
        self.time = 0.0
        self.spin_speed = 1.0          # radians per second
        self.bob_speed = 0.8           # cycles per second
        self.bob_height = 0.25 * scale

        # Cache original geometry for vertex-space animation
        self.spin_angle = 0.0
        self.y_offset = 0.0

    def update(self, delta_time):
        # Advance time and compute simple animated parameters
        self.time += delta_time
        self.spin_angle = self.time * self.spin_speed
        self.y_offset = sin(self.time * self.bob_speed * 2.0 * pi) * self.bob_height

    def draw(self, shader):
        shader.set_solid_color(*self.color)
        self.body.draw(shader)

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
        shader.set_solid_color(*self.color)  # set uniform color
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
        self.normal_array = [
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0
        ]
        self.index_array = [
            0, 1, 2,
            2, 3, 0
        ]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)  # set uniform color
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)


class RaceCar:
    def __init__(self, scale=1.0, body_color=(0.9, 0.1, 0.1), cabin_color=(0.2, 0.2, 0.25), wheel_color=(0.1, 0.1, 0.1)):
        # Dimensions (in car-local space)
        self.scale = scale
        self.body_w = 1.6 * scale
        self.body_h = 0.4 * scale
        self.body_l = 3.0 * scale

        self.cabin_w = 1.2 * scale
        self.cabin_h = 0.5 * scale
        self.cabin_l = 1.2 * scale

        self.wheel_radius = 0.35 * scale
        self.wheel_width  = 0.30 * scale
        self.track = 1.2 * scale           # distance between wheel centers (x)
        self.wheel_base = 1.6 * scale      # distance between front/back wheel centers (z)

        # Colors
        self.body_color = body_color
        self.cabin_color = cabin_color
        self.wheel_color = wheel_color

        # Parts (reused across draws)
        self.chassis = Cube()
        self.cabin = Cube()
        self.wheel = Wheel(radius=self.wheel_radius, width=self.wheel_width, segments=16)

    def draw(self, shader, model_matrix, position=Point(0,0,0), yaw=0.0):
        # Helper to set matrix and draw a part
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

        # Ground reference: car origin is at ground plane (y=0), centered in z
        # Raise chassis so bottom sits above wheels
        chassis_y = self.wheel_radius + self.body_h * 0.5
        draw_part(
            self.chassis, self.body_color,
            0.0, chassis_y, 0.0,
            self.body_w, self.body_h, self.body_l
        )

        # Cabin, slightly rear-biased
        cabin_y = chassis_y + self.body_h * 0.5 + self.cabin_h * 0.5
        cabin_z = -self.body_l * 0.15
        draw_part(
            self.cabin, self.cabin_color,
            0.0, cabin_y, cabin_z,
            self.cabin_w, self.cabin_h, self.cabin_l
        )

        # Wheels: Wheel geometry runs from x=[0..width], center at x=width/2.
        # Place by translating so that center lands on target_x.
        wx_left_center  = -self.track * 0.5
        wx_right_center =  self.track * 0.5
        wx_left   = wx_left_center  - self.wheel_width * 0.5
        wx_right  = wx_right_center - self.wheel_width * 0.5
        wy_center = self.wheel_radius
        wz_front  =  self.wheel_base * 0.5
        wz_back   = -self.wheel_base * 0.5

        # Front-left
        draw_part(self.wheel, self.wheel_color, wx_left,  wy_center, wz_front)
        # Front-right
        draw_part(self.wheel, self.wheel_color, wx_right, wy_center, wz_front)
        # Rear-left
        draw_part(self.wheel, self.wheel_color, wx_left,  wy_center, wz_back)
        # Rear-right
        draw_part(self.wheel, self.wheel_color, wx_right, wy_center, wz_back)



# ----------------------------------------------------------------------------------------------------
# --------------------------------------RaceTrack Objects---------------------------------------------
# ----------------------------------------------------------------------------------------------------

class FloorTile:
    def __init__(self, size = 1.0, color=(0.0,0.5,0.0)):
        self.color = color
        self.position_array = [
            0.0, 0.0, 0.0,
            size,0.0, 0.0,
            size,0.0, size,
            0.0, 0.0, size
            ]
        self.normal_array = [
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0
        ]
        self.index_array = [
            0, 1, 2,
            2, 3, 0
        ]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)  # set uniform color
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

class FinishLine:
    def __init__(self, width = 1.0, height = 0.1, color=(1.0,1.0,1.0)):
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
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0
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

class HorizontalRoad:
    def __init__(self, width = 1.0, tile_size = 1.0, banks = 1.0, color=(0.2,0.2,0.2)):
        w = width
        s = tile_size
        b = banks
        self.color = color
        self.position_array = [
            b, 0.0, 0.0,
            b, 0.0, s,
            w + b, 0.0, s,
            w + b, 0.0, 0.0
            ]
        self.normal_array = [
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0
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

class VerticalRoad:
    def __init__(self, width = 1.0, tile_size = 0.1, banks = 1.0, color=(0.2,0.2,0.2)):
        w = width
        s = tile_size
        b = banks
        self.color = color
        self.position_array = [
            0.0, 0.0, b,
            s,   0.0, b,
            s,   0.0, w + b,
            0.0, 0.0, w + b
            ]
        self.normal_array = [
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0
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
        self.normal_array = [
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0
        ]
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
        self.normal_array = [
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0
        ]
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
        self.normal_array = [
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0
        ]
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
        self.normal_array = [
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0
        ]
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
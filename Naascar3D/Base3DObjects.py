
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


class Rectangle:
    def __init__(self, width = 1.0, height = 1.0):
        w = width / 2
        h = height / 2
        self.position_array = [
            -w, -h, 0.0,
             w, -h, 0.0,
             w,  h, 0.0,
            -w,  h, 0.0
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
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)


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


class Cylinder:
    def __init__(self, radius = 0.5, height = 1.0, segments = 30):
        self.position_array = []
        self.normal_array = []

        for i in range(segments + 1):
            angle = i * 2 * pi / segments
            x = radius * cos(angle)
            z = radius * sin(angle)

            # Bottom circle
            self.position_array.append(x)
            self.position_array.append(-height / 2)
            self.position_array.append(z)
            self.normal_array.append(x)
            self.normal_array.append(0.0)
            self.normal_array.append(z)

            # Top circle
            self.position_array.append(x)
            self.position_array.append(height / 2)
            self.position_array.append(z)
            self.normal_array.append(x)
            self.normal_array.append(0.0)
            self.normal_array.append(z)

        self.index_array = []
        for i in range(segments):
            bottom1 = i * 2
            top1 = bottom1 + 1
            bottom2 = (i + 1) * 2
            top2 = bottom2 + 1

            # Side triangles
            self.index_array.append(bottom1)
            self.index_array.append(top1)
            self.index_array.append(bottom2)

            self.index_array.append(top1)
            self.index_array.append(top2)
            self.index_array.append(bottom2)

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

class Wall:
    def __init__(self, width = 1.0, height = 1.0):
        w = width / 2
        h = height / 2
        self.position_array = [
            -w, -h, 0.0,
             w, -h, 0.0,
             w,  h, 0.0,
            -w,  h, 0.0
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
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

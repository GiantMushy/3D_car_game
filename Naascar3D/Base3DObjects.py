
import random
from random import *

from OpenGL import GL, GLU, error

from MeshLoader import *

import math
from math import *

class Coordinate:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, n):
        return Coordinate(self.x * n, self.y * n)

    def __rmul__(self, n):
        return Coordinate(self.x * n, self.y * n)

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Coordinate({self.x}, {self.y})"


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, x):
        return Point(self.x * x, self.y * x, self.z * x)
    
    def __rmul__(self, x):
        return Point(self.x * x, self.y * x, self.z * x)
    
    def distance(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)
    
    def copy(self):
        return Point(self.x, self.y, self.z)

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
    
    def __mul__(self, x):
        return Vector(self.x * x, self.y * x, self.z * x)
    
    def __rmul__(self, x):
        return Vector(self.x * x, self.y * x, self.z * x)
    
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
MeshLoader = MeshLoader()

class Cube:
    FILENAME = "cube"
    def __init__(self):
        if MeshLoader.mesh_exists(self.FILENAME):
            mesh_data = MeshLoader.load_mesh(self.FILENAME)
            self.position_array = mesh_data.positions
            self.normal_array = mesh_data.normals
            #print(f"Loaded mesh from file: {self.FILENAME}.json")

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
    FILENAME = "sphere"
    def __init__(self, bands = 10):
        name = self.FILENAME + "_" + str(bands)
        if MeshLoader.mesh_exists(name):
            mesh_data = MeshLoader.load_mesh(name)
            self.position_array = mesh_data.positions
            self.normal_array = mesh_data.normals
            self.index_array = mesh_data.indices
            print(f"Loaded mesh from file: {name}.json")
        
        else:
            self._generate_mesh(bands)
            MeshLoader.save_mesh(name, self.position_array, self.normal_array, self.index_array)
            print(f"Saved mesh to file:    {name}.json")

    def _generate_mesh(self, bands):
        self.position_array = []
        self.normal_array = []

        for lat_number in range(0, bands + 1):
            theta = lat_number * pi / bands
            sin_theta = sin(theta)
            cos_theta = cos(theta)

            for long_number in range(0, bands + 1):
                phi = long_number * 2 * pi / bands
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
        for lat_number in range(0, bands):
            for long_number in range(0, bands):
                first = (lat_number * (bands + 1)) + long_number
                second = first + bands + 1
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
    FILENAME = "wheel"
    def __init__(self, radius=1.0, width=1.0, segments=8):
        name = self.FILENAME + "_r_w_seg$" + str(radius) + "_" + str(width) + "_" + str(segments)
        if MeshLoader.mesh_exists(name):
            mesh_data = MeshLoader.load_mesh(name)
            self.position_array = mesh_data.positions
            self.normal_array = mesh_data.normals
            self.index_array = mesh_data.indices
            print(f"Loaded mesh from file: {name}.json")
        
        else:
            self._generate_mesh(radius, width, segments)
            MeshLoader.save_mesh(name, self.position_array, self.normal_array, self.index_array)
            print(f"Saved mesh to file:    {name}.json")
    
    def _generate_mesh(self, radius, width, segments):
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
    FILENAME = "racecar"
    def __init__(self, type=1):
        self._generate_mesh(type)
        
    def _generate_mesh(self, type):
        cabin_color=(0.3, 0.8, 0.9)
        wheel_color=(0.1, 0.1, 0.1)

        if type == 1:
            body_color=(0.9, 0.1, 0.1)
        elif type == 2:
            body_color=(0.1, 0.9, 0.1)

        # Wheel / track geometry
        self.wheel_radius = 0.5
        self.wheel_width  = 0.5
        self.track = 1.8   # distance between wheel centers (x)

        self.front_axle_l = 0.50
        self.body_mid_l   = 1.90
        self.rear_axle_l  = 0.60
        self.total_l = self.front_axle_l + self.body_mid_l + self.rear_axle_l

        # Widths / heights
        self.axle_w   = self.track + 0.30   # axles a bit wider (front wing feel)
        self.axle_h   = 0.20
        self.body_w   = 1.00
        self.body_h   = 0.20
        self.cockpit_w = 0.8 
        self.cockpit_h = 0.5
        self.cockpit_l = 1.2

        self.front_axle_z =  self.total_l * 0.5 - self.front_axle_l * 0.5
        self.rear_axle_z  = -self.total_l * 0.5 + self.rear_axle_l * 0.5
        self.body_mid_z = (self.front_axle_z + self.rear_axle_z) * 0.5
        self.cockpit_z = self.body_mid_z - 0.20

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
        self.cockpit    = Sphere(bands=10)
        self.wheel      = Wheel(radius=self.wheel_radius, width=self.wheel_width, segments=16)
        self.steering_angle = 0.0

    def draw(self, shader, model_matrix, position=Point(0,0,0), yaw=0.0):
        def draw_part(obj, color, tx, ty, tz, sx=1.0, sy=1.0, sz=1.0, rotate_y=None, 
                    shininess=32.0, specular_strength=0.0):  # NEW: material params
            model_matrix.load_identity()
            model_matrix.add_translation(position.x, position.y, position.z)
            model_matrix.add_rotation_y(yaw)
            model_matrix.add_translation(tx, ty, tz)
            if rotate_y is not None:
                model_matrix.add_rotation_y(rotate_y)
            model_matrix.add_scale(sx, sy, sz)
            shader.set_model_matrix(model_matrix.matrix)
            
            # Set material properties before drawing
            shader.set_material_properties(shininess, specular_strength)
            shader.set_solid_color(*color)
            obj.draw(shader)

        # Draw non-shiny parts (no specular)
        draw_part(self.front_axle, self.body_color, 0.0, self.axle_center_y, self.front_axle_z,
                self.axle_w, self.axle_h, self.front_axle_l)
        
        draw_part(self.rear_axle, self.body_color, 0.0, self.axle_center_y, self.rear_axle_z,
                self.axle_w * 0.9, self.axle_h * 1.1, self.rear_axle_l)
        
        draw_part(self.mid_body, self.body_color, 0.0, self.body_center_y, self.body_mid_z,
                self.body_w, self.body_h, self.body_mid_l)

        # Draw SHINY cockpit with high specular strength
        draw_part(self.cockpit, self.cabin_color, 0.0, self.cockpit_center_y, self.cockpit_z,
                self.cockpit_w, self.cockpit_h, self.cockpit_l,
                shininess=128.0, specular_strength=0.8)  # Very shiny!

        # Draw wheels (matte)
        wx_left_center = -self.track * 0.5
        wx_right_center = self.track * 0.5
        wx_left = wx_left_center - self.wheel_width * 0.5
        wx_right = wx_right_center - self.wheel_width * 0.5
        wy_center = self.wheel_radius
        wz_front = self.front_axle_z
        wz_back = self.rear_axle_z

        draw_part(self.wheel, self.wheel_color, wx_left, wy_center, wz_front, rotate_y=self.steering_angle)
        draw_part(self.wheel, self.wheel_color, wx_right, wy_center, wz_front, rotate_y=self.steering_angle)
        draw_part(self.wheel, self.wheel_color, wx_left, wy_center, wz_back)
        draw_part(self.wheel, self.wheel_color, wx_right, wy_center, wz_back)



# ----------------------------------------------------------------------------------------------------
# --------------------------------------RaceTrack Objects---------------------------------------------
# ----------------------------------------------------------------------------------------------------

class VerticalWall:
    FILENAME = "wall_vert"
    def __init__(self, width = 1.0, height = 1.0, color=(0.5,0.5,0.5)):
        w = width
        h = height
        p = 0.01
        self.color = color
        self.position_array = [
            # Front face (original)
            0.0, 0.0, 0.0,
            0.0, h,   0.0,
            w,   h,   0.0,
            w,   0.0, 0.0,
            
            # Back face (same positions, different winding)
            0.0, 0.0, p,
            w,   0.0, p,
            w,   h,   p,
            0.0, h,   p
        ]
        self.normal_array = [
            # Front face normals (pointing forward +Z)
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            
            # Back face normals (pointing backward -Z)
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0
        ]
        self.index_array = [
            # Front face
            0, 1, 2,
            2, 3, 0,
            
            # Back face (reversed winding for proper culling)
            4, 5, 6,
            6, 7, 4
        ]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

class HorizontalWall:
    FILENAME = "wall_horiz"
    def __init__(self, width = 1.0, height = 1.0, color=(0.1,0.1,0.1)):
        w = width
        h = height
        p = 0.01
        self.color = color
        self.position_array = [
            # Front face (original - facing +X direction)
            0.0, 0.0, 0.0,
            0.0, h,   0.0,
            0.0, h,   w,
            0.0, 0.0, w,
            
            # Back face (facing -X direction)
            p, 0.0, 0.0,
            p, 0.0, w,
            p, h,   w,
            p, h,   0.0
        ]
        self.normal_array = [
            # Front face normals (pointing in -X direction)
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            
            # Back face normals (pointing in +X direction)
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0
        ]
        self.index_array = [
            # Front face
            0, 1, 2, 
            2, 3, 0,
            
            # Back face (reversed winding)
            4, 5, 6,
            6, 7, 4
        ]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)

class StadiumBorder:
    FILENAME = "border"
    ''' Draws simple single-sided walls around the track's boundaries '''
    def __init__(self, world_width=1.0, border_height=1.0, color=(0.5,0.5,0.5)):
        self.world_width = world_width
        self.border_height = border_height
        self.color = color
        self.wall_thickness = 1.0
        
        # Create single-sided walls manually
        self._create_walls()
    
    def _create_walls(self):
        w = self.world_width
        h = self.border_height
        t = self.wall_thickness
        
        # North wall (top) - faces south (into the track)
        self.north_positions = [
            -t, 0.0, -t,    # bottom-left
            -t, h,   -t,    # top-left
            w+t, h,  -t,    # top-right
            w+t, 0.0, -t    # bottom-right
        ]
        self.north_normals = [0.0, 0.0, 1.0] * 4  # facing +Z (south)
        
        # South wall (bottom) - faces north (into the track)
        self.south_positions = [
            w+t, 0.0, w+t,  # bottom-right
            w+t, h,   w+t,  # top-right
            -t,  h,   w+t,  # top-left
            -t,  0.0, w+t   # bottom-left
        ]
        self.south_normals = [0.0, 0.0, -1.0] * 4  # facing -Z (north)
        
        # West wall (left) - faces east (into the track)
        self.west_positions = [
            -t, 0.0, w+t,   # bottom-back
            -t, h,   w+t,   # top-back
            -t, h,   -t,    # top-front
            -t, 0.0, -t     # bottom-front
        ]
        self.west_normals = [1.0, 0.0, 0.0] * 4  # facing +X (east)
        
        # East wall (right) - faces west (into the track)
        self.east_positions = [
            w+t, 0.0, -t,   # bottom-front
            w+t, h,   -t,   # top-front
            w+t, h,   w+t,  # top-back
            w+t, 0.0, w+t   # bottom-back
        ]
        self.east_normals = [-1.0, 0.0, 0.0] * 4  # facing -X (west)
        
        # Shared index array for all walls (two triangles per wall)
        self.indices = [0, 1, 2, 2, 3, 0]
    
    def draw(self, shader, model_matrix):
        # Set material properties for walls (no specular)
        shader.set_material_properties(32.0, 0.0)
        shader.set_solid_color(*self.color)
        
        # North wall
        model_matrix.load_identity()
        shader.set_model_matrix(model_matrix.matrix)
        shader.set_position_attribute(self.north_positions)
        shader.set_normal_attribute(self.north_normals)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, self.indices)
        
        # South wall
        model_matrix.load_identity()
        shader.set_model_matrix(model_matrix.matrix)
        shader.set_position_attribute(self.south_positions)
        shader.set_normal_attribute(self.south_normals)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, self.indices)
        
        # West wall
        model_matrix.load_identity()
        shader.set_model_matrix(model_matrix.matrix)
        shader.set_position_attribute(self.west_positions)
        shader.set_normal_attribute(self.west_normals)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, self.indices)
        
        # East wall
        model_matrix.load_identity()
        shader.set_model_matrix(model_matrix.matrix)
        shader.set_position_attribute(self.east_positions)
        shader.set_normal_attribute(self.east_normals)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.indices), GL.GL_UNSIGNED_INT, self.indices)

class FloorTile:
    FILENAME = "floor"
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
    FILENAME = "finish_line"
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
    FILENAME = "road_horiz"
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
    FILENAME = "raod_vert"
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
    FILENAME = "road_left"
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
    FILENAME = "road_right"
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
    FILENAME = "road_downleft"
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
    FILENAME = "road_downright"
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

class Cylinder:
    FILENAME = "cylinder"
    def __init__(self, length=2.0, segments=8, width=1.0):
        self.position_array = []
        self.normal_array = []
        self.index_array = []
        
        radius = width * 0.5
        
        # Generate vertices for cylinder sides
        for i in range(segments + 1):
            angle = i * 2 * pi / segments
            x = radius * cos(angle)
            z = radius * sin(angle)
            
            # Bottom circle (y = 0)
            self.position_array.extend([x, 0.0, z])
            self.normal_array.extend([x/radius, 0.0, z/radius])  # normalized radial normal
            
            # Top circle (y = length)
            self.position_array.extend([x, length, z])
            self.normal_array.extend([x/radius, 0.0, z/radius])
        
        # Side faces (quads made of triangles)
        for i in range(segments):
            bottom1 = i * 2
            top1 = bottom1 + 1
            bottom2 = (i + 1) * 2
            top2 = bottom2 + 1
            
            # First triangle
            self.index_array.extend([bottom1, top1, bottom2])
            # Second triangle  
            self.index_array.extend([top1, top2, bottom2])
        
        # Center points for caps
        bottom_center_idx = len(self.position_array) // 3
        self.position_array.extend([0.0, 0.0, 0.0])
        self.normal_array.extend([0.0, -1.0, 0.0])
        
        top_center_idx = bottom_center_idx + 1
        self.position_array.extend([0.0, length, 0.0])
        self.normal_array.extend([0.0, 1.0, 0.0])
        
        # Bottom cap
        for i in range(segments):
            edge1 = i * 2
            edge2 = ((i + 1) % segments) * 2
            self.index_array.extend([bottom_center_idx, edge2, edge1])
        
        # Top cap
        for i in range(segments):
            edge1 = i * 2 + 1
            edge2 = ((i + 1) % segments) * 2 + 1
            self.index_array.extend([top_center_idx, edge1, edge2])
    
    def draw(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)


class StadiumLights:
    FILENAME = "stadiumlights"
    def __init__(self, scale=1.0, 
                 pole_color=(0.6, 0.6, 0.6),
                 light_color=(0.5, 0.5, 0.5)):
        self.scale = scale
        
        # Pole dimensions
        self.pole_height = 8.0 * scale
        self.pole_width = 0.3 * scale
        
        # Light fixture dimensions  
        self.light_length = 0.2 * scale
        self.light_width = 0.5 * scale
        self.lights_height_offset = 0.4 * scale  # how far down from top to place lights
        
        # Colors
        self.pole_color = pole_color
        self.light_color = light_color
        
        # Create geometry objects
        self.pole = Cylinder(length=self.pole_height, segments=12, width=self.pole_width)
        self.light_fixture = Cylinder(length=self.light_length, segments=8, width=self.light_width)
    
    def draw(self, shader, model_matrix, position=Point(0,0,0), yaw=0.0):
        def draw_part(obj, color, tx, ty, tz, sx=1.0, sy=1.0, sz=1.0, rotate_x=None, rotate_y=None, rotate_z=None):
            model_matrix.load_identity()
            model_matrix.add_translation(position.x, position.y, position.z)
            model_matrix.add_rotation_y(yaw)
            model_matrix.add_translation(tx, ty, tz)
            if rotate_x is not None:
                model_matrix.add_rotation_x(rotate_x)
            if rotate_y is not None:
                model_matrix.add_rotation_y(rotate_y)
            if rotate_z is not None:
                model_matrix.add_rotation_z(rotate_z)
            model_matrix.add_scale(sx, sy, sz)
            shader.set_model_matrix(model_matrix.matrix)
            shader.set_solid_color(*color)
            obj.draw(shader)
        
        # Main pole (vertical)
        draw_part(
            self.pole, self.pole_color,
            0.0, 0.0, 0.0,
            1.0, 1.0, 1.0
        )
        
        
        # Light fixtures - two rows of 3 lights each, all pointing in same direction
        pitch_angle = radians(-15)  # angled down toward the track
        
        # Top row (3 lights)
        top_row_y = self.pole_height - self.lights_height_offset
        for i in range(3):
            offset_x = (i - 1) * 0.4 * self.scale  # spread them out horizontally
            offset_z = 0.3 * self.scale            # position forward from pole center
            draw_part(
                self.light_fixture, self.light_color,
                offset_x, top_row_y, offset_z,
                1.0, 1.0, 1.0,
                rotate_x=pi/2 + pitch_angle  # horizontal + pitched down
            )
        
        # Bottom row (3 lights, slightly lower)
        bottom_row_y = top_row_y - 0.3 * self.scale
        for i in range(3):
            offset_x = (i - 1) * 0.4 * self.scale  # same horizontal spacing
            offset_z = 0.3 * self.scale            # same forward position
            draw_part(
                self.light_fixture, self.light_color,
                offset_x, bottom_row_y, offset_z,
                1.0, 1.0, 1.0,
                rotate_x=pi/2 + pitch_angle  # same angle as top row
            )

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------Pickup Objects----------------------------------------------
# ----------------------------------------------------------------------------------------------------

class Pickup:
    FILENAME = "pickup"
    def __init__(self, scale = 1.0, type = "speed_boost", color=(1.0, 0.84, 0.0)):
        self.scale = scale
        self.type = type
        self.color = color
        self.body = Sphere(bands=6)

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


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------.obj----------------------------------------------
# ----------------------------------------------------------------------------------------------------

class ObjRaceCar:
    def __init__(self, obj_filepath="obj/vehicle-speedster.obj", color=(0.2, 0.9, 0.2)):
        self.color = color
        
        # Load and cache the OBJ file
        mesh_data = MeshLoader.load_obj_and_cache(obj_filepath, "vehicle-speedster")
        
        self.position_array = mesh_data.positions
        self.normal_array = mesh_data.normals
        self.index_array = mesh_data.indices
        
        print(f"Loaded OBJ race car with {len(self.position_array)//3} vertices")
    
    def draw(self, shader, model_matrix, position, yaw=0.0):
        """Draw the car at the specified position and rotation"""
        model_matrix.load_identity()
        model_matrix.add_translation(position.x, position.y, position.z)
        model_matrix.add_rotation_y(yaw + pi)  # Add pi radians (180 degrees)
        
        # Scale the car if needed (the OBJ might be very small or large)
        model_matrix.add_scale(4.0, 4.0, 4.0)  # Adjust scale as needed
        
        shader.set_model_matrix(model_matrix.matrix)
        shader.set_solid_color(*self.color)
        
        # Set material properties
        shader.set_material_properties(32.0, 0.3)  # Some specular reflection
        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        
        if self.index_array:
            GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)
        else:
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, len(self.position_array) // 3)

# ...existing code...

class Billboard:
    def __init__(self, width=4.0, height=2.0, texture_path="rolex_banner.jpg"):
        self.width = width
        self.height = height
        self.texture_path = texture_path
        
        # Create a simple quad
        w2 = width * 0.5
        h2 = height * 0.5
        
        self.position_array = [
            -w2, -h2, 0.0,  # Bottom left
             w2, -h2, 0.0,  # Bottom right
             w2,  h2, 0.0,  # Top right
            -w2,  h2, 0.0   # Top left
        ]
        
        self.normal_array = [
            0.0, 0.0, 1.0,  # All normals facing forward
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0
        ]
        
        self.texcoord_array = [
            0.0, 0.0,  # Bottom left
            1.0, 0.0,  # Bottom right  
            1.0, 1.0,  # Top right
            0.0, 1.0   # Top left
        ]
        
        self.index_array = [0, 1, 2, 2, 3, 0]
    
    def draw(self, shader, texture_id):
        shader.set_use_texture(True)
        shader.bind_texture(texture_id)
        
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_texcoord_attribute(self.texcoord_array)
        
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)
        
        shader.set_use_texture(False)

class SimpleBillboard:
    """A simple colored billboard that doesn't require textures"""
    def __init__(self, width=4.0, height=2.0, color=(1.0, 0.0, 0.0)):
        self.width = width
        self.height = height
        self.color = color
        
        # Create a simple quad
        w2 = width * 0.5
        h2 = height * 0.5
        
        self.position_array = [
            -w2, -h2, 0.0,  # Bottom left
             w2, -h2, 0.0,  # Bottom right
             w2,  h2, 0.0,  # Top right
            -w2,  h2, 0.0   # Top left
        ]
        
        self.normal_array = [
            0.0, 0.0, 1.0,  # All normals facing forward
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0
        ]
        
        self.index_array = [0, 1, 2, 2, 3, 0]
    
    def draw(self, shader):
        shader.set_solid_color(*self.color)
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        
        GL.glDrawElements(GL.GL_TRIANGLES, len(self.index_array), GL.GL_UNSIGNED_INT, self.index_array)
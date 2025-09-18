
from math import * # trigonometry

from Base3DObjects import *

def multiply_matrices(m1, m2):
    counter = 0
    new_matrix = [0] * 16
    for row in range(4):
        for col in range(4):
            for i in range(4):
                new_matrix[counter] += m1[row*4 + i]*m2[col + 4*i]
            counter += 1
    return new_matrix

class ModelMatrix:
    def __init__(self):
        self.matrix = [ 1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1 ]
        self.stack = []
        self.stack_count = 0
        self.stack_capacity = 0

    def load_identity(self):
        self.matrix = [ 1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1 ]

    def copy_matrix(self):
        new_matrix = [0] * 16
        for i in range(16):
            new_matrix[i] = self.matrix[i]
        return new_matrix

    def add_transformation(self, matrix2):
        self.matrix = multiply_matrices(self.matrix, matrix2)

    def add_nothing(self):
        other_matrix = [1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_translation(self, tx, ty, tz):
        other_matrix = [1, 0, 0, tx,
                        0, 1, 0, ty,
                        0, 0, 1, tz,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)
    
    def add_scale(self, sx, sy, sz):
        other_matrix = [sx, 0, 0, 0,
                        0, sy, 0, 0,
                        0, 0, sz, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)
    
    def add_rotation_x(self, angle):
        c = cos(angle)
        s = sin(angle)
        other_matrix = [1, 0, 0, 0,
                        0, c, -s, 0,
                        0, s, c, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)
    
    def add_rotation_y(self, angle):
        c = cos(angle)
        s = sin(angle)
        other_matrix = [c, 0, s, 0,
                        0, 1, 0, 0,
                        -s, 0, c, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)
    
    def add_rotation_z(self, angle):
        c = cos(angle)
        s = sin(angle)
        other_matrix = [c, -s, 0, 0,
                        s, c, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    # YOU CAN TRY TO MAKE PUSH AND POP (AND COPY) LESS DEPENDANT ON GARBAGE COLLECTION
    # THAT CAN FIX SMOOTHNESS ISSUES ON SOME COMPUTERS
    def push_matrix(self):
        self.stack.append(self.copy_matrix())

    def pop_matrix(self):
        self.matrix = self.stack.pop()

    # This operation mainly for debugging
    def __str__(self):
        ret_str = ""
        counter = 0
        for _ in range(4):
            ret_str += "["
            for _ in range(4):
                ret_str += " " + str(self.matrix[counter]) + " "
                counter += 1
            ret_str += "]\n"
        return ret_str



# The ViewMatrix class holds the camera's coordinate frame and
# set's up a transformation concerning the camera's position
# and orientation

class ViewMatrix:
    def __init__(self):
        self.eye = Point(0, 0, 0)
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)

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

    def get_matrix(self):
        minusEye = Vector(-self.eye.x, -self.eye.y, -self.eye.z)
        return [self.u.x, self.u.y, self.u.z, minusEye.dot(self.u),
                self.v.x, self.v.y, self.v.z, minusEye.dot(self.v),
                self.n.x, self.n.y, self.n.z, minusEye.dot(self.n),
                0,        0,        0,        1]


# The ProjectionMatrix class builds transformations concerning
# the camera's "lens"

class ProjectionMatrix:
    def __init__(self):
        self.left = -1
        self.right = 1
        self.bottom = -1
        self.top = 1
        self.near = -1
        self.far = 1

        self.is_orthographic = True

    ## MAKE OPERATION TO SET PERSPECTIVE PROJECTION (don't forget to set is_orthographic to False) ##
    def set_perspective(self, fov, aspect, near, far):
        self.fov = fov
        self.aspect = aspect
        self.near = near
        self.far = far
        self.is_orthographic = False

    def set_orthographic(self, left, right, bottom, top, near, far):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.near = near
        self.far = far
        self.is_orthographic = True

    def get_matrix(self):
        if self.is_orthographic:
            A = 2 / (self.right - self.left)
            B = -(self.right + self.left) / (self.right - self.left)
            C = 2 / (self.top - self.bottom)
            D = -(self.top + self.bottom) / (self.top - self.bottom)
            E = 2 / (self.near - self.far)
            F = (self.near + self.far) / (self.near - self.far)

            return [A,0,0,B,
                    0,C,0,D,
                    0,0,E,F,
                    0,0,0,1]

        else:
            # Fix perspective projection formula
            f = 1.0 / tan(self.fov / 2.0)
            nf = 1.0 / (self.near - self.far)
            
            return [
                f / self.aspect, 0, 0, 0,
                0, f, 0, 0, 
                0, 0, (self.far + self.near) * nf, 2.0 * self.far * self.near * nf,
                0, 0, -1, 0
            ]

class ProjectionViewMatrix:
    def __init__(self):
        #self.matrix = [ 0.45052942369783683,  0.0,  -0.15017647456594563,  0.0,
        #        -0.10435451285616304,  0.5217725642808152,  -0.3130635385684891,  0.0,
        #        -0.2953940042189954,  -0.5907880084379908,  -0.8861820126569863,  3.082884480118567,
        #        -0.2672612419124244,  -0.5345224838248488,  -0.8017837257372732,  3.7416573867739413 ]
        self.matrix = [
            1.2990381056766582,  0.0,                     0.0,                     0.0,
            0.0,                 0.0,                    -1.7320508075688772,     0.0,
            0.0,                -1.0004000800160032,     0.0,                    79.83196639327866,
            0.0,                -1.0,                    0.0,                    80.0
        ]

    def get_matrix(self):
        return self.matrix
    
    
# class ProjectionViewMatrix:
#     def __init__(self):
#         pass

#     def get_matrix(self):
#         return [ 0.45052942369783683,  0.0,  -0.15017647456594563,  0.0,
#                 -0.10435451285616304,  0.5217725642808152,  -0.3130635385684891,  0.0,
#                 -0.2953940042189954,  -0.5907880084379908,  -0.8861820126569863,  3.082884480118567,
#                 -0.2672612419124244,  -0.5345224838248488,  -0.8017837257372732,  3.7416573867739413 ]

# IDEAS FOR OPERATIONS AND TESTING:
# if __name__ == "__main__":
#     matrix = ModelMatrix()
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_translation(3, 1, 2)
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_scale(2, 3, 4)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
    
#     matrix.add_translation(5, 5, 5)
#     matrix.push_matrix()
#     print(matrix)
#     matrix.add_scale(3, 2, 3)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
    
#     matrix.pop_matrix()
#     print(matrix)
        
#     matrix.push_matrix()
#     matrix.add_scale(2, 2, 2)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_translation(3, 3, 3)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_rotation_y(pi / 3)
#     print(matrix)
#     matrix.push_matrix()
#     matrix.add_translation(1, 1, 1)
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
#     matrix.pop_matrix()
#     print(matrix)
    

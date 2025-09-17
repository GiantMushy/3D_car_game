
from OpenGL import GL, GLU, error
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *
from Vehicle import *

class GameManager:
    CAMERA_DISTANCE = 6.0
    CAMERA_HEIGHT = 3.0
    def __init__(self, settings = {"aspect_x": 800, "aspect_y": 600, "viewport": (0,0,800,600)}):
        self.aspect_x = settings["aspect_x"]
        self.aspect_y = settings["aspect_y"]
        self.viewport = settings["viewport"]

        pygame.init() 
        pygame.display.set_mode((self.aspect_x, self.aspect_y), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()
        self.vehicle = Vehicle( {"position": Point(0,0.5,0), "direction": Vector(0,0,1), "speed": 0, "steering": 0, "color": (1.0, 0.0, 0.0, 1.0)})
        self.ground_tile = Cube()

        self.view_matrix = ViewMatrix()
        self.projection_matrix = ProjectionMatrix()

        self.projection_matrix.set_perspective(radians(60.0), self.aspect_x/self.aspect_y, 0.1, 1000.0)
        self.update_camera()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.LEFT_key_down = False
        self.RIGHT_key_down = False
        self.UP_key_down = False
        self.DOWN_key_down = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.vehicle.update(delta_time, (self.LEFT_key_down, self.RIGHT_key_down, self.UP_key_down, self.DOWN_key_down))
    
    def display(self):
        GL.glEnable(GL.GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###
        GL.glClearColor(0.1, 0.5, 1.0, 1.0) # blue background
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###
        GL.glViewport(self.viewport[0], self.viewport[1], self.viewport[2], self.viewport[3])
        
        self.display_ground()
        self.vehicle.draw(self.shader)
        self.update_camera()

        #self.debug_prints()
        pygame.display.flip()
    
    def update_camera(self):
        # Position the camera behind and above the vehicle
        self.vehicle.direction.normalize()

        cam_position = Point(
            self.vehicle.position.x - self.vehicle.direction.x * self.CAMERA_DISTANCE,
            self.vehicle.position.y + self.CAMERA_HEIGHT,
            self.vehicle.position.z - self.vehicle.direction.z * self.CAMERA_DISTANCE
        )
        look_at_position = Point(
            self.vehicle.position.x + self.vehicle.direction.x,
            self.vehicle.position.y,
            self.vehicle.position.z + self.vehicle.direction.z
        )
        up_vector = Vector(0, 1, 0)

        self.view_matrix.look_at(cam_position, look_at_position, up_vector)
        self.shader.set_projection_view_matrix(
            multiply_matrices(self.projection_matrix.get_matrix(), 
                              self.view_matrix.get_matrix()))
    
    def display_ground(self):
        grid_size = 8
        square_size = 32

        def draw_tile(x, z, color):
            self.model_matrix.load_identity()
            self.model_matrix.add_translation(x * square_size, -0.1, z * square_size)
            self.model_matrix.add_scale(square_size, 0.1, square_size)
            self.shader.set_model_matrix(self.model_matrix.matrix)
            self.shader.set_solid_color(*color)
            self.ground_tile.draw(self.shader)
        
        for x in range(-grid_size, grid_size):
            for z in range(-grid_size, grid_size):
                if (x + z) % 2 == 0:
                    draw_tile(x, z, (0.2, 0.8, 0.2))  # Light green
                else:
                    draw_tile(x, z, (0.1, 0.4, 0.1))  # Dark green

        
    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.UP_key_down = True
                    elif event.key == pygame.K_s:
                        self.DOWN_key_down = True
                    if event.key == pygame.K_a:
                        self.LEFT_key_down = True
                    elif event.key == pygame.K_d:
                        self.RIGHT_key_down = True
                    if event.key == pygame.K_ESCAPE:
                        print("Escaping!")
                        exiting = True
                        

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.UP_key_down = False
                    elif event.key == pygame.K_s:
                        self.DOWN_key_down = False
                    if event.key == pygame.K_a:
                        self.LEFT_key_down = False
                    elif event.key == pygame.K_d:
                        self.RIGHT_key_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def debug_prints(self):
        print("----------------------------------------------------------------------------------------------")
        print(f"Vehicle at: {self.vehicle.position.x}, {self.vehicle.position.y}, {self.vehicle.position.z}")
        print(f"----Camera at: {self.view_matrix.eye.x}, {self.view_matrix.eye.y}, {self.view_matrix.eye.z}")
        print("---------")
        print("Vehicle direction:", self.vehicle.direction.x, self.vehicle.direction.y, self.vehicle.direction.z)
        print("----Camera direction:", self.view_matrix.n.x, self.view_matrix.n.y, self.view_matrix.n.z)
        print("---------")
        print(f"View matrix: {self.view_matrix.get_matrix()[0:4]}")
        print(f"Projection matrix: {self.projection_matrix.get_matrix()[0:4]}")

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    settings = {"aspect_x": 800, "aspect_y": 600, "viewport": (0,0,800,600)}
    GameManager(settings).start()
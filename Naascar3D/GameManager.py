
from OpenGL import GL
from math import *

import pygame
from pygame.locals import *

from Shaders import *
from Camera import *
from Physics3D import *
from Matrices import *
from Vehicle import *
from Track import *

class GameManager:
    CAMERA_DISTANCE = 16.0
    CAMERA_HEIGHT = 5
    TRACK_NUMBER = 0

    GRID_SIZE = 8
    SQUARE_SIZE = 32.0
    ROAD_WIDTH = 16.0
    SIDELINE_WIDTH = 8.0 #(SQUARE_SIZE - ROAD_WIDTH) / 2
    def __init__(self, settings = {"aspect_x": 800, "aspect_y": 600, "viewport": (0,0,800,600), "track": 1}):
        self.settings = settings

        pygame.init() 
        pygame.display.set_mode((settings["aspect_x"], settings["aspect_y"]), pygame.OPENGL|pygame.DOUBLEBUF)
        self.shader = Shader3D()
        self.shader.use()

        self.track = Track(self.shader, {"track": self.TRACK_NUMBER, "grid_size": self.GRID_SIZE, "tile_size": self.SQUARE_SIZE, "road_width": self.ROAD_WIDTH, "sideline_width": self.SIDELINE_WIDTH})
        start_x = self.track.track["start"][0] * self.SQUARE_SIZE + self.SQUARE_SIZE/2
        start_y = self.track.track["start"][1] * self.SQUARE_SIZE + self.SQUARE_SIZE/2

        self.vehicle = Vehicle( {"position": Point(start_x, 0.5, start_y), 
                                 "direction": self.track.track["direction"], 
                                 "hitbox_size": 2.0,
                                 "speed": 0, "steering": 0, 
                                 "color": (1.0, 0.0, 0.0)})
        
        self.physics = Physics3D(self.track, self.vehicle)

        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(radians(60.0), settings["aspect_x"]/settings["aspect_y"], 0.1, 1000.0)
        self.camera = Camera(self.shader, self.projection_matrix, self.CAMERA_DISTANCE, self.CAMERA_HEIGHT)
        self.camera.update_pos(self.vehicle.position, self.vehicle.direction)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.LEFT_key_down = False
        self.RIGHT_key_down = False
        self.UP_key_down = False
        self.DOWN_key_down = False

        self.frame_count = 0

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.vehicle.update(delta_time, (self.LEFT_key_down, self.RIGHT_key_down, self.UP_key_down, self.DOWN_key_down))
        self.physics.enforce_track_bounds()
    
        self.frame_count += 1
        self.frame_count = self.frame_count % 200
        if self.frame_count == 0:
            #self.debug_prints()
            pass

    def display(self):
        GL.glEnable(GL.GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###
        GL.glClearColor(0.1, 0.5, 1.0, 1.0) # blue background
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###
        GL.glViewport(*self.settings["viewport"])

        self.track.draw()
        self.vehicle.draw(self.shader)
        self.camera.update_pos(self.vehicle.position, self.vehicle.direction)

        pygame.display.flip()
    
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
        #print(f"----Camera at: {self.view_matrix.eye.x}, {self.view_matrix.eye.y}, {self.view_matrix.eye.z}")
        #print("---------")
        print("Vehicle direction:", self.vehicle.direction.x, self.vehicle.direction.y, self.vehicle.direction.z)
        #print("----Camera direction:", self.view_matrix.n.x, self.view_matrix.n.y, self.view_matrix.n.z)
        #print("---------")
        #print(f"View matrix: {self.view_matrix.get_matrix()[0:4]}")
        #rint(f"Projection matrix: {self.projection_matrix.get_matrix()[0:4]}")

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    settings = {"aspect_x": 800, "aspect_y": 600, "viewport": (0,0,800,600), "track": 0}
    GameManager(settings).start()
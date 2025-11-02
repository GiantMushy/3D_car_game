
from OpenGL import GL
from math import *
import traceback

import pygame
from pygame.locals import *

from Shaders import *
from Matrices import *
from Camera import Camera
from UI import UI
from Pickups import Pickups
from LapCounter import LapCounter
from Physics3D import *
from Vehicle import *
from VehicleGhost import *
from Track import *

class GameManager:
    CAMERA_DISTANCE = 16.0
    CAMERA_HEIGHT = 5
    TRACK_NUMBER = 0 # CAN CHANGE THIS TO TEST OTHER TRACKS: 0, 1, 2, 3
    GRID_SIZE = 8
    SQUARE_SIZE = 32.0
    ROAD_WIDTH = 16.0
    SIDELINE_WIDTH = 8.0 #(SQUARE_SIZE - ROAD_WIDTH) / 2
    MINIMUM_TRACK_LENGTH = 16
    MAXIMUM_TRACK_LENGTH = 24 #Could take a while to load lmao

    def __init__(self, view_settings = {"aspect_x": 800, "aspect_y": 600, "viewport": (0,0,800,600)}, game_settings = {"track_number": TRACK_NUMBER}):
        self.view_settings = view_settings

        pygame.init() 
        pygame.display.set_mode((self.view_settings["aspect_x"], self.view_settings["aspect_y"]), pygame.OPENGL|pygame.DOUBLEBUF)
        self.Shader = Shader3D(use_stadium_lights=True)
        self.Shader.use()
        self.UI_Shader = Shader3D(use_stadium_lights=False)

        self.Track = Track(self.Shader, settings = {
            "track_id": game_settings["track_number"], 
            "grid_size": self.GRID_SIZE, 
            "tile_size": self.SQUARE_SIZE, 
            "road_width": self.ROAD_WIDTH, 
            "sideline_width": self.SIDELINE_WIDTH,
            "min_length": 6,
            "max_length": 12
        })
        
        starting_position = self.Track.start_coordinates()
        start_dir_x = self.Track.Grid.start.direction.x
        start_dir_y = self.Track.Grid.start.direction.y

        self.Vehicle = Vehicle( settings = {
            "position": starting_position, 
            "direction": Vector(start_dir_y,0,start_dir_x), 
            "hitbox_size": 2.0,
            "speed": 0
        })
        
        self.Ghost = Ghost( self.Track, settings = {
            "position": starting_position, 
            "direction" : Vector(start_dir_y,0,start_dir_x),
            "hitbox_size": 2.0,
            "speed" : 20
        })

        self.Physics = Physics3D(self.Track, self.Vehicle)
        self.Pickups = Pickups(self.Track, self.Vehicle)
        self.LapCounter = LapCounter(self.Track, self.Vehicle, total_laps=3)

        
        # 3D Camera
        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(radians(60.0), view_settings["aspect_x"]/view_settings["aspect_y"], 0.1, 1000.0)
        self.Camera = Camera(self.Shader, self.projection_matrix, self.Track.Grid.start.direction)
        self.Camera.update_pos(self.Vehicle.position, self.Vehicle.direction, self.Vehicle.speed)

        # 2D UI
        self.UI = UI(self.UI_Shader, self.Vehicle, self.LapCounter, view_settings)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.LEFT_key_down = False
        self.RIGHT_key_down = False
        self.UP_key_down = False
        self.DOWN_key_down = False
        self.ARROW_UP_down = False
        self.ARROW_DOWN_down = False
        self.ARROW_LEFT_down = False
        self.ARROW_RIGHT_down = False

        self.frame_count = 0

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.Vehicle.update(delta_time, (self.LEFT_key_down, self.RIGHT_key_down, self.UP_key_down, self.DOWN_key_down))
        self.Ghost.update(delta_time)
        self.Camera.update((self.ARROW_LEFT_down, self.ARROW_RIGHT_down, self.ARROW_UP_down, self.ARROW_DOWN_down), delta_time)
        self.Physics.enforce_track_bounds()
        self.Pickups.update(delta_time)
        self.LapCounter.update()
    
        self.frame_count += 1
        self.frame_count = self.frame_count % 200
        if self.frame_count == 0:
            #self.debug_positional_prints()
            pass

    def display(self):
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glClearColor(0.05, 0.1, 0.2, 1.0) # background
        GL.glClear(GL.GL_COLOR_BUFFER_BIT|GL.GL_DEPTH_BUFFER_BIT)
        GL.glViewport(*self.view_settings["viewport"])

        self.Shader.use()
        self.Camera.update_pos(self.Vehicle.position, self.Vehicle.direction, self.Vehicle.speed)
        self.Shader.set_camera_position(self.Camera.eye)

        # Set underglow position and pass to track lighting
        underglow_pos = Point(self.Vehicle.position.x, 0.2, self.Vehicle.position.z)
        self.Track.set_stadium_lighting(underglow_pos, 20.0)  # Very high intensity for testing

        # 3D scene
        self.Track.draw()
        self.Pickups.draw()
        self.Vehicle.draw(self.Shader)
        self.Ghost.draw(self.Shader)

        # 2D UI
        self.UI.draw()

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
                    elif event.key == pygame.K_UP:
                        self.ARROW_UP_down = True
                    elif event.key == pygame.K_DOWN:
                        self.ARROW_DOWN_down = True
                    elif event.key == pygame.K_LEFT:
                        self.ARROW_LEFT_down = True
                    elif event.key == pygame.K_RIGHT:
                        self.ARROW_RIGHT_down = True
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
                    elif event.key == pygame.K_UP:
                        self.ARROW_UP_down = False
                    elif event.key == pygame.K_DOWN:
                        self.ARROW_DOWN_down = False
                    elif event.key == pygame.K_LEFT:
                        self.ARROW_LEFT_down = False
                    elif event.key == pygame.K_RIGHT:
                        self.ARROW_RIGHT_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def debug_positional_prints(self):
        print("----------------------------------------------------------------------------------------------")
        print(f"Vehicle at: {self.Vehicle.position.x}, {self.Vehicle.position.y}, {self.Vehicle.position.z}")
        #print(f"----Camera at: {self.view_matrix.eye.x}, {self.view_matrix.eye.y}, {self.view_matrix.eye.z}")
        #print("---------")
        print("Vehicle direction:", self.Vehicle.direction.x, self.Vehicle.direction.y, self.Vehicle.direction.z)
        #print("----Camera direction:", self.view_matrix.n.x, self.view_matrix.n.y, self.view_matrix.n.z)
        #print("---------")
        #print(f"View matrix: {self.view_matrix.get_matrix()[0:4]}")
        #rint(f"Projection matrix: {self.projection_matrix.get_matrix()[0:4]}")

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    try:
        view_settings = {"aspect_x": 800, "aspect_y": 600, "viewport": (0,0,800,600)}
        game_settings = {"track_number": 0}
        game = GameManager(view_settings=view_settings, game_settings=game_settings)
        game.start()
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Full traceback:")
        traceback.print_exc()
        input("Press Enter to exit...")  # Keep console open to see error
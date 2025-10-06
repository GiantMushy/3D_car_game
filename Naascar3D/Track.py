from OpenGL import GL, GLU
from math import *
import pygame
from Base3DObjects import *
from Matrices import ModelMatrix

class Track:
    def __init__(self, shader, track_setup = {"track": 0, "grid_size": 8, "tile_size": 32.0, "road_width": 16.0}):
        self.model_matrix = ModelMatrix()
        self.shader = shader

        self.grid_size = track_setup["grid_size"]
        self.tile_size = track_setup["tile_size"]
        self.half_tile = self.tile_size * 0.5
        self.road_width = track_setup["road_width"]
        self.sideline_width = (track_setup["tile_size"] - track_setup["road_width"]) * 0.5

        # ----------------------------- 3D Objects for track components ----------------------------------
        self.h_wall = HorizontalWall(width=self.tile_size, height=2.0, color=(0.5,0.5,0.5))
        self.v_wall = VerticalWall(width=self.tile_size, height=2.0, color=(0.5,0.5,0.5))
        self.ground_tile = FloorTile(size=self.tile_size)
        self.h_road = HorizontalRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)
        self.v_road = VerticalRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)
        self.left_turn_road = LeftTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)
        self.right_turn_road = RightTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)
        self.down_left_turn_road = DownLeftTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)
        self.down_right_turn_road = DownRightTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)
        self.stadium_lights = StadiumLights(scale=10.0, pole_color=(0.3,0.3,0.3), light_color=(0.5,0.5,0.5))
        self.world_border = StadiumBorder(world_width=self.grid_size*self.tile_size, border_height=10.0, color=(0.5,0.5,0.5))

        self.track = {}
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.track[(x,y)] = "NA"

        self.load_track(track_setup["track"])

    def draw(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                tile_data = self.track[(x,y)]
                tile_type = tile_data[:2]
                if tile_type == "NA":
                    self.draw_ground(x, y, color = (1.0, 0.5, 0.0))
                    pass
                
                self.draw_ground(x, y, color = (0.2, 0.2, 0.2))

                if tile_type == "v0":
                    self.draw_vertical_tile(x, y)
                elif tile_type == "h0":
                    self.draw_horizontal_tile(x, y)
                elif tile_type == "d0":
                    self.draw_d0_turn_tile(x, y)
                elif tile_type == "d1":
                    self.draw_d1_turn_tile(x, y)
                elif tile_type == "d2":
                    self.draw_d2_turn_tile(x, y)
                elif tile_type == "d3":
                    self.draw_d3_turn_tile(x, y)
                elif tile_type == "v1":
                    self.draw_vertical_tile(x, y, finish_line=True)
                elif tile_type == "h1":
                    self.draw_horizontal_tile(x, y, finish_line=True)

        # Draw stadium lights at corners
        self.draw_stadium_lights(Point(0,0,0), rotation=45.0)
        self.draw_stadium_lights(Point(0,0,(self.grid_size)*self.tile_size), rotation=135.0)
        self.draw_stadium_lights(Point((self.grid_size)*self.tile_size,0,0), rotation=315.0)
        self.draw_stadium_lights(Point((self.grid_size)*self.tile_size,0,(self.grid_size)*self.tile_size), rotation=225.0)
        self.world_border.draw(self.shader, self.model_matrix)


    def draw_horizontal_tile(self, x, y, finish_line=False):
        self.draw_hwall(x, y, 0)
        self.draw_hwall(x, y, 1)
        self.set_model_matrix_and_shader(x, y, height=-0.05, centered=False)
        self.h_road.draw(self.shader)
        if finish_line:
            self.draw_finish_line(x, y)

    def draw_vertical_tile(self, x, y, finish_line=False):
        self.draw_vwall(x, y, 0)
        self.draw_vwall(x, y, 1)
        self.set_model_matrix_and_shader(x, y, height=-0.05, centered=False)
        self.v_road.draw(self.shader)
        if finish_line:
            self.draw_finish_line(x, y)

    def draw_d0_turn_tile(self, x, y):
        self.draw_hwall(x, y, 1)
        self.draw_vwall(x, y, 0)
        self.set_model_matrix_and_shader(x, y, height=-0.05, centered=False)
        self.right_turn_road.draw(self.shader)

    def draw_d1_turn_tile(self, x, y):
        self.draw_hwall(x, y, 1)
        self.draw_vwall(x, y, 1)
        self.set_model_matrix_and_shader(x, y, height=-0.05, centered=False)
        self.left_turn_road.draw(self.shader)

    def draw_d2_turn_tile(self, x, y):
        self.draw_hwall(x, y, 0)
        self.draw_vwall(x, y, 1)
        self.set_model_matrix_and_shader(x, y, height=-0.05, centered=False)
        self.down_left_turn_road.draw(self.shader)

    def draw_d3_turn_tile(self, x, y):
        self.draw_hwall(x, y, 0)
        self.draw_vwall(x, y, 0)
        self.set_model_matrix_and_shader(x, y, height=-0.05, centered=False)
        self.down_right_turn_road.draw(self.shader)

    def draw_hwall(self, grid_x, grid_y, shift = 0):
        self.model_matrix.load_identity()

        self.model_matrix.add_translation( grid_y * self.tile_size + self.tile_size * shift, # x position
                                           0.0, 
                                           grid_x * self.tile_size ) # z position

        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.h_wall.draw(self.shader)

    def draw_vwall(self, grid_x, grid_y, shift = 0):
        self.model_matrix.load_identity()

        self.model_matrix.add_translation( grid_y * self.tile_size, # x position
                                           0.0, 
                                           grid_x * self.tile_size + self.tile_size * shift ) # z position

        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.v_wall.draw(self.shader)

    def draw_ground(self, grid_x, grid_y, color):
        self.set_model_matrix_and_shader(grid_x, grid_y, height=-0.1, centered=False)
        self.shader.set_solid_color(*color)
        self.ground_tile.draw(self.shader)

    def draw_finish_line(self, grid_x, grid_y):
        self.set_model_matrix_and_shader(grid_x, grid_y, height=0.0, centered=False)
        self.finish_line.draw(self.shader)

    def draw_stadium_lights(self, position, rotation):
        rotation_radians = math.radians(rotation)
        self.stadium_lights.draw(self.shader, self.model_matrix, position, rotation_radians)

    def set_stadium_lighting(self):
        """Configure the 4 stadium lights"""
        grid_size = self.grid_size
        tile_size = self.tile_size
        light_height = 80.0  # Height of light fixtures (8.0 * scale=10.0 from StadiumLights)
        
        # Light positions
        light_positions = [
            Point(0, light_height, 0),                                    # Corner 1
            Point(0, light_height, grid_size * tile_size),               # Corner 2  
            Point(grid_size * tile_size, light_height, 0),               # Corner 3
            Point(grid_size * tile_size, light_height, grid_size * tile_size)  # Corner 4
        ]
        
        # Light colors
        light_colors = [
            (1.0, 0.95, 0.8),  # Warm white
            (1.0, 0.95, 0.8),
            (1.0, 0.95, 0.8), 
            (1.0, 0.95, 0.8)
        ]
        light_intensity = 15.0

        self.shader.set_stadium_lights(light_positions, light_colors, [light_intensity]*4)
        
        moon_direction = Vector(0.3, -0.8, 0.2)  # Coming from upper-right
        moon_direction.normalize()
        moon_color = (0.2, 0.2, 0.3)  # Cool blue moonlight
        moon_intensity = 0.1  # Subtle ambient illumination

        self.shader.set_directional_light(moon_direction, moon_color, moon_intensity)

    def set_model_matrix_and_shader(self, grid_x, grid_y, height=0.0, centered=True):
        self.model_matrix.load_identity()
        if centered:
            self.model_matrix.add_translation(  grid_y * self.tile_size + self.half_tile,
                                                height, 
                                                grid_x * self.tile_size + self.half_tile)
        else:
            self.model_matrix.add_translation(  grid_y * self.tile_size,
                                                height, 
                                                grid_x * self.tile_size)
        self.shader.set_model_matrix(self.model_matrix.matrix)

    def load_track(self, track_number):
        """
        v0 = horizontal road
        h1 = horizontal road with finish/start line
        h0 = vertical road
        v1 = vertical road with finish/start line
        d0 = 90 degree turn (bottom to right) (45 degree clockwise)
        d1 = 90 degree turn (left to bottom) (135 degree clockwise)
        d2 = 90 degree turn (top to left) (225 degree clockwise)
        d3 = 90 degree turn (right to top) (315 degree clockwise)

        """
        if track_number == 0:
            self.track = {
                (0,0) : "NA", (1,0) : "NA", (2,0) : "NA", (3,0) : "NA", (4,0) : "NA", (5,0) : "NA", (6,0) : "d3", (7,0) : "d2",
                (0,1) : "NA", (1,1) : "d3", (2,1) : "h0", (3,1) : "h0", (4,1) : "h0", (5,1) : "d2", (6,1) : "v0", (7,1) : "v0s",
                (0,2) : "NA", (1,2) : "d0", (2,2) : "d2", (3,2) : "NA", (4,2) : "d3", (5,2) : "d1", (6,2) : "v0", (7,2) : "v0",
                (0,3) : "NA", (1,3) : "NA", (2,3) : "v1", (3,3) : "NA", (4,3) : "v0", (5,3) : "NA", (6,3) : "v0", (7,3) : "v0",
                (0,4) : "NA", (1,4) : "NA", (2,4) : "v0b", (3,4) : "NA", (4,4) : "v0", (5,4) : "d3", (6,4) : "d1", (7,4) : "v0",
                (0,5) : "NA", (1,5) : "d3", (2,5) : "d1", (3,5) : "NA", (4,5) : "d0", (5,5) : "d1", (6,5) : "NA", (7,5) : "v0",
                (0,6) : "NA", (1,6) : "v0", (2,6) : "NA", (3,6) : "NA", (4,6) : "d3", (5,6) : "d2", (6,6) : "NA", (7,6) : "v0b",
                (0,7) : "NA", (1,7) : "d0", (2,7) : "h0d", (3,7) : "h0", (4,7) : "d1", (5,7) : "d0", (6,7) : "h0", (7,7) : "d1",
                "start" : (2,3), "direction" : Vector(1,0,0)}
            
            self.finish_line = FinishLine(road_width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, horizontal=False)
        
        elif track_number == 1:
            self.track = {
                (0,0) : "d3", (1,0) : "h1",(2,0) : "h0", (3,0) : "h0", (4,0) : "h0d",(5,0) : "h0", (6,0) : "h0", (7,0) : "d2",
                (0,1) : "v0", (1,1) : "NA", (2,1) : "NA", (3,1) : "NA", (4,1) : "NA", (5,1) : "NA", (6,1) : "NA", (7,1) : "v0",
                (0,2) : "v0", (1,2) : "NA", (2,2) : "NA", (3,2) : "NA", (4,2) : "NA", (5,2) : "NA", (6,2) : "NA", (7,2) : "v0",
                (0,3) : "v0", (1,3) : "NA", (2,3) : "NA", (3,3) : "NA", (4,3) : "NA", (5,3) : "NA", (6,3) : "NA", (7,3) : "v0",
                (0,4) : "v0", (1,4) : "NA", (2,4) : "NA", (3,4) : "NA", (4,4) : "NA", (5,4) : "NA", (6,4) : "NA", (7,4) : "v0",
                (0,5) : "v0", (1,5) : "NA", (2,5) : "NA", (3,5) : "NA", (4,5) : "NA", (5,5) : "NA", (6,5) : "NA", (7,5) : "v0",
                (0,6) : "v0", (1,6) : "NA", (2,6) : "NA", (3,6) : "NA", (4,6) : "NA", (5,6) : "NA", (6,6) : "NA", (7,6) : "v0",
                (0,7) : "d0b",(1,7) : "h0", (2,7) : "h0", (3,7) : "h0", (4,7) : "h0", (5,7) : "h0", (6,7) : "h0s",(7,7) : "d1",
                "start" : (1,0), "direction" : Vector(0,0,-1)}

            self.finish_line = FinishLine(road_width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, horizontal=True)
        
        elif track_number == 2:
            self.track = {
                (0,0) : "d3", (1,0) : "h0b",(2,0) : "d2", (3,0) : "NA", (4,0) : "NA", (5,0) : "NA", (6,0) : "NA", (7,0) : "NA",
                (0,1) : "v1",(1,1) : "NA", (2,1) : "v0d",(3,1) : "NA", (4,1) : "NA", (5,1) : "NA", (6,1) : "NA", (7,1) : "NA",
                (0,2) : "d0", (1,2) : "h0s",(2,2) : "d1", (3,2) : "NA", (4,2) : "NA", (5,2) : "NA", (6,2) : "NA", (7,2) : "NA",
                (0,3) : "NA", (1,3) : "NA", (2,3) : "NA", (3,3) : "NA", (4,3) : "NA", (5,3) : "NA", (6,3) : "NA", (7,3) : "NA",
                (0,4) : "NA", (1,4) : "NA", (2,4) : "NA", (3,4) : "NA", (4,4) : "NA", (5,4) : "NA", (6,4) : "NA", (7,4) : "NA",
                (0,5) : "NA", (1,5) : "NA", (2,5) : "NA", (3,5) : "NA", (4,5) : "NA", (5,5) : "NA", (6,5) : "NA", (7,5) : "NA",
                (0,6) : "NA", (1,6) : "NA", (2,6) : "NA", (3,6) : "NA", (4,6) : "NA", (5,6) : "NA", (6,6) : "NA", (7,6) : "NA",
                (0,7) : "NA", (1,7) : "NA", (2,7) : "NA", (3,7) : "NA", (4,7) : "NA", (5,7) : "NA", (6,7) : "NA", (7,7) : "NA",
                "start" : (0,1), "direction" : Vector(1,0,0)}
            
            self.finish_line = FinishLine(road_width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, horizontal=False)
        
        elif track_number == 3:
            self.track = {
                (0,0) : "d3", (1,0) : "h1",(2,0) : "d2", (3,0) : "NA", (4,0) : "NA", (5,0) : "NA", (6,0) : "NA", (7,0) : "NA",
                (0,1) : "v0b",(1,1) : "NA", (2,1) : "v0b",(3,1) : "NA", (4,1) : "NA", (5,1) : "NA", (6,1) : "NA", (7,1) : "NA",
                (0,2) : "d0", (1,2) : "h0b",(2,2) : "d1", (3,2) : "NA", (4,2) : "NA", (5,2) : "NA", (6,2) : "NA", (7,2) : "NA",
                (0,3) : "NA", (1,3) : "NA", (2,3) : "NA", (3,3) : "NA", (4,3) : "NA", (5,3) : "NA", (6,3) : "NA", (7,3) : "NA",
                (0,4) : "NA", (1,4) : "NA", (2,4) : "NA", (3,4) : "NA", (4,4) : "NA", (5,4) : "NA", (6,4) : "NA", (7,4) : "NA",
                (0,5) : "NA", (1,5) : "NA", (2,5) : "NA", (3,5) : "NA", (4,5) : "NA", (5,5) : "NA", (6,5) : "NA", (7,5) : "NA",
                (0,6) : "NA", (1,6) : "NA", (2,6) : "NA", (3,6) : "NA", (4,6) : "NA", (5,6) : "NA", (6,6) : "NA", (7,6) : "NA",
                (0,7) : "NA", (1,7) : "NA", (2,7) : "NA", (3,7) : "NA", (4,7) : "NA", (5,7) : "NA", (6,7) : "NA", (7,7) : "NA",
                "start" : (0,0), "direction" : Vector(0,0,1)}
            self.finish_line = FinishLine(road_width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, horizontal=True)

    def get_track_type(self, x, y):
        return self.track[(x, y)]
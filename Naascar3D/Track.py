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
        self.half_grid = self.grid_size * 0.5
        self.tile_size = track_setup["tile_size"]
        self.road_width = track_setup["road_width"]
        self.sideline_width = (track_setup["tile_size"] - track_setup["road_width"]) * 0.5

        # ----------------------------- 3D Objects for track components ----------------------------------
        self.h_wall = HorizontalWall(width=self.tile_size, height=2.0, color=(0.5,0.5,0.5))
        self.v_wall = VerticalWall(width=self.tile_size, height=2.0, color=(0.1,0.1,0.1))
        self.ground_tile = FloorTile(size=self.tile_size, color=(0.0, 0.5, 0.0))
        self.finish_line = FinishLine(width=self.road_width, height=0.2, color=(1.0,1.0,1.0))
        self.h_road = HorizontalRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, color=(0.2,0.2,0.2))
        self.v_road = VerticalRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, color=(0.2,0.2,0.2))
        self.left_turn_road = LeftTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, color=(0.2,0.2,0.2))
        self.right_turn_road = RightTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, color=(0.2,0.2,0.2))
        self.down_left_turn_road = DownLeftTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, color=(0.2,0.2,0.2))
        self.down_right_turn_road = DownRightTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, color=(0.2,0.2,0.2))

        self.track = {}
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.track[(x,y)] = "null"

        self.load_track(track_setup["track"])

    def draw(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.track[(x,y)] == "null":
                    self.draw_ground(x, y, color = (1.0, 0.5, 0.0))
                    pass
                
                self.draw_ground(x, y, color = (0.2, 0.2, 0.2))

                if self.track[(x,y)] == "v0":
                    self.draw_v0(x, y)
                elif self.track[(x,y)] == "h0":
                    self.draw_h0(x, y)
                elif self.track[(x,y)] == "d0":
                    self.draw_d0(x, y)
                elif self.track[(x,y)] == "d1":
                    self.draw_d1(x, y)
                elif self.track[(x,y)] == "d2":
                    self.draw_d2(x, y)
                elif self.track[(x,y)] == "d3":
                    self.draw_d3(x, y)
                elif self.track[(x,y)] == "v1":
                    self.draw_v1(x, y)
                elif self.track[(x,y)] == "h1":
                    self.draw_h1(x, y)

    def draw_h0(self, x, y):
        self.draw_hwall(x, y, 0)
        self.draw_hwall(x, y, 1)
        self.draw_hroad(x, y)

    def draw_h1(self, x, y):
        self.draw_hwall(x, y, 0)
        self.draw_hwall(x, y, 1)
        self.draw_hroad(x, y)
        self.draw_finish_line(x, y, horizontal=True)

    def draw_v0(self, x, y):
        self.draw_vwall(x, y, 0)
        self.draw_vwall(x, y, 1)
        self.draw_vroad(x, y)

    def draw_v1(self, x, y):
        self.draw_vwall(x, y, 0)
        self.draw_vwall(x, y, 1)
        self.draw_vroad(x, y)
        self.draw_finish_line(x, y, horizontal=False)

    def draw_d0(self, x, y):
        self.draw_hwall(x, y, 1)
        self.draw_vwall(x, y, 0)
        self.draw_right_turn_road(x, y)

    def draw_d1(self, x, y):
        self.draw_hwall(x, y, 1)
        self.draw_vwall(x, y, 1)
        self.draw_left_turn_road(x, y)

    def draw_d2(self, x, y):
        self.draw_hwall(x, y, 0)
        self.draw_vwall(x, y, 1)
        self.draw_down_left_turn_road(x, y)

    def draw_d3(self, x, y):
        self.draw_hwall(x, y, 0)
        self.draw_vwall(x, y, 0)
        self.draw_down_right_turn_road(x, y)

    def draw_hwall(self, grid_x, grid_y, shift = 0):
        self.model_matrix.load_identity()

        xPos = grid_y * self.tile_size + self.tile_size * shift
        zPos = grid_x * self.tile_size

        self.model_matrix.add_translation( xPos, 0.0, zPos )

        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.h_wall.draw(self.shader)

    def draw_vwall(self, grid_x, grid_y, shift = 0):
        self.model_matrix.load_identity()

        xPos = grid_y * self.tile_size
        zPos = grid_x * self.tile_size + self.tile_size * shift

        self.model_matrix.add_translation( xPos, 0.0, zPos )

        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.v_wall.draw(self.shader)

    def draw_hroad(self, grid_x, grid_y):
        self.set_model_matrix_and_shader(grid_x, grid_y, height=-0.05)
        self.h_road.draw(self.shader)

    def draw_vroad(self, grid_x, grid_y):
        self.set_model_matrix_and_shader(grid_x, grid_y, height=-0.05)
        self.v_road.draw(self.shader)

    def draw_finish_line(self, grid_x, grid_y, horizontal=True):
        self.set_model_matrix_and_shader(grid_x, grid_y, height=0.0)
        self.finish_line.draw(self.shader)

    def draw_left_turn_road(self, grid_x, grid_y):
        self.set_model_matrix_and_shader(grid_x, grid_y, height=-0.05)
        self.left_turn_road.draw(self.shader)

    def draw_right_turn_road(self, grid_x, grid_y):
        self.set_model_matrix_and_shader(grid_x, grid_y, height=-0.05)
        self.right_turn_road.draw(self.shader)

    def draw_down_left_turn_road(self, grid_x, grid_y):
        self.set_model_matrix_and_shader(grid_x, grid_y, height=-0.05)
        self.down_left_turn_road.draw(self.shader)

    def draw_down_right_turn_road(self, grid_x, grid_y):
        self.set_model_matrix_and_shader(grid_x, grid_y, height=-0.05)
        self.down_right_turn_road.draw(self.shader)

    def draw_ground(self, grid_x, grid_y, color):
        self.set_model_matrix_and_shader(grid_x, grid_y, height=-0.1)
        self.shader.set_solid_color(*color)
        self.ground_tile.draw(self.shader)

    def set_model_matrix_and_shader(self, grid_x, grid_y, height=0.0):
        self.model_matrix.load_identity()
        self.model_matrix.add_translation(  grid_y * self.tile_size + self.half_grid,
                                            height, 
                                            grid_x * self.tile_size + self.half_grid)
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
                (0,0) : "null", (1,0) : "null", (2,0) : "null", (3,0) : "null", (4,0) : "null", (5,0) : "null", (6,0) : "d3",   (7,0) : "d2",
                (0,1) : "null", (1,1) : "d3",   (2,1) : "h0",   (3,1) : "h0",   (4,1) : "h0",   (5,1) : "d2",   (6,1) : "v0",   (7,1) : "v0",
                (0,2) : "null", (1,2) : "d0",   (2,2) : "d2",   (3,2) : "null", (4,2) : "d3",   (5,2) : "d1",   (6,2) : "v0",   (7,2) : "v0",
                (0,3) : "null", (1,3) : "null", (2,3) : "v1",   (3,3) : "null", (4,3) : "v0",   (5,3) : "null", (6,3) : "v0",   (7,3) : "v0",
                (0,4) : "null", (1,4) : "null", (2,4) : "v0",   (3,4) : "null", (4,4) : "v0",   (5,4) : "d3",   (6,4) : "d1",   (7,4) : "v0",
                (0,5) : "null", (1,5) : "d3",   (2,5) : "d1",   (3,5) : "null", (4,5) : "d0",   (5,5) : "d1",   (6,5) : "null", (7,5) : "v0",
                (0,6) : "null", (1,6) : "v0",   (2,6) : "null", (3,6) : "null", (4,6) : "d3",   (5,6) : "d2",   (6,6) : "null", (7,6) : "v0",
                (0,7) : "null", (1,7) : "d0",   (2,7) : "h0",   (3,7) : "h0",   (4,7) : "d1",   (5,7) : "d0",   (6,7) : "h0",   (7,7) : "d1",
                "start" : (1,3), "direction" : Vector(1,0,0)}
        
        elif track_number == 1:
            self.track = {
                (0,0) : "d3", (1,0) : "h0",   (2,0) : "h0",   (3,0) : "h0",   (4,0) : "h0",   (5,0) : "h0",   (6,0) : "h0",   (7,0) : "d2",
                (0,1) : "v0", (1,1) : "null", (2,1) : "null", (3,1) : "null", (4,1) : "null", (5,1) : "null", (6,1) : "null", (7,1) : "v0",
                (0,2) : "v0", (1,2) : "null", (2,2) : "null", (3,2) : "null", (4,2) : "null", (5,2) : "null", (6,2) : "null", (7,2) : "v0",
                (0,3) : "v0", (1,3) : "null", (2,3) : "null", (3,3) : "null", (4,3) : "null", (5,3) : "null", (6,3) : "null", (7,3) : "v0",
                (0,4) : "v0", (1,4) : "null", (2,4) : "null", (3,4) : "null", (4,4) : "null", (5,4) : "null", (6,4) : "null", (7,4) : "v0",
                (0,5) : "v0", (1,5) : "null", (2,5) : "null", (3,5) : "null", (4,5) : "null", (5,5) : "null", (6,5) : "null", (7,5) : "v0",
                (0,6) : "v0", (1,6) : "null", (2,6) : "null", (3,6) : "null", (4,6) : "null", (5,6) : "null", (6,6) : "null", (7,6) : "v0",
                (0,7) : "d0", (1,7) : "h0",   (2,7) : "h0",   (3,7) : "h0",   (4,7) : "h0",   (5,7) : "h0",   (6,7) : "h0",   (7,7) : "d1",
                "start" : (0,2), "direction" : Vector(0,0,-1)}
        elif track_number == 2:
            self.track = {
                (0,0) : "d3",   (1,0) : "h0",   (2,0) : "h0",   (3,0) : "d2",   (4,0) : "null", (5,0) : "null", (6,0) : "null", (7,0) : "null",
                (0,1) : "v0",   (1,1) : "null", (2,1) : "null", (3,1) : "v0",   (4,1) : "null", (5,1) : "null", (6,1) : "null", (7,1) : "null",
                (0,2) : "v0",   (1,2) : "null", (2,2) : "null", (3,2) : "v0",   (4,2) : "null", (5,2) : "null", (6,2) : "null", (7,2) : "null",
                (0,3) : "d0",   (1,3) : "h0",   (2,3) : "h0",   (3,3) : "d1",   (4,3) : "null", (5,3) : "null", (6,3) : "null", (7,3) : "null",
                (0,4) : "null", (1,4) : "null", (2,4) : "null", (3,4) : "null", (4,4) : "null", (5,4) : "null", (6,4) : "null", (7,4) : "null",
                (0,5) : "null", (1,5) : "null", (2,5) : "null", (3,5) : "null", (4,5) : "null", (5,5) : "null", (6,5) : "null", (7,5) : "null",
                (0,6) : "null", (1,6) : "null", (2,6) : "null", (3,6) : "null", (4,6) : "null", (5,6) : "null", (6,6) : "null", (7,6) : "null",
                (0,7) : "null", (1,7) : "null", (2,7) : "null", (3,7) : "null", (4,7) : "null", (5,7) : "null", (6,7) : "null", (7,7) : "null",
                "start" : (0,0), "direction" : Vector(1,0,0)}

    def get_track_type(self, x, y):
        return self.track[(x, y)]
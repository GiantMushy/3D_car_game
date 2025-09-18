from OpenGL import GL, GLU
from math import *
import pygame
from Base3DObjects import FloorTile, HorizontalWall, Vector, VerticalWall
from Shaders import Shader3D
from Matrices import ModelMatrix

class Track:
    def __init__(self, track_setup = {"track": 0, "grid_size": 8, "tile_size": 32.0, "road_width": 16.0, "sideline_width": 8.0}):
        self.shader = Shader3D()
        self.model_matrix = ModelMatrix()

        self.grid_size = track_setup["grid_size"]
        self.tile_size = track_setup["tile_size"]
        self.road_width = track_setup["road_width"]

        self.h_wall = HorizontalWall(width=self.tile_size, height=1.0, color=(0.5,0.5,0.5))
        self.v_wall = VerticalWall(width=self.tile_size, height=1.0, color=(0.1,0.1,0.1))
        self.ground_tile = FloorTile(size=self.tile_size, color=(0.0, 0.5, 0.0))

        self.track = {}
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.track[(x,y)] = "null"

        self.load_track(track_setup["track"])

    def draw(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.track[(x,y)] != "null":
                    self.draw_ground(x, y, color = (0.2, 0.2, 0.2))
                else:                           
                    self.draw_ground(x, y, color = (0.0, 0.5, 0.0))
                    pass

                if self.track[(x,y)] == "h0":
                    self.draw_h0(x, y)
                elif self.track[(x,y)] == "v0":
                    self.draw_v0(x, y)
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
        self.draw_hwall(x, y)
        self.draw_hwall(x, y, 1)

    def draw_h1(self, x, y):
        self.draw_hwall(x, y)
        self.draw_hwall(x, y, 1)
        # finish line

    def draw_v0(self, x, y):
        self.draw_vwall(x, y)
        self.draw_vwall(x, y, 1)

    def draw_v1(self, x, y):
        self.draw_vwall(x, y)
        self.draw_vwall(x, y, 1)
        # finish line

    def draw_d0(self, x, y):
        self.draw_hwall(x, y)
        self.draw_vwall(x, y, 1)

    def draw_d1(self, x, y):
        self.draw_hwall(x, y, 1)
        self.draw_vwall(x, y, 1)

    def draw_d2(self, x, y):
        self.draw_hwall(x, y)
        self.draw_vwall(x, y, 1)

    def draw_d3(self, x, y):
        self.draw_hwall(x, y)
        self.draw_vwall(x, y)

    def draw_hwall(self, grid_x, grid_y, shift = 0):
        self.model_matrix.load_identity()

        xPos = grid_x * self.tile_size + self.road_width
        zPos = grid_y * self.tile_size + self.tile_size * shift
        self.model_matrix.add_translation( xPos, 1.0, zPos )

        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.h_wall.draw(self.shader)

    def draw_vwall(self, grid_x, grid_y, shift = 0):
        self.model_matrix.load_identity()

        xPos = grid_x * self.tile_size + self.tile_size * shift
        zPos = grid_y * self.tile_size + self.road_width
        self.model_matrix.add_translation( xPos, 1.0, zPos )

        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.v_wall.draw(self.shader)

    def draw_ground(self, grid_x, grid_y, color):
        self.model_matrix.load_identity()
        self.model_matrix.add_translation(grid_x * self.tile_size, -0.1, grid_y * self.tile_size)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_solid_color(*color)
        self.ground_tile.draw(self.shader)

    def load_track(self, track_number):
        """
        h0 = horizontal road
        h1 = horizontal road with finish/start line
        v0 = vertical road
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
                "start" : (2,3), "direction" : Vector(0,0,-1)}
        
        elif track_number == 1:
            self.track = {
                (0,0) : "d3", (1,0) : "h0",   (2,0) : "h0",   (3,0) : "h0",   (4,0) : "h0",   (5,0) : "h0",   (6,0) : "h0",   (7,0) : "d2",
                (0,1) : "v0", (1,1) : "null", (2,1) : "null", (3,1) : "null", (4,1) : "null", (5,1) : "null", (6,1) : "null", (7,1) : "v0",
                (0,2) : "v1", (1,2) : "null", (2,2) : "null", (3,2) : "null", (4,2) : "null", (5,2) : "null", (6,2) : "null", (7,2) : "v0",
                (0,3) : "v0", (1,3) : "null", (2,3) : "null", (3,3) : "null", (4,3) : "null", (5,3) : "null", (6,3) : "null", (7,3) : "v0",
                (0,4) : "v0", (1,4) : "null", (2,4) : "null", (3,4) : "null", (4,4) : "null", (5,4) : "null", (6,4) : "null", (7,4) : "v0",
                (0,5) : "v0", (1,5) : "null", (2,5) : "null", (3,5) : "null", (4,5) : "null", (5,5) : "null", (6,5) : "null", (7,5) : "v0",
                (0,6) : "v0", (1,6) : "null", (2,6) : "null", (3,6) : "null", (4,6) : "null", (5,6) : "null", (6,6) : "null", (7,6) : "v0",
                (0,7) : "d0", (1,7) : "h0",   (2,7) : "h0",   (3,7) : "h0",   (4,7) : "h0",   (5,7) : "h0",   (6,7) : "h0",   (7,7) : "d1",
                "start" : (0,2), "direction" : Vector(0,0,-1)}


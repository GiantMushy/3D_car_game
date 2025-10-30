import os
from OpenGL import GL, GLU
from math import *
from random import *
import pygame
from Base3DObjects import *
from Matrices import ModelMatrix
from Grid import Grid

class Track:
    TRACK_MAX_LENGTH = 16
    TRACK_MIN_LENGTH = 6

    def __init__(self, shader, settings = {"track_id": 0, "grid_size": 8, "tile_size": 32.0, "road_width": 16.0, "min_length": 16, "max_length": 24}):
        self.model_matrix = ModelMatrix()
        self.shader = shader

        self.grid_size = settings["grid_size"]
        self.tile_size = settings["tile_size"]
        self.half_tile = self.tile_size * 0.5
        self.road_width = settings["road_width"]
        self.sideline_width = (settings["tile_size"] - settings["road_width"]) * 0.5

        # ----------------------------- 3D Objects for track components ----------------------------------
        self.ground_tile = FloorTile(size=self.tile_size)

        self.h_wall = HorizontalWall(width=self.tile_size, height=2.0, color=(0.5,0.5,0.5))
        self.v_wall = VerticalWall(width=self.tile_size, height=2.0, color=(0.5,0.5,0.5))
        self.h_road = HorizontalRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)
        self.v_road = VerticalRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)

        self.left_turn_road =       LeftTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)
        self.right_turn_road =      RightTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)
        self.down_left_turn_road =  DownLeftTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)
        self.down_right_turn_road = DownRightTurnRoad(width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width)
        
        self.stadium_lights = StadiumLights(scale=10.0, pole_color=(0.3,0.3,0.3), light_color=(0.5,0.5,0.5))
        self.world_border = StadiumBorder(world_width=self.grid_size*self.tile_size, border_height=10.0, color=(0.5,0.5,0.5))
        self.set_stadium_lighting()

        # ---------------------------------------- Track Layout -----------------------------------------
        self.Grid = Grid(settings = {
            "size": settings["grid_size"], 
            "min_length": settings["min_length"], 
            "max_length": settings["max_length"]
        })
        self.load_track(settings["track_id"])
    
    def get_cell(self, pos):
        return self.Grid.get_cell(pos)
    
    def get_cell_type(self, pos):
        cell = self.get_cell(pos)
        if cell: return cell.type
        return None

    def get_cell_powerup(self, pos):
        cell = self.get_cell(pos)
        if cell: return cell.powerup
        return None
        
    def get_cell_direction(self, pos):
        cell = self.get_cell(pos)
        return cell.direction
    
    def get_start_postion(self):
        return self.Grid.start.position
    
    def grid_pos_to_coords(self, pos):
        ''' 
        Translates the grid's (x,y) position (x and y are between 0 and self.grid_size) to the games real world (x,y) coordinates
        returns the coordinates of the center of the cell
        '''
        x = pos.x * self.tile_size + self.tile_size/2
        y = pos.y * self.tile_size + self.tile_size/2
        return Point(y, 0, x) # (x, y, z)
        
    def start_coordinates(self):
        return self.Grid.start.real_center
    
    def set_cells_real_coords(self):
        cell = self.Grid.start
        pos = Coordinate(cell.x, cell.y)
        cell.real_center = self.grid_pos_to_coords(pos)
        cell.real_enter = self.grid_pos_to_coords(pos - cell.direction)
        cell.real_exit = self.grid_pos_to_coords(pos + cell.direction)
        
        prev = cell
        for _ in range(self.Grid.length):
            cell = cell.next
            pos = Coordinate(cell.x, cell.y)
            cell.real_center = self.grid_pos_to_coords(pos)
            cell.real_enter = self.grid_pos_to_coords(pos - prev.direction)
            cell.real_exit = self.grid_pos_to_coords(pos + cell.direction)

            prev = cell

    def draw(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                tile_type = self.get_cell_type(Coordinate(x,y))
                if tile_type == "XX":
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


    # ------------------------------- MAP GENERATION -------------------------------
    def load_track(self, track_number):
        if track_number == 0:
            self.Grid.generate_random_track()

        if track_number == 1:
            self.Grid.load_preset({"start" : Coordinate(2,3), "direction" : Coordinate(1,0), "layout": [
                "v1", "v0b", "d1", "d3", "v0", "d0", "h0d", "h0", "d1", "d3", "d2", "d0", "h0", 
                "d1", "v0b", "v0", "v0", "v0", "v0", "v0s", "d2", "d3", "v0", "v0", "v0", "d1",
                "d3", "d1", "d0", "v0", "v0", "d3", "d1", "d2", "h0", "h0", "h0", "d3", "d0", "d2"]})
        
        elif track_number == 2:
            self.Grid.load_preset({"start" : Coordinate(1,0), "direction" : Coordinate(0, -1), "layout": [
                "h1", "h0", "h0", "h0", "h0", "h0", "d2", "v0", "v0", "v0", "v0", "v0", "v0", "d1", 
                "h0", "h0", "h0", "h0", "h0", "j0", "d0", "v0", "v0", "v0", "v0", "v0", "v0", "d3"]})
        
        elif track_number == 3:
            self.Grid.load_preset({"start" : Coordinate(0,1), "direction" : Coordinate(1,0), "layout" : [
                "v1", "d3", "h0", "d2", "v0", "d1", "h0", "d0"]})
        
        self.set_cells_real_coords()
        self.finish_line = FinishLine(road_width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, horizontal=(self.Grid.start.type[0] == 'h'))

    def draw_track_debug(self):
        '''
        Draws the track in text format with starting position marked as 'S'
        '''
        print(self.Grid)

if __name__ == "__main__":
    grid = Grid()
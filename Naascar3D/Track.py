import os
from OpenGL import GL, GLU
from math import *
from random import *
import pygame
from Base3DObjects import *
from Matrices import ModelMatrix


class Cell:
    ''' 
    Node for the Track's grid. Each node contains the following data:

    position:
        (x,y)
    type:
        v0 = vertical road without finish line
        h0 = horizontal road without finish line
        v1 = vertical road with finish line
        h1 = horizontal road with finish line
        d1 = 90 degree turn (bottom to right) (45 degree clockwise)
        d2 = 90 degree turn (left to bottom) (135 degree clockwise)
        d3 = 90 degree turn (top to left) (225 degree clockwise)
        d4 = 90 degree turn (right to top) (315 degree clockwise)
    exit_direction:
        ( 0, 1) = north
        ( 0,-1) = south
        ( 1, 0) = east
        (-1, 0) = west
    powerup:
        b = boost
        s = slow
        d = disable
    '''
    def __init__(self, position=(0,0), type="XX", next=None, direction=None, powerup=None):
        self.position = position
        self.type = type
        self.next = next
        self.direction = direction
        self.powerup = powerup

    def set_type(self, type):
        self.type = type

    def type(self):
        return self.tile_type
    
    def set_direction(self, direction):
        self.direction = direction
    
    def direction(self):
        return self.direction
    
    def set_powerup(self, powerup):
        self.powerup = powerup
    
    def powerup(self):
        return self.powerup
    
    def set_next(self, next_cell):
        self.next = next_cell
    
    def next(self):
        return self.next
    
    def __str__(self):
        if self.type == "XX":
            return "   "
        elif self.type == "v0":
            return " | "
        elif self.type == "v1":
            return "s| "
        elif self.type == "h0":
            return "---"
        elif self.type == "h1":
            return "-s-"
        elif self.type == "d0":
            return " ┌ "
        elif self.type == "d1":
            return " ┐ "
        elif self.type == "d2":
            return " ┘ "
        elif self.type == "d3":
            return " └ "
        else:
            return "OO"

class Grid:
    TRACK_TYPE_FOR_DIRECTIONAL_CHANGE = {
        (( 1, 0), ( 1, 0)): 'h0',
        (( 1, 0), ( 0, 1)): 'd2',
        (( 1, 0), ( 0,-1)): 'd1',
        (( 1, 0), (-1, 0)): 'x',

        ((-1, 0), (-1, 0)): 'h0',
        ((-1, 0), ( 0, 1)): 'd3',
        ((-1, 0), ( 0,-1)): 'd0',
        ((-1, 0), ( 1, 0)): 'x',

        (( 0, 1), ( 0, 1)): 'v0',
        (( 0, 1), ( 1, 0)): 'd0',
        (( 0, 1), (-1, 0)): 'd1',
        (( 0, 1), ( 0,-1)): 'x',

        (( 0,-1), ( 0,-1)): 'v0',
        (( 0,-1), ( 1, 0)): 'd3',
        (( 0,-1), (-1, 0)): 'd2',
        (( 0,-1), ( 0, 1)): 'x'
    }

    def __init__(self, settings = {"size":8, "min_length":10, "max_length":16}):
        self.size = settings["size"]
        self.start = None
        self.min_length = settings["min_length"]
        self.max_length = settings["max_length"]
        self.length = 1
        self.cells = {}
        for x in range(self.size):
            for y in range(self.size):
                self.cells[(x,y)] = Cell(position=(x,y), type="XX")
    
    def get_cell(self, position):
        return self.cells.get(position, None)
    
    def add_positions(self, pos1, pos2):
        return (pos1[0] + pos2[0], pos1[1] + pos2[1])
    
    def get_start(self):
        return self.start
    
    def set_random_start(self):
        x = randint(0, self.size - 1)
        y = randint(0, self.size - 1)

        # Prevent corners
        if (x == 0 and (y == 0 or y == self.size - 1)):
            x += 1
        elif (y == 0 and (x == 0 or x == self.size - 1)):
            y += 1

        self.start = self.get_cell((x, y))
        # Determine valid tile types based on position
        if   x == 0 or x == self.size - 1: # Left or right edge
            self.start.direction = (0,1)  # Facing North
        elif y == 0 or y == self.size - 1: # Top or bottom edge  
            self.start.direction = (1,0)  # Facing East
        else:  # Interior
            self.start.direction = choice( [(1,0), (0,1)] )  # Randomly choose North or East
        
        self.start.set_type("v1" if self.start.direction == (0,1) else "h1")
        next_pos = self.add_positions(self.start.position, self.start.direction)
        self.start.next = self.get_cell(next_pos)
    
    def bounds_check(self, position):
        return position[0] >= 0 and position[0] < self.size and position[1] >= 0 and position[1] < self.size
    
    def is_cell_empty(self, pos):
        cell = self.get_cell(pos)
        return cell is not None and cell.type == "XX"
    
    def reached_end_check(self, pos, direction, length):
        if pos == self.start.position:
            if direction == self.start.direction:
                if length >= self.min_length and length <= self.max_length:
                    return True
        return False
    
    def generate_random_track(self):
        self.set_random_start()

        self.dfs(self.start.next, self.start.direction, 1)
        print(self)
    
    def dfs(self, cell, old_direction, length):
        directions = [ (0,1), (1,0), (0,-1), (-1,0) ]  # N, E, S, W
        shuffle(directions)  # make genereration random

        if length <= self.max_length:
            for new_direction in directions:
                cell.type = self.TRACK_TYPE_FOR_DIRECTIONAL_CHANGE[(old_direction, new_direction)]
                cell.direction = new_direction
                next_pos = self.add_positions(cell.position, cell.direction)
                cell.next = self.get_cell(next_pos)
                
                print(f"----------- Current Attempt = [next_pos: {next_pos} , next_dir: {new_direction} , length: {length}] -----------")
                print(self)
     
                if self.reached_end_check(next_pos, cell.direction, length):
                    print("Found HAHA!")
                    self.length += 1
                    print(self)
                    return True
                
                elif self.bounds_check(next_pos) and self.is_cell_empty(next_pos) and cell.type != "x": # check if the propsed direction is valid
                    if self.dfs(cell.next, cell.direction, length + 1):
                        print("Found!!!" + f"length: {length}")
                        print(self)
                        self.length += 1
                        return True
                
                cell.direction = None
                cell.type = "XX"
                cell.next = None

        return False
    
    def load_preset(data):
        pass

    def __str__(self):
        #os.system('cls' if os.name == 'nt' else 'clear')
        output = []
        for y in range(self.size):
            output.append([])
            for x in range(self.size):
                node = self.get_cell((x,self.size - 1 - y))
                output[y].append(str(node))

        
        ret = "  ──────────────────────────────────────────────\n"
        for n in range(self.size):
            ret += f"{self.size - 1 - n} "
            ret += "│" + " , ".join(output[n]) + "│\n"

        ret += "  ──────────────────────────────────────────────\n"
        ret += "   0     1     2     3     4     5     6     7\n"
        return ret


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
        grid_settings = {"size": settings["grid_size"], "min_length": settings["min_length"], "max_length": settings["max_length"]}
        self.Grid = Grid(grid_settings)
        self.load_track(settings["track_id"])
    
    def add_positions(self, pos1, pos2):
        return (pos1[0] + pos2[0], pos1[1] + pos2[1])
    
    def get_cell(self, pos):
        return self.Grid.get_cell(pos)
    
    def get_cell_type(self, pos):
        cell = self.get_cell(pos)
        return cell.type

    def get_cell_powerup(self, pos):
        cell = self.get_cell(pos)
        return cell.powerup
        
    def get_cell_direction(self, pos):
        cell = self.get_cell(pos)
        return cell.direction
    
    def get_start_postion(self):
        return self.Grid.start.position
    
    def grid_pos_to_coords(self, pos):
        ''' Translates the grid's (x,y) position (x and y are between 0 and self.grid_size) to the games real world (x,y) coordinates '''
        x = pos[0] * self.tile_size + self.tile_size/2
        y = pos[1] * self.tile_size + self.tile_size/2
        return (x, y)
        
    def start_coordinates(self):
        return self.grid_pos_to_coords(self.Grid.start.position)

    def draw(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                tile_type = self.get_cell_type((x,y))
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


    # ------------------------------- MAP GENERATION -------------------------------
    def load_track(self, track_number):
        if track_number == 0:
            self.Grid.generate_random_track()

        if track_number == 1:
            self.Grid.load_preset({"start" : (2,3), "direction" : (1,0), "layout": [
                "v1", "v0b", "d1", "d3", "v0", "d0", "h0d", "h0", "d1", "d3", "d2", "d0", "h0", 
                "d1", "v0b", "v0", "v0", "v0", "v0", "v0s", "d2", "d3", "v0", "v0", "v0", "d1",
                "d3", "d1", "d0", "v0", "v0", "d3", "d1", "d2", "h0", "h0", "h0", "d3", "d0", "d2"]})
        
        elif track_number == 2:
            self.Grid.load_preset({"start" : (1,0), "direction" : (0, -1), "layout": [
                "h1", "h0", "h0", "h0", "h0", "h0", "d2", "v0", "v0", "v0", "v0", "v0", "v0", "d1", 
                "h0", "h0", "h0", "h0", "h0", "j0", "d0", "v0", "v0", "v0", "v0", "v0", "v0", "d3"]})
        
        elif track_number == 3:
            self.Grid.load_preset({"start" : (0,1), "direction" : Vector(1,0), "layout" : [
                "v1", "d3", "h0", "d2", "v0", "d1", "h0", "d0"]})
        
        self.finish_line = FinishLine(road_width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, horizontal=(self.Grid.start.type[0] == 'h'))

    def draw_track_debug(self):
        '''
        Draws the track in text format with starting position marked as 'S'
        '''
        print(self.Grid)

if __name__ == "__main__":
    grid = Grid()
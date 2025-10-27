from OpenGL import GL, GLU
from math import *
from random import *
import pygame
from Base3DObjects import *
from Matrices import ModelMatrix


class Cell:
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
            return " . "
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

    def __init__(self, size=8, track_length=8):
        self.size = size
        self.start = None
        self.track_length = track_length
        self.cells = {}
        for x in range(size):
            for y in range(size):
                self.cells[(x,y)] = Cell(position=(x,y), type="XX")
        
        self.generate_random_track()
    
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
        if (x == 0 and y == 0):
            y += 1
        elif (x == self.size - 1) and y == self.size - 1:
            x -= 1

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
    
    def generate_random_track(self):
        self.set_random_start()

        self.dfs(self.start.next, self.start.direction, 1)
        print(self)
    
    def reached_end_check(self, pos, direction, length):
        return pos == self.start.position and length == self.track_length and direction == self.start.direction
    
    def dfs(self, cell, old_direction, length):
        if length <= self.track_length:
            directions = [ (1,0), (0,1), (-1,0), (0,-1) ]  # N, E, S, W
            shuffle(directions)  # make genereration random
            
            for new_direction in directions:
                new_type = self.TRACK_TYPE_FOR_DIRECTIONAL_CHANGE[(old_direction, new_direction)]
                next_pos = self.add_positions(cell.position, new_direction)

                if self.bounds_check(next_pos) and self.is_cell_empty(next_pos) and new_type != "x":
                    if self.reached_end_check(next_pos, new_direction, length):
                        cell.direction = new_direction
                        cell.next = self.start
                        cell.type = new_type
                        return cell
                    else:
                        next_cell = self.dfs(self.get_cell(next_pos), new_direction, length + 1)
                        if next_cell is not None:
                            cell.direction = new_direction
                            cell.next = next_cell
                            cell.type = new_type
                            print(self)
                            return cell
        return None

    def __str__(self):
        output = []
        for x in range(self.size):
            output.append([])
            for y in range(self.size):
                output[x].append("   ")
        node = self.start
        for n in range(self.size):
            if node is not None:
                pos = node.position
                output[self.size - 1 - pos[0]][pos[1]] = str(node)
                node = node.next
        
        result = []
        for row in output:
            result.append(", ".join(row))
        return "\n".join(result) + "\n\n"



class Track:
    TRACK_LENGTH = 8
    DIRECTIONAL_VECTOR = {
        'N': ( 1, 0),
        'S': (-1, 0),
        'E': ( 0, 1),
        'W': ( 0,-1)
    }
    TRACK_TYPE_FOR_DIRECTIONAL_CHANGE = {
        ('N', 'N'): 'v0',
        ('N', 'E'): 'd0',
        ('N', 'W'): 'd1',
        ('N', 'S'): 'XX',

        ('S', 'S'): 'v0',
        ('S', 'E'): 'd3',
        ('S', 'W'): 'd2',
        ('S', 'N'): 'XX',

        ('E', 'E'): 'h0',
        ('E', 'N'): 'd3',
        ('E', 'S'): 'd0',
        ('E', 'W'): 'XX',

        ('W', 'W'): 'h0',
        ('W', 'N'): 'd2',
        ('W', 'S'): 'd1',
        ('W', 'E'): 'XX'
    }
    def __init__(self, shader, track_setup = {"track": 0, "grid_size": 8, "tile_size": 32.0, "road_width": 16.0}):
        self.model_matrix = ModelMatrix()
        self.shader = shader

        self.grid_size = track_setup["grid_size"]
        self.tile_size = track_setup["tile_size"]
        self.half_tile = self.tile_size * 0.5
        self.road_width = track_setup["road_width"]
        self.sideline_width = (track_setup["tile_size"] - track_setup["road_width"]) * 0.5

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

        self.init_empty_track()

        self.load_track(track_setup["track"])

    def init_empty_track(self):
        ''' Creates an empty track layout '''
        self.track = {}
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                self.track[(x,y)] = "NA"
                
    def get_cell_data(self, pos):
        ''' Returns the track data at the given grid position '''
        if pos not in self.track:
            return "NA"
        return self.track[pos]
    
    def get_cell_type(self, data):
        ''' Returns the tile type for the given track data '''
        return data[:2]

    def get_cell_direction(self, data):
        ''' Returns the exit direction vector for the given track data '''
        return self.DIRECTIONS[data[2]]
    
    def get_cell_powerup(self, data):
        ''' Returns the powerup type for the given track data '''
        if len(data) < 4:
            return None
        return data[3]
    
    def add_positions(self, pos1, pos2):
        return (pos1[0] + pos2[0], pos1[1] + pos2[1])
    
    def subtract_positions(self, pos1, pos2):
        return (pos1[0] - pos2[0], pos1[1] - pos2[1])

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


    # ------------------------------- MAP GENERATION -------------------------------
    def set_random_starting_position(self):
        starting_cell, starting_cell_type = self.get_valid_starting_tilechoice()
        starting_tile_direction = Vector(1 if starting_cell_type == "v1N" else 0, 0, 0 if starting_cell_type == "v1N" else 1)

        self.track[starting_cell] = starting_cell_type
        self.track["start"] = starting_cell
        self.track["direction"] = starting_tile_direction
    
    def get_valid_starting_tilechoice(self):
        x = randint(0, self.grid_size - 1)
        y = randint(0, self.grid_size - 1)

        # Prevent corners
        if (x == 0 and y == 0):
            y += 1
        elif (x == self.grid_size - 1) and y == self.grid_size - 1:
            x -= 1

        # Determine valid tile types based on position
        if   x == 0 or x == self.grid_size - 1: # Left or right edge
            return (x,y), "v1N"
        elif y == 0 or y == self.grid_size - 1: # Top or bottom edge  
            return (x,y), "h1E"
        else:  # Interior
            return (x,y), choice(["v1N","h1E"])
            
    def generate_random_track(self):
        ''' 
        Algorithm that generates a random track layout with DFS
        empty cells are "NA"
        
        Number of cells: self.grid_size x self.grid_size
        
        tile data consists of:
        (x,y) : "[tile_type][exit_direction][powerup]"

        tile_type:
            v0 = vertical road without finish line
            h0 = horizontal road without finish line
            v1 = vertical road with finish line
            h1 = horizontal road with finish line
            d1 = 90 degree turn (bottom to right) (45 degree clockwise)
            d2 = 90 degree turn (left to bottom) (135 degree clockwise)
            d3 = 90 degree turn (top to left) (225 degree clockwise)
            d4 = 90 degree turn (right to top) (315 degree clockwise)
        exit_direction:
            N = north
            S = south
            E = east
            W = west
        powerup:
            b = boost
            s = slow
            d = disable
        '''
        self.init_empty_track()
        self.set_random_starting_position()
        
        starting_cell_position = self.track["start"]
        starting_cell_data = self.get_cell_data(starting_cell_position)

        print("Starting DEF algorithm at cell:", starting_cell_position, "Type:", starting_cell_data)
        next_cell_position = self.add_positions(starting_cell_position + self.DIRECTIONS[starting_cell_data[2]])
        self.dfs_recursion(next_cell_position, 1)
        self.print("Final Track Layout:")
        self.draw_track_debug()

    def dfs_recursion(self, current_type, current_pos, track_length):
        print("------ DFS at position:", current_pos, "Type:", current_type, "Length:", track_length)
        direction = self.DIRECTIONS[current_type[2]]
        next_track_pos = (current_pos[0] + direction[0], current_pos[1] + direction[1])
        
        if (track_length > self.TRACK_LENGTH or         # Base Case: exceeded track length
            self.is_out_of_bounds(next_track_pos) or    # Base Case: out of bounds
            self.track[next_track_pos] != "NA"):        # Base Case: already occupied
            
            return False
        
        if next_track_pos == self.track["start"]:   # Base case: reached end of track
            if track_length != self.TRACK_LENGTH or current_type[2] != self.gen_track[self.gen_track["start"]][2]:# not correct length or not coming from the correct direction
                
                self.gen_track[current_pos] = "NA" # clear cell and backtrack
                self.draw_track_debug()
                return False
            self.track[current_pos] = current_type
            self.draw_track_debug()
            print("Track generation complete!")
            return True # successfully completed track
        
        directions = ['N', 'S', 'E', 'W']
        shuffle(directions)  # make genereration random
        
        for new_direction in directions:
            next_type = self.TRACK_TYPE_FOR_DIRECTIONAL_CHANGE[(current_type[2], new_direction)]
            if next_type != 'X':
                self.gen_track[next_track_pos] = next_type + new_direction
                if self.dfs_recursion(next_type + new_direction, next_track_pos, track_length + 1):
                    print("Hello from the backtrack")
                    self.track[current_pos] = current_type
                    self.draw_track_debug()
                    return True
        
        self.gen_track[current_pos] = "NA" # clear cell and backtrack 
        return False

    def is_out_of_bounds(self, position):
        return position[0] < 0 or position[0] >= self.grid_size or position[1] < 0 or position[1] >= self.grid_size

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
            self.generate_random_track()
            self.finish_line = FinishLine(road_width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, horizontal=(self.track[self.track["start"]][0] == 'h'))

        if track_number == 1:
            self.track = {
                (0,0) : "NA", (1,0) : "NA", (2,0) : "NA", (3,0) : "NA", (4,0) : "NA", (5,0) : "NA", (6,0) : "d3", (7,0) : "d2",
                (0,1) : "NA", (1,1) : "d3", (2,1) : "h0", (3,1) : "h0", (4,1) : "h0", (5,1) : "d2", (6,1) : "v0", (7,1) : "v0s",
                (0,2) : "NA", (1,2) : "d0", (2,2) : "d2", (3,2) : "NA", (4,2) : "d3", (5,2) : "d1", (6,2) : "v0", (7,2) : "v0",
                (0,3) : "NA", (1,3) : "NA", (2,3) : "v1", (3,3) : "NA", (4,3) : "v0", (5,3) : "NA", (6,3) : "v0", (7,3) : "v0",
                (0,4) : "NA", (1,4) : "NA", (2,4) : "v0b",(3,4) : "NA", (4,4) : "v0", (5,4) : "d3", (6,4) : "d1", (7,4) : "v0",
                (0,5) : "NA", (1,5) : "d3", (2,5) : "d1", (3,5) : "NA", (4,5) : "d0", (5,5) : "d1", (6,5) : "NA", (7,5) : "v0",
                (0,6) : "NA", (1,6) : "v0", (2,6) : "NA", (3,6) : "NA", (4,6) : "d3", (5,6) : "d2", (6,6) : "NA", (7,6) : "v0b",
                (0,7) : "NA", (1,7) : "d0", (2,7) : "h0d",(3,7) : "h0", (4,7) : "d1", (5,7) : "d0", (6,7) : "h0", (7,7) : "d1",
                "start" : (2,3), "direction" : Vector(1,0,0)}
            
            self.finish_line = FinishLine(road_width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, horizontal=False)
        
        elif track_number == 2:
            self.track = {
                (0,0) : "d3", (1,0) : "h1W",(2,0) : "h0W", (3,0) : "h0W", (4,0) : "h0Wd",(5,0) : "h0W", (6,0) : "h0W", (7,0) : "d2W",
                (0,1) : "v0", (1,1) : "NA", (2,1) : "NA", (3,1) : "NA", (4,1) : "NA", (5,1) : "NA", (6,1) : "NA", (7,1) : "v0",
                (0,2) : "v0", (1,2) : "NA", (2,2) : "NA", (3,2) : "NA", (4,2) : "NA", (5,2) : "NA", (6,2) : "NA", (7,2) : "v0",
                (0,3) : "v0", (1,3) : "NA", (2,3) : "NA", (3,3) : "NA", (4,3) : "NA", (5,3) : "NA", (6,3) : "NA", (7,3) : "v0",
                (0,4) : "v0", (1,4) : "NA", (2,4) : "NA", (3,4) : "NA", (4,4) : "NA", (5,4) : "NA", (6,4) : "NA", (7,4) : "v0",
                (0,5) : "v0", (1,5) : "NA", (2,5) : "NA", (3,5) : "NA", (4,5) : "NA", (5,5) : "NA", (6,5) : "NA", (7,5) : "v0",
                (0,6) : "v0", (1,6) : "NA", (2,6) : "NA", (3,6) : "NA", (4,6) : "NA", (5,6) : "NA", (6,6) : "NA", (7,6) : "v0",
                (0,7) : "d0b",(1,7) : "h0", (2,7) : "h0", (3,7) : "h0", (4,7) : "h0", (5,7) : "h0", (6,7) : "h0s",(7,7) : "d1",
                "start" : (1,0), "direction" : Vector(0,0,-1)}

            self.finish_line = FinishLine(road_width=self.road_width, tile_size=self.tile_size, banks=self.sideline_width, horizontal=True)
        
        elif track_number == 3:
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
        
        elif track_number == 4:
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

    def draw_track_debug(self):
        '''
        Draws the track in text format with starting position marked as 'S'
        '''
        start_pos = self.track.get("start", None)
        
        print("\n" + "="*40 + " TRACK DEBUG " + "="*40)
        for x in range(self.grid_size):
            row = ""
            x = self.grid_size - 1 - x  # Invert x to match visual layout
            for y in range(self.grid_size):
                tile_data = self.track[(x,y)]
                tile_type = tile_data[:2]
                
                if tile_type == "NA":
                    row += " . "
                elif tile_type == "v0":
                    row += " | "
                elif tile_type == "v1":
                    row += "S| "
                elif tile_type == "h0":
                    row += "---"
                elif tile_type == "h1":
                    row += "-S-"
                elif tile_type == "d0":
                    row += " ┌ "
                elif tile_type == "d1":
                    row += " ┐ "
                elif tile_type == "d2":
                    row += " ┘ "
                elif tile_type == "d3":
                    row += " └ "
            print(row)
        
        if start_pos:
            print(f"Start: {start_pos} | Tile: {self.track[start_pos]}")
        print("="*93)

    def get_track_type(self, x, y):
        return self.track[(x, y)]

if __name__ == "__main__":
    grid = Grid()
    grid.generate_random_track()
    print(grid)
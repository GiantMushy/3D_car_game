
from random import choice, randint, shuffle
from Base3DObjects import Point, Coordinate


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
    def __init__(self, x=0, y=0, type="XX", next=None, direction=Coordinate(), powerup=None):
        self.x = x
        self.y = y
        self.key = (x,y)
        self.type = type
        self.next = next
        self.direction = direction
        self.powerup = powerup

        self.real_center = Point(0,0,0)
        self.real_enter = Point(0,0,0)
        self.real_exit = Point(0,0,0)

    def get_next_pos(self):
        return Coordinate(self.x + self.direction.x, self.y + self.direction.y)

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self.x == other.x and self.y == other.y
        return False
    
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
    
    def type(self):
        return self.tile_type
    
    def set_direction(self, direction):
        self.direction = direction
    
    def set_powerup(self, powerup):
        self.powerup = powerup
    
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
        (Coordinate( 1, 0), Coordinate( 1, 0)): 'h0',
        (Coordinate( 1, 0), Coordinate( 0, 1)): 'd2',
        (Coordinate( 1, 0), Coordinate( 0,-1)): 'd1',
        (Coordinate( 1, 0), Coordinate(-1, 0)): 'x',

        (Coordinate(-1, 0), Coordinate(-1, 0)): 'h0',
        (Coordinate(-1, 0), Coordinate( 0, 1)): 'd3',
        (Coordinate(-1, 0), Coordinate( 0,-1)): 'd0',
        (Coordinate(-1, 0), Coordinate( 1, 0)): 'x',

        (Coordinate( 0, 1), Coordinate( 0, 1)): 'v0',
        (Coordinate( 0, 1), Coordinate( 1, 0)): 'd0',
        (Coordinate( 0, 1), Coordinate(-1, 0)): 'd1',
        (Coordinate( 0, 1), Coordinate( 0,-1)): 'x',

        (Coordinate( 0,-1), Coordinate( 0,-1)): 'v0',
        (Coordinate( 0,-1), Coordinate( 1, 0)): 'd3',
        (Coordinate( 0,-1), Coordinate(-1, 0)): 'd2',
        (Coordinate( 0,-1), Coordinate( 0, 1)): 'x'
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
                self.cells[Coordinate(x,y)] = Cell(x, y)

    def get_cell(self, pos):
        try:
            return self.cells[pos]
        except:
            return None
    
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

        self.start = self.get_cell(Coordinate(x, y))
        # Determine valid tile types based on position
        if   x == 0 or x == self.size - 1: # Left or right edge
            self.start.direction = Coordinate(0,1)  # Facing North
        elif y == 0 or y == self.size - 1: # Top or bottom edge  
            self.start.direction = Coordinate(1,0)  # Facing East
        else:  # Interior
            self.start.direction = choice( [Coordinate(1,0), Coordinate(0,1)] )  # Randomly choose North or East
        
        self.start.type = "v1" if self.start.direction == Coordinate(0,1) else "h1"
        self.start.next = self.get_cell(self.start.get_next_pos())
    
    def bounds_check(self, position):
        return position.x >= 0 and position.x < self.size and position.y >= 0 and position.y < self.size
    
    def is_cell_empty(self, pos):
        cell = self.get_cell(pos)
        return cell is not None and cell.type == "XX"
    
    def reached_end_check(self, pos, direction, length):
        if pos.x == self.start.x and pos.y == self.start.y:
            if direction == self.start.direction:
                if length >= self.min_length and length <= self.max_length:
                    return True
        return False
    
    def generate_random_track(self):
        self.set_random_start()
        self.dfs(self.start.next, self.start.direction, 1)
        print(self)
    
    def dfs(self, cell, old_direction, length):
        directions = [ Coordinate(0,1), Coordinate(1,0), Coordinate(0,-1), Coordinate(-1,0) ]  # N, E, S, W
        shuffle(directions)  # make genereration random

        if length <= self.max_length:
            for new_direction in directions:
                if cell.type == "x":
                    continue
                cell.type = self.TRACK_TYPE_FOR_DIRECTIONAL_CHANGE[(old_direction, new_direction)]
                cell.direction = new_direction
                next_pos = cell.get_next_pos()
                cell.next = self.get_cell(next_pos)
                
                print(f"----------- Current Attempt = [next_pos: {next_pos} , next_dir: {new_direction} , length: {length}] -----------")
                print(self)
                
                if next_pos.x == self.start.x and next_pos.y == self.start.y:
                    if cell.direction == self.start.direction:
                        if length >= self.min_length and length <= self.max_length:
                            self.length += 1
                            print(self)
                            return True
                
                elif self.bounds_check(next_pos) and self.is_cell_empty(next_pos): # check if the propsed direction is valid
                    if self.dfs(cell.next, cell.direction, length + 1):
                        print(self)
                        self.length += 1
                        self.assign_random_powerup(cell)
                        return True
                
                cell.direction = Coordinate()
                cell.type = "XX"
                cell.next = None

        return False
        
    def load_preset(self, data):
        print("Loading preset")
        layout = data["layout"]
        prev_direction = data["direction"]
        pos = data["start"]

        self.start = self.get_cell(pos)
        cell = self.start
        for type in layout:
            cell.type = type[:2]
            cell.direction = self.get_next_direction(cell.type, prev_direction)
            pos += cell.direction
            cell.next = self.get_cell(pos)
            if len(type) == 3:
                cell.powerup = type[2]

            prev_direction = cell.direction.copy()
            cell = cell.next
            self.length += 1
            print(self)
    
    def get_next_direction(self, type, prev_direction):
        if type == "h0" or type == "v0" or type == "h1" or type == "v1" :
            return prev_direction
        elif type == "d0" or type == "d2":
            return Coordinate(prev_direction.y, prev_direction.x)
        elif type == "d1" or type == "d3":
            return Coordinate(-prev_direction.y, -prev_direction.x)
            

    def assign_random_powerup(self, cell):
        if cell.type in ["v0", "h0"]:
            num = randint(0, 10)
            if num < 3:
                cell.powerup = "b"
            elif num == 3:
                cell.powerup = "s"
            elif num == 9:
                cell.powerup = "d"

    def __str__(self):
        output = []
        for y in range(self.size):
            output.append([])
            for x in range(self.size):
                node = self.get_cell(Coordinate(x,self.size - 1 - y))
                output[y].append(str(node))

        
        ret = "  ──────────────────────────────────────────────\n"
        for n in range(self.size):
            ret += f"{self.size - 1 - n} "
            ret += "│" + " , ".join(output[n]) + "│\n"

        ret += "  ──────────────────────────────────────────────\n"
        ret += "   0     1     2     3     4     5     6     7\n"
        return ret

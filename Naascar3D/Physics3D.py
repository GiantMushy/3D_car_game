import math

from Base3DObjects import Coordinate

class Physics3D:
    GRAVITY = -9.81

    def __init__(self, track, vehicle):
        self.track = track
        self.vehicle = vehicle

        self.curr_tile = (self.track.Grid.start.x, self.track.Grid.start.y)

    def update_current_tile(self):
        # I know this is confusing, but the track's grid is (x,y) while the car's position is (x,y,z), so (z,x) == (x,y)
        car_x, car_y = self.vehicle.position.z, self.vehicle.position.x
        tile_x = int(car_x // self.track.tile_size)
        tile_y = int(car_y // self.track.tile_size)

        if (tile_x, tile_y) != self.curr_tile:
            self.curr_tile = (tile_x, tile_y)

    def update_active_tiles(self):
        """ Not currently used, but could be useful if it is neccesary to track which tiles are near the car."""
        
        x_tile, y_tile = self.curr_tile
        # Calculate bounds once with min/max to ensure they're within the grid
        x_min = max(0, x_tile - 1)
        x_max = min(self.track.grid_size, x_tile + 2)
        y_min = max(0, y_tile - 1)
        y_max = min(self.track.grid_size, y_tile + 2)

        # Use pre-calculated bounds directly in the ranges
        self.active_tiles = {
            (x, y): self.track.get_cell_type(Coordinate(x, y))
            for x in range(x_min, x_max)
            for y in range(y_min, y_max)
        }

    @staticmethod
    def _normalize(nx, ny):
        l = math.sqrt(nx*nx + ny*ny)
        if l == 0:
            return 0.0, 0.0
        return nx / l, ny / l

    def collide(self, grid_norm_x, grid_norm_y):
        nz, nx = self._normalize(grid_norm_x, grid_norm_y) # Note: car's (z,x) corresponds to track's (x,y)
        v = self.vehicle.direction
        dot = v.x*nx + v.z*nz   # dot product of velocity and normal

        impact = abs(dot)
        if self.vehicle.speed > 0.6 * self.vehicle.MAX_SPEED and impact > 0.15:
            # Base loss 12%, plus up to +18% depending on how head-on
            loss_fraction = 0.12 + 0.18 * impact          # range ≈ 0.12 .. 0.30
            self.vehicle.speed = max(self.vehicle.MIN_SPEED, self.vehicle.speed * (1.0 - loss_fraction))

        v.x = v.x - 2*dot*nx
        v.z = v.z - 2*dot*nz

        # Re-normalize direction to preserve unit length
        mag = math.hypot(v.x, v.z)
        if mag:
            v.x /= mag
            v.z /= mag
        
        self.vehicle.position.x += nx * 2
        self.vehicle.position.z += nz * 2

    def enforce_track_bounds(self):
        self.update_current_tile()

        self.enforce_tile_bounds(self.track.get_cell(Coordinate(self.curr_tile[0], self.curr_tile[1])))

    def enforce_tile_bounds(self, cell):
        if cell.type == "XX":
            return  # No walls on this tile

        tile_min_x = cell.x * self.track.tile_size
        tile_min_y = cell.y * self.track.tile_size
        tile_max_x = (cell.x + 1) * self.track.tile_size
        tile_max_y = (cell.y + 1) * self.track.tile_size

        car_x, car_y = self.vehicle.position.z, self.vehicle.position.x # Note the swap: car's z is track's x
        hitbox = self.vehicle.hitbox_size

        if cell.type in ("h0", "h1"):  # Horizontal road
            if car_y - hitbox < tile_min_y:
                self.collide(0, 1)  # Collide with bottom wall
                #print("Collide with bottom wall")
            elif car_y + hitbox > tile_max_y:
                self.collide(0, -1) # Collide with top wall
                #print("Collide with top wall")

        elif cell.type in ("v0", "v1"):  # Vertical road
            if car_x - hitbox < tile_min_x:
                self.collide(1, 0)  # Collide with left wall
                #print("Collide with left wall")
            elif car_x + hitbox > tile_max_x:
                self.collide(-1, 0) # Collide with right wall
                #print("Collide with right wall")
        
        elif cell.type == "d0":  # 90 degree turn (bottom to right) (45 degree clockwise)
            if car_x - hitbox < tile_min_x:
                self.collide(1, 0)  # Collide with left wall
                #print("Collide with left wall")
            elif car_y + hitbox > tile_max_y:
                self.collide(0, -1) # Collide with top wall
                #print("Collide with top wall")

        elif cell.type == "d1":  # 90 degree turn (left to bottom) (135 degree clockwise)
            if car_x + hitbox > tile_max_x:
                self.collide(-1, 0) # Collide with right wall
                #print("Collide with right wall")
            elif car_y + hitbox > tile_max_y:
                self.collide(0, -1) # Collide with top wall
                #print("Collide with top wall")

        elif cell.type == "d2":  # 90 degree turn (top to left) (225 degree clockwise)
            if car_x + hitbox > tile_max_x:
                self.collide(-1, 0) # Collide with right wall
                #print("Collide with right wall")
            elif car_y - hitbox < tile_min_y:
                self.collide(0, 1)  # Collide with bottom wall
                #print("Collide with bottom wall")

        elif cell.type == "d3":  # 90 degree turn (right to top) (315 degree clockwise)
            if car_x - hitbox < tile_min_x:
                self.collide(1, 0)  # Collide with left wall
                #print("Collide with left wall")
            elif car_y - hitbox < tile_min_y:
                self.collide(0, 1)  # Collide with bottom wall
                #print("Collide with bottom wall")

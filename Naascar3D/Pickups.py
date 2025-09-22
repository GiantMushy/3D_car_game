from dataclasses import dataclass
from Base3DObjects import *
from Matrices import ModelMatrix

@dataclass
class PickupEntity:
    object: Pickup
    position: Point
    timeout: float = 0.0

class Pickups:
    def __init__(self, track, vehicle):
        self.track = track
        self.vehicle = vehicle
        self.shader = track.shader
        self.model_matrix = ModelMatrix()

        self.pickups = []
        self.init_pickups()

    def update(self, delta_time):
        for p in self.pickups:
            if p.timeout == 0.0:
                p.object.update(delta_time)

                if self.check_collision(p):
                    print(f"Pickup collected: {p.object.type}")
                    self.apply_pickup_effect(p)
                    p.timeout = 10.0

            else:
                p.timeout -= delta_time
                if p.timeout < 0:
                    p.timeout = 0.0

    def draw(self):
        for p in self.pickups:
            if p.timeout == 0.0:
                self.set_model_matrix_and_shader(p)
                p.object.draw(self.shader)
                
    def init_pickups(self):
        for gx in range(self.track.grid_size):
            for gy in range(self.track.grid_size):
                tile_data = self.track.get_track_type(gx, gy)
                tile_pickups = tile_data[2:]
                if tile_pickups:
                    # grid (gx,gy) -> world (z = gx, x = gy)
                    world_x = gy * self.track.tile_size + self.track.half_tile
                    world_z = gx * self.track.tile_size + self.track.half_tile
                    base_y = 1.5
                    pickup_pos = Point(world_x, base_y, world_z)

                    if 'b' in tile_pickups:
                        self.pickups.append(PickupEntity(object=Pickup(type='speed_boost', scale=2.0, color=(0.0, 1.0, 0.0)), position=pickup_pos))
                    if 's' in tile_pickups:
                        self.pickups.append(PickupEntity(object=Pickup(type='slow_down', scale=2.0, color=(1.0, 1.0, 0.0)), position=pickup_pos))
                    if 'd' in tile_pickups:
                        self.pickups.append(PickupEntity(object=Pickup(type='disable', scale=2.0, color=(1.0, 0.0, 0.0)), position=pickup_pos))


    def check_collision(self, p):
        distance = p.position.distance(self.vehicle.position)
        return distance < (self.vehicle.hitbox_size + p.object.scale) / 2.0
    
    def apply_pickup_effect(self, p):
        if p.object.type == 'speed_boost':
            self.vehicle.boost()
        elif p.object.type == 'slow_down':
            self.vehicle.slow()
        elif p.object.type == 'disable':
            self.vehicle.disable()

    def set_model_matrix_and_shader(self, pickup_entity):
        o = pickup_entity.object
        pos = pickup_entity.position
        self.model_matrix.load_identity()

        self.model_matrix.add_translation(pos.x, pos.y + o.y_offset, pos.z) # apply translation + bob
        self.model_matrix.add_rotation_y(o.spin_angle) # spin
        
        self.model_matrix.add_scale(o.scale, o.scale, o.scale)
        self.shader.set_model_matrix(self.model_matrix.matrix)
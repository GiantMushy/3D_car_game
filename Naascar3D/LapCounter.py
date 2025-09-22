
from inspect import stack
from Base3DObjects import Point

class LapCounter:
    CHECKPOINT_WIDTH = 5.0

    def __init__(self, track, vehicle, total_laps = 3):
        self.track = track
        self.vehicle = vehicle
        
        self.half_tile = track.half_tile
        tile_size = track.tile_size

        self.total_laps = total_laps
        self.horizontal = (track.track["direction"] == Point(0,0,1)) or (track.track["direction"] == Point(0,0,-1))
        self.starting_pos = Point(track.track["start"][1] * tile_size + self.half_tile, 0.0, track.track["start"][0] * tile_size + self.half_tile)

        self.finish_line_pos = self.starting_pos
        self.checkpoint_1_pos = self.starting_pos.copy()
        self.checkpoint_2_pos = self.starting_pos.copy()

        self.checkpoint_1_pos += self.track.track["direction"] * self.half_tile
        self.checkpoint_2_pos -= self.track.track["direction"] * self.half_tile

        self.finish_line =  { "pos": self.finish_line_pos }
        self.checkpoint_1 = { "pos": self.checkpoint_1_pos, "passed": False }
        self.checkpoint_2 = { "pos": self.checkpoint_2_pos, "passed": False }

        self.lap_counter = 0

    def update(self):
        if self.is_in_zone(self.finish_line["pos"]):
            self.trigger_finish_line()
        elif self.is_in_zone(self.checkpoint_1["pos"]):
            self.trigger_checkpoint_1()
        elif self.is_in_zone(self.checkpoint_2["pos"]):
            self.trigger_checkpoint_2()

    def is_in_zone(self, checkpoint_pos):
        """ Check if vehicle is in square zone around checkpoint Point"""
        if self.horizontal:
            return  (checkpoint_pos.x - self.half_tile <= self.vehicle.position.x <= checkpoint_pos.x + self.half_tile) and \
                    (checkpoint_pos.z - self.CHECKPOINT_WIDTH <= self.vehicle.position.z <= checkpoint_pos.z + self.CHECKPOINT_WIDTH)
        else:
            return  (checkpoint_pos.x - self.CHECKPOINT_WIDTH <= self.vehicle.position.x <= checkpoint_pos.x + self.CHECKPOINT_WIDTH) and \
                    (checkpoint_pos.z - self.half_tile <= self.vehicle.position.z <= checkpoint_pos.z + self.half_tile)

    def trigger_checkpoint_1(self):
        if not self.checkpoint_1["passed"]:
            if not self.checkpoint_2["passed"]:
                self.checkpoint_1["passed"] = True
            else:
                self.checkpoint_1["passed"] = True
                self.checkpoint_2["passed"] = False

    def trigger_checkpoint_2(self):
        if not self.checkpoint_2["passed"]:
            if self.checkpoint_1["passed"]:
                self.checkpoint_2["passed"] = True
            else:
                self.checkpoint_2["passed"] = True
                self.checkpoint_1["passed"] = False

    def trigger_finish_line(self):
        if self.checkpoint_1["passed"] and self.checkpoint_2["passed"]:
            self.checkpoint_1["passed"] = False
            self.checkpoint_2["passed"] = False
            self.increment_lap()
        else:
            self.checkpoint_1["passed"] = False
            self.checkpoint_2["passed"] = False
    
    def increment_lap(self):
        self.lap_counter += 1
        self.finish_line["passed"] = True
        print(f"Lap {self.lap_counter}/{self.total_laps} completed!")
        if self.lap_counter >= self.total_laps:
            print("All laps completed!")
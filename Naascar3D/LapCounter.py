

from Naascar3D.Base3DObjects import Point


class Laps:
    def __init__(self, track, vehicle, total_laps = 3):
        self.track = track
        self.vehicle = vehicle

        self.total_laps = total_laps
        self.starting_grid_pos = Point(track.track["start"][1], 0, track.track["start"][0])
        self.horizontal = (track.track["direction"] == Point(0,0,1)) or (track.track["direction"] == Point(0,0,-1))
        


        self.current_lap = 0
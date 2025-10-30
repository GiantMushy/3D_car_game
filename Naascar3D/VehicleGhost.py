from Vehicle import *
from Matrices import *
from Base3DObjects import RaceCar

class Ghost:
    def __init__(self, track, settings = {"position" : Point(0,0,0), "direction" : Vector(1,0,0), "speed" : 5, "hitbox_size" : 2}):
        self.pos =         settings["position"]
        self.direction =   settings["direction"]
        self.speed =       settings["speed"]
        
        self.Track = track
        self.ModelMatrix = ModelMatrix()
        self.Body = RaceCar()


    def update(self, dt):
        pass

    def draw(self, shader):
        self.Body.draw(shader, self.ModelMatrix, self.pos, atan2(self.direction.x, self.direction.z))
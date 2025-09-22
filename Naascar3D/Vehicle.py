
from math import *
import OpenGL.GL as gl
from Matrices import *


class Vehicle:
    MAX_SPEED = 50.0
    MIN_SPEED = -20.0
    TURN_SPEED = 2.0
    ACCELERATION = 10.0

    def __init__(self, settings = {"position": Point(0,0,0), "direction": Vector(1,0,0), "hitbox_size": 1.0, "speed": 0, "steering": 0, "color": (1.0, 0.0, 0.0, 1.0)}):
        self.position = settings["position"]
        self.direction = settings["direction"]
        self.speed = settings["speed"]
        self.steering = settings["steering"]
        self.color = settings["color"]
        self.hitbox_size = settings["hitbox_size"]
        self.acceleration = self.ACCELERATION # default acceleration -- can be modified by power-ups
        
        self.disabled = 0
        self.slowed = 0
        self.boosted = 0

        self.model_matrix = ModelMatrix()
        self.car_body = RaceCar()

    def update(self, delta_time, steering_input):
        # Update speed and steering based on user input or AI
        self.acceleration = self.ACCELERATION
        if self.boosted:
            self.acceleration *= 2
            self.boosted -= delta_time
        elif self.slowed:
            self.acceleration *= 0.5
            self.slowed -= delta_time

        if not self.disabled:
            if steering_input[0]: # turn left
                self.turn_left(self.TURN_SPEED * delta_time)
            elif steering_input[1]: # turn right
                self.turn_right(self.TURN_SPEED * delta_time)
            else:
                self.car_body.steering_angle = 0.0  # Reset steering angle when not turning
            if steering_input[2]: # accelerate
                self.speed += self.acceleration * delta_time
            elif steering_input[3]: # brake
                self.speed -= self.acceleration * delta_time
            else: # decelerate
                self.auto_decelerate(delta_time)
        else:
            self.auto_decelerate(delta_time)
            self.disabled -= delta_time

        self.direction.normalize()
        self.move(delta_time)
    
    def move(self, delta_time):
        if self.speed > self.MAX_SPEED:
            self.speed = self.MAX_SPEED
        elif self.speed < self.MIN_SPEED:
            self.speed = self.MIN_SPEED

        displacement = self.direction * (self.speed * delta_time)
        self.position = self.position + displacement

    def turn_left(self, angle):
        # Rotate the direction vector to the left around the Y-axis on proportion of the car's speed
        #self.direction = self.direction.rotate_y(-angle * (self.speed / self.MAX_SPEED))
        self.direction = self.direction.rotate_y(-angle)
        self.car_body.steering_angle = 0.5  # Set steering angle for visual effect

    def turn_right(self, angle):
        #self.direction = self.direction.rotate_y(angle * (self.speed / self.MAX_SPEED))
        self.direction = self.direction.rotate_y(angle)
        self.car_body.steering_angle = -0.5  # Set steering angle for visual effect

    def auto_decelerate(self, delta_time):
        if self.speed > 0:
            self.speed -= self.ACCELERATION * delta_time
            if self.speed < 0:
                self.speed = 0
        elif self.speed < 0:
            self.speed += self.ACCELERATION * delta_time
            if self.speed > 0:
                self.speed = 0

    def dissable(self, duration):
        self.disabled = duration
    
    def slow(self, duration):
        self.slowed = duration
    
    def boost(self, duration):
        self.boosted = duration

    def draw(self, shader, turning=None):
        self.car_body.draw(shader, self.model_matrix, self.position, atan2(self.direction.x, self.direction.z))
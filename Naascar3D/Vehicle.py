
from math import *
import OpenGL.GL as gl
from Matrices import *
from Base3DObjects import ObjRaceCar


class Vehicle:
    MAX_SPEED = 70.0
    MIN_SPEED = -20.0
    ACCELERATION = 10.0

    DISABLED_DURATION = 3.0
    SLOWED_DURATION = 5.0
    BOOSTED_DURATION = 5.0

    TURN_SPEED = 2.0
    STEER_MIN_SPEED = 0.1          # must exceed this to steer at all
    STEER_MIN_FACTOR = 0.5         # minimal factor once moving
    STEER_MAX_FACTOR = 1.15        # allow a bit more authority at top speed
    STEER_RESPONSE_EXP = 2.0       # >1 makes low speeds very insensitive

    def __init__(self, settings = {"position": Point(0,0,0), "direction": Vector(1,0,0), "hitbox_size": 1.0, "speed": 0}):
        self.position = settings["position"]
        self.direction = settings["direction"]
        self.hitbox_size = settings["hitbox_size"]
        self.speed = settings["speed"]
        self.steering = 0.0
        self.acceleration = self.ACCELERATION # default acceleration -- can be modified by power-ups
        
        self.disabled = 0
        self.slowed = 0
        self.boosted = 0

        self.model_matrix = ModelMatrix()
        #self.car_body = RaceCar(1)
        self.car_body = ObjRaceCar(color=(0.8, 0.2, 0.2))  # Red player car

    def update(self, delta_time, steering_input):
        # Update speed and steering based on user input or AI
        self.acceleration = self.ACCELERATION
        self.top_speed = self.MAX_SPEED
        if self.boosted:
            self.acceleration *= 3
            self.top_speed = self.MAX_SPEED * 2.0
            self.boosted -= delta_time
            if self.boosted < 0:
                self.boosted = 0
        elif self.slowed:
            self.acceleration *= 0.2
            self.top_speed = self.MAX_SPEED * 0.2
            self.slowed -= delta_time
            if self.slowed < 0:
                self.slowed = 0

        if not self.disabled:
            if steering_input[0]:
                self.turn_left(self.TURN_SPEED * delta_time)
            elif steering_input[1]:
                self.turn_right(self.TURN_SPEED * delta_time)
            else:
                self.car_body.steering_angle = 0.0  # Reset steering angle when not turning

            if steering_input[2]: # accelerate
                self.speed += self.acceleration * delta_time
            elif steering_input[3]: # brake / reverse
                if self.speed > 0:  self.speed -= self.acceleration * 2 * delta_time
                else:               self.speed -= self.acceleration * delta_time
            else:
                self.auto_decelerate(delta_time)
        else:
            self.auto_decelerate(delta_time)
            self.disabled -= delta_time
            if self.disabled < 0:
                self.disabled = 0

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
        factor = self.compute_steer_factor()
        if factor == 0.0:
            self.car_body.steering_angle = 0.0
            return
        direction_sign = 1.0 if self.speed >= 0.0 else -1.0  # invert yaw when reversing
        eff_angle = -angle * factor * direction_sign
        self.direction = self.direction.rotate_y(eff_angle)
        self.car_body.steering_angle = 0.6 * factor

    def turn_right(self, angle):
        factor = self.compute_steer_factor()
        if factor == 0.0:
            self.car_body.steering_angle = 0.0
            return
        direction_sign = 1.0 if self.speed >= 0.0 else -1.0
        eff_angle = angle * factor * direction_sign
        self.direction = self.direction.rotate_y(eff_angle)
        self.car_body.steering_angle = -0.6 * factor

    def compute_steer_factor(self):
        v = abs(self.speed)
        if v <= self.STEER_MIN_SPEED:
            return 0.0
        # Normalize to [0,1]
        ratio = min(v / self.MAX_SPEED, 1.0)
        # Emphasize high speeds; exp > 1 reduces low-speed response
        ratio = ratio ** self.STEER_RESPONSE_EXP
        factor = self.STEER_MIN_FACTOR + ratio * (self.STEER_MAX_FACTOR - self.STEER_MIN_FACTOR)
        return factor

    def auto_decelerate(self, delta_time):
        if self.speed > 0:
            self.speed -= self.ACCELERATION * delta_time * 2
            if self.speed < 0:
                self.speed = 0
        elif self.speed < 0:
            self.speed += self.ACCELERATION * delta_time
            if self.speed > 0:
                self.speed = 0

    def disable(self):
        self.disabled = self.DISABLED_DURATION
    
    def slow(self):
        self.speed *= 0.2  # immediate speed reduction
        self.slowed = self.SLOWED_DURATION
    
    def boost(self):
        self.speed = self.MAX_SPEED  # Immediate speed boost
        self.boosted = self.BOOSTED_DURATION

    def draw(self, shader, turning=None):
        self.car_body.draw(shader, self.model_matrix, self.position, atan2(self.direction.x, self.direction.z))
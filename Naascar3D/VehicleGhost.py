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
        self.Body = RaceCar(
                body_color=(0.1, 0.9, 0.1),
                cabin_color=(0.30, 0.80, 0.90),
                wheel_color=(0.1, 0.1, 0.1),
                steering_angle=0.0)

        self.current_cell = self.Track.Grid.start
        self.t = 0.0
        self.turning_left = False
        self.turning_right = False

        self._p0 = Point(0,0,0)
        self._p1 = Point(0,0,0)
        self._p2 = Point(0,0,0)
        self._seg_len = 1.0
        self._setup_segment(self.current_cell)

    def _setup_segment(self, cell):
        self._p0 = cell.real_enter.copy()
        self._p1 = cell.real_center.copy()
        self._p2 = cell.real_exit.copy()

        self._seg_len = max(0.0001, self._p0.distance(self._p1) + self._p1.distance(self._p2))

    def update(self, dt):

        # Advance parameter using speed scaled by approximate segment length
        delta_t = (self.speed * dt) / self._seg_len
        self.t += delta_t

        # if we finish this segment, advance to next (support overshoot)
        while self.t >= 1.0 and self.current_cell is not None:
            self.t -= 1.0
            nxt = self.current_cell.next
            self.current_cell = nxt
            self._setup_segment(self.current_cell)

        # clamp t
        t = max(0.0, min(1.0, self.t))

        # Quadratic Bezier position: B(t) = (1-t)^2 P0 + 2(1-t)t P1 + t^2 P2
        u = 1.0 - t
        pos = (u*u) * self._p0 + (2 * u * t) * self._p1 + (t*t) * self._p2 
        self.pos = pos

        # derivative B'(t) = 2(1-t)(P1-P0) + 2 t (P2-P1)
        d = (2 * u) * (self._p1 - self._p0) + (2 * t) * (self._p2 - self._p1)  # Vector
        # set horizontal direction from derivative (x,z)
        cross_y = self.direction.x * d.z - self.direction.z * d.x # to detect change in direction (for turning the tires)
        self.direction.x = d.x
        self.direction.y = 0.0
        self.direction.z = d.z

        # normalize direction vector (avoid zero-length)
        mag = math.hypot(self.direction.x, self.direction.z)
        if mag > 1e-6:
            self.direction.x /= mag
            self.direction.z /= mag

        self.turn_tires(cross_y)

    def turn_tires(self, cross_y):
    
        # Threshold to avoid noise from small direction changes
        turn_threshold = 0.01
        
        if cross_y > turn_threshold:
            self.Body.steering_angle = -0.6
        elif cross_y < -turn_threshold:
            self.Body.steering_angle = 0.6
        else:
            self.Body.steering_angle = 0.0

    def draw(self, shader):
        self.Body.draw(shader, self.ModelMatrix, self.pos, atan2(self.direction.x, self.direction.z))
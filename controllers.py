from abc import ABC, abstractmethod
import math

class BaseController(ABC):
    def __init__(self, parent_entity, linear_velocity, angular_velocity, logger):
        self._parent_entity = parent_entity

        self._linear_velocity = linear_velocity
        self._angular_velocity = angular_velocity
        self._logger = logger

    @abstractmethod
    def move(self, dt, held_keys):
        pass

class DroneController(BaseController):
    def __init__(self, parent_entity, linear_velocity, angular_velocity, logger, **kwargs):
        super().__init__(parent_entity, linear_velocity, angular_velocity, logger)

    def move(self, dt, held_keys):
        dist = held_keys['w'] * dt * self._linear_velocity

        # Tilt drone when going forward
        self._parent_entity.rotation_z = held_keys['w'] * -15

        # check bounds
        nx = self._parent_entity.x - dist * math.cos(self._parent_entity.rotation_y * math.pi / 180)
        nz = self._parent_entity.z + dist * math.sin(self._parent_entity.rotation_y * math.pi / 180)
        if 0 <= nx and nx <= 40:
            self._parent_entity.x = nx
        if 0 <= nz and nz <= 40:
            self._parent_entity.z = nz

        ny = self._parent_entity.y + held_keys['z'] * dt * self._linear_velocity - held_keys['x'] * dt * self._linear_velocity
        if ny >= 0.5:
            self._parent_entity.y = ny

        self._parent_entity.rotation_y += held_keys['a'] * dt * self._angular_velocity
        self._parent_entity.rotation_y -= held_keys['d'] * dt * self._angular_velocity


class RotationController(BaseController):
    def __init__(self, parent_entity, linear_velocity, angular_velocity, logger, **kwargs):
        super().__init__(parent_entity, linear_velocity, angular_velocity, logger)
    
    def move(self, dt, held_keys):
        dist = held_keys['w'] * dt * self._linear_velocity

        # check bounds
        nx = self._parent_entity.x - dist * math.cos(self._parent_entity.rotation_y * math.pi / 180)
        nz = self._parent_entity.z + dist * math.sin(self._parent_entity.rotation_y * math.pi / 180)
        if 0 <= nx and nx <= 40:
            self._parent_entity.x = nx
        if 0 <= nz and nz <= 40:
            self._parent_entity.z = nz

        # player.x += held_keys['d'] * time.dt * 4
        # player.x -= held_keys['a'] * time.dt * 4

        # player.z += held_keys['w'] * time.dt * 4
        # player.z -= held_keys['s'] * time.dt * 4

        # player.y += held_keys['z'] * time.dt * 4
        # player.y -= held_keys['x'] * time.dt * 4

        self._parent_entity.rotation_y += held_keys['a'] * dt * self._angular_velocity
        self._parent_entity.rotation_y -= held_keys['d'] * dt * self._angular_velocity
        

class JumpController(BaseController):
    def __init__(self, parent_entity, linear_velocity, angular_velocity, logger, ground_height, **kwargs):
        super().__init__(parent_entity, linear_velocity, angular_velocity, logger)

        self._vertical_velocity = 0
        self._g = -9.81
        self._ground_height = ground_height # Shouldn't be hardcoded, can be received on init
        self._multiple_jump = False
    
    def set_vertical_vel(self, vertical_velocity):
        if not self._multiple_jump and self._vertical_velocity != 0:
            return # do not allow double, triple or even more jumps
        self._vertical_velocity = vertical_velocity
        self._logger.log(f"Set vertical vel to: {self._vertical_velocity}")

    def get_vertical_vel(self):
        return self._vertical_velocity

    def _update_y(self, dt):
        # vertical velocity?
        if self._vertical_velocity != 0:
            # update positions and velocities
            # dy = v0*dt + 1/2*a*(dt^2)
            # dv = a*dt
            self._parent_entity.y += self._vertical_velocity * dt + (1/2) * (self._g) * dt*dt
            self._vertical_velocity += self._g * dt
            if self._parent_entity.y <= self._ground_height:
                self._parent_entity.y = self._ground_height
                self._vertical_velocity = 0

    def move(self, dt, held_keys):
        # TODO: While on air, this values should not be able to change
        dist = held_keys['w'] * dt * self._linear_velocity

        self._update_y(dt)
        
        # check bounds
        nx = self._parent_entity.x - dist * math.cos(self._parent_entity.rotation_y * math.pi / 180)
        nz = self._parent_entity.z + dist * math.sin(self._parent_entity.rotation_y * math.pi / 180)
        if 0 <= nx and nx <= 40:
            self._parent_entity.x = nx
        if 0 <= nz and nz <= 40:
            self._parent_entity.z = nz


        # player.x += held_keys['d'] * time.dt * 4
        # player.x -= held_keys['a'] * time.dt * 4

        # player.z += held_keys['w'] * time.dt * 4
        # player.z -= held_keys['s'] * time.dt * 4

        # player.y += held_keys['z'] * time.dt * 4
        # player.y -= held_keys['x'] * time.dt * 4

        self._parent_entity.rotation_y += held_keys['a'] * dt * self._angular_velocity
        self._parent_entity.rotation_y -= held_keys['d'] * dt * self._angular_velocity
    
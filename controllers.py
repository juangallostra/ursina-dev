from abc import ABC, abstractmethod
import math

class BaseController(ABC):
    def __init__(self, parent_entity, linear_velocity, angular_velocity, logger):
        self._parent_entity = parent_entity

        self._linear_velocity = linear_velocity
        self._angular_velocity = angular_velocity
        self._logger = logger

    @abstractmethod
    def move(self, dt, held_keys, **kwargs):
        pass

class DroneController(BaseController):
    def __init__(self, parent_entity, linear_velocity, angular_velocity, logger, **kwargs):
        super().__init__(parent_entity, linear_velocity, angular_velocity, logger)

    def move(self, dt, held_keys, **kwargs):
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
    
    def move(self, dt, held_keys, **kwargs):
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
        self._jumping = False
    
    def set_vertical_vel(self, vertical_velocity):
        if not self._multiple_jump and self._vertical_velocity != 0:
            return # do not allow double, triple or even more jumps
        self._vertical_velocity = vertical_velocity

    def get_vertical_vel(self):
        return self._vertical_velocity

    def _update_y(self, dt, vel):
        # vertical velocity?
        if self._vertical_velocity != 0:
            if not self._jumping:
                self._jump_orientation = self._parent_entity.rotation_y 
                self._jump_vel = vel
                self._jumping = True 
            # update positions and velocities
            # dy = v0*dt + 1/2*a*(dt^2)
            # dv = a*dt
            self._parent_entity.y += self._vertical_velocity * dt + (1/2) * (self._g) * dt*dt
            self._vertical_velocity += self._g * dt
            if self._parent_entity.y <= self._ground_height:
                self._parent_entity.y = self._ground_height
                self._vertical_velocity = 0
                self._jumping = False
        
        return True if self._parent_entity.y > self._ground_height else False

    def _update_x_z(self, d, rot ):
            nx = self._parent_entity.x - d * math.cos(rot * math.pi / 180)
            nz = self._parent_entity.z + d * math.sin(rot * math.pi / 180)
            if 0 <= nx and nx <= 40:
                self._parent_entity.x = nx
            if 0 <= nz and nz <= 40:
                self._parent_entity.z = nz

    def move(self, dt, held_keys, **kwargs):

        colls =  kwargs.get('collisions', dict())
        # for c in colls.items():
        #     self._logger.log(f'{c}')

        dist = held_keys['w'] * dt * self._linear_velocity

        if bool(colls):
            is_on_air = False
        else:
            is_on_air = self._update_y(dt, held_keys['w'] * dt * self._linear_velocity)
        
        if is_on_air:
            self._update_x_z(self._jump_vel, self._jump_orientation)

        # check bounds
        if not is_on_air:
            self._update_x_z(dist, self._parent_entity.rotation_y)

        self._parent_entity.rotation_y += held_keys['a'] * dt * self._angular_velocity
        self._parent_entity.rotation_y -= held_keys['d'] * dt * self._angular_velocity
    
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
    def __init__(self, parent_entity, linear_velocity, angular_velocity, logger):
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
    def __init__(self, parent_entity, linear_velocity, angular_velocity, logger):
        super().__init__(parent_entity, linear_velocity, angular_velocity, logger)

        self._vertical_vel = 0
    
    def set_vertical_vel(self, vv):
        self._vertical_vel = vv
        self._logger.log(f"Set VV to: {self._vertical_vel}")

    def move(self, dt, held_keys):
        dist = held_keys['w'] * dt * self._linear_velocity

        # check bounds
        nx = self._parent_entity.x - dist * math.cos(self._parent_entity.rotation_y * math.pi / 180)
        nz = self._parent_entity.z + dist * math.sin(self._parent_entity.rotation_y * math.pi / 180)
        if 0 <= nx and nx <= 40:
            self._parent_entity.x = nx
        if 0 <= nz and nz <= 40:
            self._parent_entity.z = nz

        # vertical acceleration?
        if self._vertical_vel != 0:
            # dy = v0*dt + 1/2*a*(dt^2)
            # dv = a*dt
            dy = self._vertical_vel * dt + (1/2) * (-9.81) * dt*dt
            dv = -9.81 * dt
            self._logger.log(f"Jumping: dy - {dy}, dv - {dv}")
            # update positions and velocities
            self._parent_entity.y += dy
            self._vertical_vel += dv
            if self._parent_entity.y <= 0.5:
                self._parent_entity.y = 0.5
                self._vertical_vel = 0

        # player.x += held_keys['d'] * time.dt * 4
        # player.x -= held_keys['a'] * time.dt * 4

        # player.z += held_keys['w'] * time.dt * 4
        # player.z -= held_keys['s'] * time.dt * 4

        # player.y += held_keys['z'] * time.dt * 4
        # player.y -= held_keys['x'] * time.dt * 4

        self._parent_entity.rotation_y += held_keys['a'] * dt * self._angular_velocity
        self._parent_entity.rotation_y -= held_keys['d'] * dt * self._angular_velocity
    
from abc import ABC, abstractmethod
import math

class BaseController(ABC):
    def __init__(self, parent_entity, linear_velocity, angular_velocity):
        self._parent_entity = parent_entity

        self._linear_velocity = linear_velocity
        self._angular_velocity = angular_velocity

    @abstractmethod
    def move(self, dt, held_keys):
        pass

class DroneController(BaseController):
    def __init__(self, parent_entity, linear_velocity, angular_velocity):
        super().__init__(parent_entity, linear_velocity, angular_velocity)

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


class ShipController(BaseController):
    def __init__(self, parent_entity, linear_velocity, angular_velocity):
        super().__init__(parent_entity, linear_velocity, angular_velocity)

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
    
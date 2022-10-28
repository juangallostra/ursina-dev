from ursina import *
import math

class Player(Entity):
    def __init__(self, add_to_scene_entities=True, angular_speed=80, linear_speed=4, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self._angular_speed = angular_speed
        self._linear_speed = linear_speed

    def update(self):
        dist = held_keys['w'] * time.dt * self._linear_speed

        # check bounds
        nx = self.x - dist * math.cos(self.rotation_y * math.pi / 180)
        nz = self.z + dist * math.sin(self.rotation_y * math.pi / 180)
        if 0 <= nx and nx <= 40:
            self.x = nx
        if 0 <= nz and nz <= 40:
            self.z = nz

        # self.x -= dist * math.cos(self.rotation_y * math.pi / 180)
        # self.z += dist * math.sin(self.rotation_y * math.pi / 180)

        # player.x += held_keys['d'] * time.dt * 4
        # player.x -= held_keys['a'] * time.dt * 4

        # player.z += held_keys['w'] * time.dt * 4
        # player.z -= held_keys['s'] * time.dt * 4

        # player.y += held_keys['z'] * time.dt * 4
        # player.y -= held_keys['x'] * time.dt * 4

        self.rotation_y += held_keys['a'] * time.dt * self._angular_speed
        self.rotation_y -= held_keys['d'] * time.dt * self._angular_speed

from ursina import *

class Projectile(Entity):
    def __init__(self, speed, rotation, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self._speed = speed
        self._rotation = rotation

    def update(self):
        dist = self._speed * time.dt
        self.x -= dist * math.cos(self._rotation * math.pi / 180)
        self.z += dist * math.sin(self._rotation * math.pi / 180)
        # destroy when out of bounds
        # if 0 >= self.z or self.z >= 40 or 0 >= self.x or self.x >= 40:
        #     destroy(self)

        # wrap around
        if 0 >= self.z:
            self.z = 40
        elif self.z >= 40:
            self.z = 0
        elif 0 >= self.x:
            self.x = 40
        elif self.x >= 40:
            self.x = 0
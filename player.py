from ursina import *
from controllers import DroneController, ShipController
import math

DEFAULT_LINEAR_VELOCITY = 4
DEFAULT_ANGULAR_VELOCITY = 80


class ShipPlayer(Entity):
    def __init__(
        self, 
        add_to_scene_entities=True, 
        linear_velocity=DEFAULT_LINEAR_VELOCITY, 
        angular_velocity=DEFAULT_ANGULAR_VELOCITY, 
        controller=ShipController, 
        **kwargs
    ):
        super().__init__(add_to_scene_entities, **kwargs)
        self._controller = controller(parent_entity=self, linear_velocity=linear_velocity, angular_velocity=angular_velocity)

    def update(self):
        self._controller.move(time.dt, held_keys)

class DronePlayer(Entity):
    def __init__(        
        self, 
        add_to_scene_entities=True, 
        linear_velocity=DEFAULT_LINEAR_VELOCITY, 
        angular_velocity=DEFAULT_ANGULAR_VELOCITY, 
        controller=DroneController, 
        **kwargs
    ):
        super().__init__(add_to_scene_entities, **kwargs)
        self._controller = controller(parent_entity=self, linear_velocity=linear_velocity, angular_velocity=angular_velocity)


    def update(self):
        self._controller.move(time.dt, held_keys)

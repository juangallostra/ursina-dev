from ursina import *
from controllers import DroneController, RotationController

DEFAULT_LINEAR_VELOCITY = 6
DEFAULT_ANGULAR_VELOCITY = 120


class GenericPlayer(Entity):
    def __init__(
        self, 
        add_to_scene_entities=True, 
        linear_velocity=DEFAULT_LINEAR_VELOCITY, 
        angular_velocity=DEFAULT_ANGULAR_VELOCITY,
        ground_height=0,
        controller=RotationController,
        logger=None,
        **kwargs
    ):
        super().__init__(add_to_scene_entities, **kwargs)
        self._controller = controller(
            logger=logger,
            parent_entity=self,
            linear_velocity=linear_velocity,
            angular_velocity=angular_velocity,
            ground_height=self.y)
        self._logger = logger

    def update(self):
        self._controller.move(time.dt, held_keys)

    def get_controller(self):
        return self._controller

class DronePlayer(Entity):
    def __init__(        
        self, 
        logger,
        add_to_scene_entities=True, 
        linear_velocity=DEFAULT_LINEAR_VELOCITY, 
        angular_velocity=DEFAULT_ANGULAR_VELOCITY, 
        controller=DroneController,
        **kwargs
    ):
        super().__init__(add_to_scene_entities, **kwargs)
        self._controller = controller(logger=logger, parent_entity=self, linear_velocity=linear_velocity, angular_velocity=angular_velocity)


    def update(self):
        self._controller.move(time.dt, held_keys)

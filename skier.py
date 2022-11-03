from ursina import *
from ursina.shaders import *


DEFAULT_LINEAR_VELOCITY = 6
DEFAULT_ANGULAR_VELOCITY = 120

class CustomCollision:
    def __init__(self, obj1, obj2, collision) -> None:
        self.obj1 = obj1
        self.obj2 = obj2
        self.collision = collision

class Skier(Entity):
    """
    Player entity. This is the Entity that the user controls and
    it is how the user interacts with the virtual world
    """
    def __init__(
        self, 
        add_to_scene_entities=True, 
        linear_velocity=DEFAULT_LINEAR_VELOCITY, 
        angular_velocity=DEFAULT_ANGULAR_VELOCITY,
        controller=None,
        logger=None,
        **kwargs
    ):
        super().__init__(
            add_to_scene_entities,
            scale_x=0.4,
            scale_y=0.4,
            scale_z=0.4,
            model='models/skier_1.obj', 
            texture='models/skier_1.mtl',
            position=(0, 0.5, 0),
            collider='box',
            shader=lit_with_shadows_shader,
            rotation_y = 120,
            **kwargs)

        self._controller = controller(
            logger=logger,
            parent_entity=self,
            linear_velocity=linear_velocity,
            angular_velocity=angular_velocity,
            ground_height=kwargs.get('ground_height', self.y) # if no ground height has been specified, assume current y
        )

        self._logger = logger

        self._collisions_againts = []

    def update(self):
        # TODO: improve collision handling
        collisions = []
        for entity in self._collisions_againts:
            if entity.intersects(self).hit:
                collisions.append(CustomCollision(self, entity, entity.intersects(self)))

        self._controller.move(time.dt, held_keys, collisions=collisions)

    def set_vertical_velocity(self, vertical_velocity):
        self._controller.set_vertical_velocity(vertical_velocity)

    def get_controller(self):
        return self._controller

    def add_collider_check_entity(self, entity):
        self._collisions_againts.append(entity)

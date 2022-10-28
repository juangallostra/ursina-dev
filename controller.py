DEFAULT_LINEAR_VELOCITY = 4
DEFAULT_ANGULAR_VELOCITY = 80

class BaseController():
    def __init__(self, parent_entity, linear_velocity=DEFAULT_LINEAR_VELOCITY, angular_velocity=DEFAULT_ANGULAR_VELOCITY):
        self._parent_entity = parent_entity

        self._linear_velocity = linear_velocity
        self._angular_velocity = angular_velocity

    def move(self, dt, held_keys):
        raise NotImplementedError

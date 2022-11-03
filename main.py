from ursina import *
from ursina.shaders import *
from controllers import RotationController, DroneController, JumpController
from logger import Logger

from player import GenericPlayer, DronePlayer
from projectile import Projectile

import panda3d

from skier import Skier

# create a window
app = Ursina()

# most things in ursina are Entities. An Entity is a thing you place in the world.
# you can think of them as GameObjects in Unity or Actors in Unreal.
# the first paramenter tells us the Entity's model will be a 3d-model called 'cube'.
# ursina includes some basic models like 'cube', 'sphere' and 'quad'.

logger = Logger(
    messages_to_display=20, 
    x_0=-.85,
    y_0=.45,
    dy=-.05
)


EditorCamera()

# in ursina, positive x is right, positive y is up, and positive z is forward.

snow = []
for z in range(40):
    for x in range(40):
        snow.append(
            Entity(
                model='cube',
                collider='box',
                position=(x, 0, z),
                parent=scene,
                origin_y=0.5,
                texture='models/snow',
                shader=basic_lighting_shader
            )
        )

# Skier
player = Skier(
    linear_velocity=6,
    angular_velocity=120,
    controller=JumpController,
    logger=logger
)


camera.position = (20, 70, -55)
camera.rotation = (45, 0, 0)

# this part will make the player move left or right based on our input.
# to check which keys are held down, we can check the held_keys dictionary.
# 0 means not pressed and 1 means pressed.
# time.dt is simply the time since the last frame. by multiplying with this, the
# player will move at the same speed regardless of how fast the game runs.

# Extra entities
rail =  Entity(
        model='models/rail_1.obj',
        texture='models/rail_1',
        scale_x = 0.3,
        scale_y = 0.3,
        scale_z = 0.3,
        # color=color.blue,
        collider='box',
        position=(20, 0, 20),
        parent=scene,
        origin_y=0.5,
        shader=basic_lighting_shader
    )

# Manually adjusted values
rail.collider.shape = panda3d.core.CollisionBox((-20.3241, -1.0, -1.00423), (20.3241, 0.3, 1.00423))
# Add rail to list of objects the player has to check collisions against
player.add_collider_check_entity(rail)

def update():
    if rail.intersects(player).hit:
        rail.color = color.lime
    else:
        rail.color = color.white

def input(key):
    if key == 'space':
        player.set_vertical_velocity(5)


# Shaders
pivot = Entity()
DirectionalLight(
    parent=pivot,
    x = 20,
    y = 70,
    z= -55,
    shadows=True,
    rotation=(45, 0, 0)
)

# start running the game
app.run()
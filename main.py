from ursina import *
from ursina.shaders import *
import math
from controllers import ShipController, DroneController

from player import ShipPlayer, DronePlayer
from projectile import Projectile

# create a window
app = Ursina()
# most things in ursina are Entities. An Entity is a thing you place in the world.
# you can think of them as GameObjects in Unity or Actors in Unreal.
# the first paramenter tells us the Entity's model will be a 3d-model called 'cube'.
# ursina includes some basic models like 'cube', 'sphere' and 'quad'.


# Sky()
# ground = Entity(model='plane', collider='box', scale=128, texture='grass', texture_scale=(4,4), name="ground")

EditorCamera()

# in ursina, positive x is right, positive y is up, and positive z is forward.

projectiles = []
sea = []

for z in range(40):
    for x in range(40):
        sea.append(
            Entity(
                model='cube',
                # color=color.blue,
                collider='box',
                position=(x, 0, z),
                parent=scene,
                origin_y=0.5,
                texture='models/water_2',
                shader=basic_lighting_shader
            )
        )

# Ship

player = ShipPlayer(
    # linear_velocity=6,
    # angular_velocity=120,
    # controller=ShipController,
    model='models/pirate-ship-fat.obj', 
    texture='models/pirate-ship-fat.mtl',
    position=(0,-0.1,0),
    # collider='mesh'
    collider='box',
    shader=lit_with_shadows_shader
)

# Drone
# player = DronePlayer(
#     angular_speed=120,
#     linear_speed=6,
#     controller=DroneController,
#     model='models/drone.obj',
#     color=color.black,
#     # model='models/pirate-ship-fat.obj', 
#     # texture='models/pirate-ship-fat.mtl',
#     scale_x=0.5,
#     scale_y=0.5,
#     scale_z=0.5,
#     # position=(0,-0.1,0),
#     position=(0,1,0),
#     # collider='mesh'
#     collider='box',
#     shader=lit_with_shadows_shader
# )


# camera.position = (15, 100, 15)
# camera.rotation = (90, 0, 0)

camera.position = (20, 70, -55)
camera.rotation = (45, 0, 0)

def input(key):
    if key == 'space':
        projectiles.append(
            Projectile(
                speed=8,
                rotation=(player.rotation_y + 90),
                model='sphere',
                color=color.black,
                scale_x=0.5,
                scale_y=0.5,
                scale_z=0.5,
                position=(player.x, 0.5, player.z),
                # collider='mesh'
                collider='sphere',
                shader=lit_with_shadows_shader                
            )
        )
    elif key == 'r':
        for p in projectiles:
            destroy(p)

# def update():
#     for projectile in projectiles:
#         if projectile.intersects(player).hit:
#             projectile.color = color.lime
#             destroy(projectile)
#         else:
#             projectile.color = color.black

# this part will make the player move left or right based on our input.
# to check which keys are held down, we can check the held_keys dictionary.
# 0 means not pressed and 1 means pressed.
# time.dt is simply the time since the last frame. by multiplying with this, the
# player will move at the same speed regardless of how fast the game runs.


# def input(key):
#     if key == 'space':
#         player.y += 1
#         invoke(setattr, player, 'y', player.y-1, delay=.25)

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
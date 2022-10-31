from ursina import *
from ursina.shaders import *
from controllers import RotationController, DroneController, JumpController
from logger import Logger

from player import GenericPlayer, DronePlayer
from projectile import Projectile

# create a window
app = Ursina()
# most things in ursina are Entities. An Entity is a thing you place in the world.
# you can think of them as GameObjects in Unity or Actors in Unreal.
# the first paramenter tells us the Entity's model will be a 3d-model called 'cube'.
# ursina includes some basic models like 'cube', 'sphere' and 'quad'.

# test = Text(text='AAAAAAAA', x=-.85, y=.45)
logger = Logger(
    messages_to_display=20, 
    x_0=-.85,
    y_0=.45,
    dy=-.05
)


EditorCamera()

# in ursina, positive x is right, positive y is up, and positive z is forward.

projectiles = []

# sea = []
# for z in range(40):
#     for x in range(40):
#         sea.append(
#             Entity(
#                 model='cube',
#                 # color=color.blue,
#                 collider='box',
#                 position=(x, 0, z),
#                 parent=scene,
#                 origin_y=0.5,
#                 texture='models/water_2',
#                 shader=basic_lighting_shader
#             )
#         )

# # Ship
# player = GenericPlayer(
#     linear_velocity=6,
#     angular_velocity=120,
#     controller=RotationController,
#     model='models/pirate-ship-fat.obj', 
#     texture='models/pirate-ship-fat.mtl',
#     position=(0,-0.1,0),
#     # collider='mesh'
#     collider='box',
#     shader=lit_with_shadows_shader
# )


snow = []
for z in range(40):
    for x in range(40):
        snow.append(
            Entity(
                model='cube',
                # color=color.blue,
                collider='box',
                position=(x, 0, z),
                parent=scene,
                origin_y=0.5,
                texture='models/snow',
                shader=basic_lighting_shader
            )
        )

# Skier
player = GenericPlayer(
    linear_velocity=6,
    angular_velocity=120,
    controller=JumpController,
    logger=logger,
    scale_x=0.4,
    scale_y=0.4,
    scale_z=0.4,
    model='models/skier_1.obj', 
    texture='models/skier_1.mtl',
    position=(0,0.5,0),
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

# def input(key):
#     if key == 'space':
        # projectiles.append(
        #     Projectile(
        #         speed=8,
        #         rotation=(player.rotation_y + 90),
        #         model='sphere',
        #         color=color.black,
        #         scale_x=0.5,
        #         scale_y=0.5,
        #         scale_z=0.5,
        #         position=(player.x, 0.5, player.z),
        #         collider='sphere',
        #         shader=lit_with_shadows_shader                
        #     )
        # )
        # logger.log("Fire!")
    # elif key == 'r':
    #     for p in projectiles:
    #         destroy(p)
    #     logger.log("Reset all projectiles")


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

def update():
    if rail.intersects(player).hit:
        rail.color = color.lime
    else:
        rail.color = color.white

def input(key):
    if key == 'space':
        player.get_controller().set_vertical_vel(5)
        # player.y += 1
        # invoke(setattr, player, 'y', player.y-1, delay=.25)

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
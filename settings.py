#from numba import njit
import numpy as np
import glm
import math

# OpenGL settings
NUM_SAMPLES = 16 # antialiasing

# resolution
WIN_RES = glm.vec2(1280, 720)


# ray casting
MAX_RAY_DIST = 6

# chunk
CHUNK_SIZE = 48
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE
CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * math.sqrt(3)

# world
WORLD_W, WORLD_H = 3, 2
WORLD_D = WORLD_W
WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_AREA * WORLD_H

# world center
CENTER_XZ = WORLD_W * H_CHUNK_SIZE
CENTER_Y = WORLD_H * H_CHUNK_SIZE

# camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 80
V_FOV = glm.radians(FOV_DEG) # vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO) # horizontal fov
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(89)

# player
PLAYER_SPEED = 0.0065
PLAYER_SPEED_MIN = 0.0065
PLAYER_SPEED_MAX = 0.009

PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(CENTER_XZ, 100, CENTER_XZ)
MOUSE_SENSITIVITY = 0.002

# colors
BG_COLOR = glm.vec3(0.58, 0.83, 0.99)

# textures
VOID = 0
SAND = 1
GRASS = 2
DIRT = 3
GRAVEL = 4
STONE = 5
QUARTZ = 6
OAK_WOOD = 7
C_YELLOW = 8
C_WHITE = 9
C_GREEN = 10
C_BLUE = 11
C_ORANGE = 12
C_PINK = 13
C_BROWN = 14
C_BLACK = 15
C_GREY = 16
NUM_BLOCKS = 16

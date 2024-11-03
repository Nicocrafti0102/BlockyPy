import pygame as pg
from camera import Camera
from settings import *
from world_objects.crosshair import Crosshair

y_cam_brut = None
x_cam_brut = None
Name = "Nico"
x_cam = x_cam_brut
y_cam = y_cam_brut
Score = 52
IsAlive = True
IsShooting = False
equiped_weapon = 2


class Player(Camera):
    def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
        self.app = app
        super().__init__(position, yaw, pitch)


    def update(self, pg):
        self.keyboard_controls()
        self.mouse_control(pg)
        global x_cam
        global y_cam

        x_cam = x_cam_brut
        y_cam = y_cam_brut

        super().update()
        # if self.chunks:
        #     voxel_type = self.get_voxel_id(self.position)
        #     print("Voxel Type: ", voxel_type)
        ###Get INFO ####

    def render(self):
        pass
        #self.underwater_mesh.render()

    def get_voxel_id(self, voxel_world_pos):
        cx, cy, cz = chunk_pos = voxel_world_pos / CHUNK_SIZE

        if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:
            chunk_index = cx + WORLD_W * cz + WORLD_AREA * cy
            chunk = self.chunks[chunk_index]

            lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * CHUNK_SIZE

            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            voxel_id = chunk.voxels[voxel_index]

            return voxel_id, voxel_index, voxel_local_pos, chunk
        return 0, 0, 0, 0

    def handle_event(self, event, pg):
        voxel_handler = self.app.scene.world.voxel_handler

        if event.type == pg.MOUSEBUTTONDOWN:

            # adding and removing voxels with clicks
            if event.button == 1:
                voxel_handler.place_mode(True)
                voxel_handler.set_voxel(pg)
            if event.button == 3:
                voxel_handler.place_mode(False)
                voxel_handler.set_voxel(pg)


        if event.type == pg.MOUSEWHEEL:
            if event.y == 1:
                voxel_handler.set_voxel_id(voxel_handler.new_voxel_id + 1)
            if event.y == -1:
                voxel_handler.set_voxel_id(voxel_handler.new_voxel_id - 1)
    def mouse_control(self, pg):        
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        global x_cam_brut
        global y_cam_brut
        x_cam_brut = mouse_dx * MOUSE_SENSITIVITY
        y_cam_brut = mouse_dy * MOUSE_SENSITIVITY
        if mouse_dx:
            self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)

        pg.mouse.set_pos(WIN_RES.x / 2, WIN_RES.y / 2)

    def keyboard_controls(self):
        key_state = pg.key.get_pressed()
        if key_state[pg.K_LCTRL]:
            PLAYER_SPEED = PLAYER_SPEED_MAX
        else:
            PLAYER_SPEED = PLAYER_SPEED_MIN

        vel = PLAYER_SPEED * self.app.delta_time
        if key_state[pg.K_z]:
            self.move_forward(vel)
        if key_state[pg.K_s]:
            self.move_back(vel)
        if key_state[pg.K_q]:
            self.move_left(vel)
        if key_state[pg.K_d]:
            self.move_right(vel)
        if key_state[pg.K_SPACE]:
            self.jump()


        #if key_state[pg.K_LSHIFT]:
            #self.move_down(vel)


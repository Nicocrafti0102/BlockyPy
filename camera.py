from settings import *
from frustum import Frustum
from world import *
import time
import glm
import os

class Camera:
    def __init__(self, position, yaw, pitch, hitbox_radius=0.25):
        self.position = glm.vec3(position.x, position.y + 1.5, position.z)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)
        
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        self.m_proj = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()
        self.frustum = Frustum(self)
        
        self.is_jumping = False
        self.vertical_speed = 0.0
        self.gravity = -0.13333
        self.jump_force = 0.8 

        self.hitbox_radius = hitbox_radius

    def update(self):
        self.update_vectors()
        self.apply_gravity()
        self.update_view_matrix()

    def apply_gravity(self):
        if not self.is_on_ground(self.position, self.vertical_speed):
            self.vertical_speed += self.gravity / 60
        else:
            if self.vertical_speed < 0:
                self.vertical_speed = 0  
                self.is_jumping = False

        self.position.y += self.vertical_speed

    def jump(self):
        if self.is_on_ground(self.position, 0) and not self.is_jumping:
            self.is_jumping = True
            self.vertical_speed += self.jump_force / 10

    def is_on_ground(self, current_pos, direction):
        new_pos = glm.ivec3(current_pos.x, current_pos.y - 1.5, current_pos.z)
        new_pos += glm.ivec3(0, direction, 0)
        
        return World.is_voxel_at(new_pos)

    


    def update_view_matrix(self):
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self):
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
            self.yaw += delta_x

    def move_left(self, velocity):
        move_direction = -self.right * velocity
        new_position = self.position + move_direction
        if not self.is_colliding(new_position):
            self.position = new_position

    def move_right(self, velocity):
        move_direction = self.right * velocity
        new_position = self.position + move_direction
        if not self.is_colliding(new_position):
            self.position = new_position
        
    def move_forward(self, velocity):
        horizontal_forward = glm.vec3(self.forward.x, 0, self.forward.z)
        horizontal_forward = glm.normalize(horizontal_forward)
        move_direction = horizontal_forward * velocity
        new_position = self.position + move_direction
        if not self.is_colliding(new_position):
            self.position = new_position

    def move_back(self, velocity):
        horizontal_forward = glm.vec3(self.forward.x, 0, self.forward.z)
        horizontal_forward = glm.normalize(horizontal_forward)
        move_direction = -horizontal_forward * velocity
        new_position = self.position + move_direction
        if not self.is_colliding(new_position):
            self.position = new_position

    def is_colliding(self, new_position):
        offsets = [
            glm.vec3(0, 0, 0),
            glm.vec3(self.hitbox_radius, 0, 0),
            glm.vec3(-self.hitbox_radius, 0, 0),
            glm.vec3(0, 0, self.hitbox_radius),
            glm.vec3(0, 0, -self.hitbox_radius)
        ]
        
        check_positions = [
            glm.ivec3(new_position.x + offset.x, new_position.y + height, new_position.z + offset.z)
            for height in [0, 0.5, 1.0]
            for offset in offsets
        ]
        
        # Add positions at the player's head
        check_positions.extend([
            glm.ivec3(new_position.x + offset.x, new_position.y, new_position.z + offset.z)
            for offset in offsets
        ])
        
        for pos in check_positions:
            if World.is_voxel_at(pos):
                return True
        return False

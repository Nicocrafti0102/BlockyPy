from settings import *
from frustum import Frustum
from meshes.hotbar_icon_mesh import HotBarIconMesh
from meshes.hotbar_mesh import HotBarMesh
from world import *
import time
import glm
import os

class Camera:
    def __init__(self, position, yaw, pitch, hitbox_radius=0.25,head_pos=1.75):
        self.position = glm.vec3(position.x, position.y + head_pos, position.z)
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
        self.head_pos = head_pos

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

        if self.is_colliding(new_position):
            # Check if moving left would result in a collision
            # If so, reduce the velocity and change the move direction
            reduced_velocity = velocity / 1.01
            move_direction = -self.right * reduced_velocity

            # Try moving to the left and right to find a non-colliding position
            left_position = self.position + glm.vec3(-self.forward.z, 0, self.forward.x) * reduced_velocity
            right_position = self.position + glm.vec3(self.forward.z, 0, -self.forward.x) * reduced_velocity

            if not self.is_colliding(left_position):
                new_position = left_position
            elif not self.is_colliding(right_position):
                new_position = right_position

        if not self.is_colliding(new_position):
            self.position = new_position


    def move_right(self, velocity):
        move_direction = self.right * velocity
        new_position = self.position + move_direction

        if self.is_colliding(new_position):
            # Check if moving right would result in a collision
            # If so, reduce the velocity and change the move direction
            reduced_velocity = velocity / 1.01
            move_direction = self.right * reduced_velocity

            # Try moving to the left and right to find a non-colliding position
            left_position = self.position + glm.vec3(-self.forward.z, 0, self.forward.x) * reduced_velocity
            right_position = self.position + glm.vec3(self.forward.z, 0, -self.forward.x) * reduced_velocity

            if not self.is_colliding(left_position):
                new_position = left_position
            elif not self.is_colliding(right_position):
                new_position = right_position

        if not self.is_colliding(new_position):
            self.position = new_position


    def move_forward(self, velocity):
        horizontal_forward = glm.vec3(self.forward.x, 0, self.forward.z)
        horizontal_forward = glm.normalize(horizontal_forward)
        move_direction = horizontal_forward * velocity
        new_position = self.position + move_direction

        if self.is_colliding(new_position):
            # Check if moving forward would result in a collision
            # If so, reduce the velocity and change the move direction
            reduced_velocity = velocity / 1.01
            move_direction = horizontal_forward * reduced_velocity

            # Try moving to the left and right to find a non-colliding position
            left_position = self.position + glm.vec3(-self.forward.z, 0, self.forward.x) * reduced_velocity
            right_position = self.position + glm.vec3(self.forward.z, 0, -self.forward.x) * reduced_velocity

            if not self.is_colliding(left_position):
                new_position = left_position
            elif not self.is_colliding(right_position):
                new_position = right_position

        if not self.is_colliding(new_position):
            self.position = new_position


    def move_back(self, velocity):
        horizontal_forward = glm.vec3(self.forward.x, 0, self.forward.z)
        horizontal_forward = glm.normalize(horizontal_forward)
        move_direction = -horizontal_forward * velocity
        new_position = self.position + move_direction

        if self.is_colliding(new_position):
            # Check if moving back would result in a collision
            # If so, reduce the velocity and change the move direction
            reduced_velocity = velocity / 1.01
            move_direction = -horizontal_forward * reduced_velocity

            # Try moving to the left and right to find a non-colliding position
            left_position = self.position + glm.vec3(-self.forward.z, 0, self.forward.x) * reduced_velocity
            right_position = self.position + glm.vec3(self.forward.z, 0, -self.forward.x) * reduced_velocity

            if not self.is_colliding(left_position):
                new_position = left_position
            elif not self.is_colliding(right_position):
                new_position = right_position

        if not self.is_colliding(new_position):
            self.position = new_position

    def is_colliding(self, new_position):
        # Define the offsets for collision detection
        offsets = [
            glm.vec3(0, 0, 0),
            glm.vec3(self.hitbox_radius, 0, 0),
            glm.vec3(-self.hitbox_radius, 0, 0),
            glm.vec3(0, 0, self.hitbox_radius),
            glm.vec3(0, 0, -self.hitbox_radius),
            glm.vec3(0, -self.head_pos, 0),  # Adjust the offset for checking at the player's feet based on the player's height
            glm.vec3(0, 1.25 + self.jump_force, 0),  # Add offset for checking at the player's head and jump height
            glm.vec3(self.hitbox_radius, -1.0, 0),
            glm.vec3(-self.hitbox_radius, -1.0, 0),
            glm.vec3(0, -1.0, self.hitbox_radius),
            glm.vec3(0, -1.0, -self.hitbox_radius),
            glm.vec3(0, 1.0 + self.jump_force, self.hitbox_radius),
            glm.vec3(0, 1.0 + self.jump_force, -self.hitbox_radius),
            glm.vec3(self.hitbox_radius, 1.0 + self.jump_force, 0),
            glm.vec3(-self.hitbox_radius, 1.0 + self.jump_force, 0),
        ]

        # Check for collisions at the player's current position
        current_bounding_box = [
            glm.vec3(self.position.x + offset.x, self.position.y + height, self.position.z + offset.z)
            for height in [-0.5, 1.5]  # Adjust the height range to include the player's height
            for offset in offsets
        ]

        for pos in current_bounding_box:
            if World.is_voxel_at(pos):
                return True

        # Check for collisions at the player's new position after applying the jump force
        new_bounding_box = [
            glm.vec3(new_position.x + offset.x, new_position.y + height, new_position.z + offset.z)
            for height in [-0.5, 1.5 + self.jump_force]  # Adjust the height range to include the player's height and jump height
            for offset in offsets
        ]

        for pos in new_bounding_box:
            if World.is_voxel_at(pos):
                return True

        return False
from settings import *
from world import World
from world_objects.voxel_marker import VoxelMarker
from world_objects.crosshair import Crosshair
from meshes.quad_mesh import QuadMesh
from world_objects.hotbar import HotBar

class Scene:
    def __init__(self, app):
        self.app = app
        self.world = World(self.app)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)
        self.quad_mesh = QuadMesh(self.app)
        self.hotbar = HotBar(self.world.voxel_handler)

    def update(self):
        self.world.update()
        self.voxel_marker.update()
        self.hotbar.update()
        player_pos = glm.ivec3(int(self.app.player.position.x), int(self.app.player.position.y), int(self.app.player.position.z))
        voxel_id, voxel_index, voxel_local_pos, chunk = self.get_voxel_id(player_pos)

    def render(self):
        self.world.render()
        self.voxel_marker.render()
        self.quad_mesh.render()
        self.hotbar.render()

    def get_voxel_id(self, voxel_world_pos=glm.ivec3):
        cx, cy, cz = chunk_pos = voxel_world_pos / CHUNK_SIZE

        if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:
            chunk_index = int(cx + WORLD_W * cz + WORLD_AREA * cy)
            chunk = self.world.chunks[chunk_index]

            lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * CHUNK_SIZE

            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            voxel_id = chunk.voxels[voxel_index]

            return voxel_id, voxel_index, voxel_local_pos, chunk
        return 0, 0, 0, 0
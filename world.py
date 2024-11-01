from settings import *
from world_objects.chunk import Chunk
from meshes.chunk_mesh_builder import get_chunk_index
from voxel_handler import VoxelHandler
from world import *
import numpy as np

class World:
    _instance = None

    def __init__(self, app):
        self.app = app
        World._instance = self
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype='uint8')
        self.build_chunks()
        self.build_chunk_mesh()
        
        self.voxel_handler = VoxelHandler(self)

    def build_chunks(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    # Put the chunk voxels in a separate array
                    self.voxels[chunk_index] = chunk.build_voxels()

                    # Get pointer to voxels
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        self.voxel_handler.update()

    def render(self):
        for chunk in self.chunks:
            chunk.render()

    @staticmethod
    def is_voxel_at(pos):
        voxel_id = World.get_voxel_at(World._instance, pos)
        return voxel_id != 0

    @staticmethod
    def get_voxel_at(world_instance, pos):
        # Convertir en indices entiers pour la position du chunk
        cx, cy, cz = int(pos.x // CHUNK_SIZE), int(pos.y // CHUNK_SIZE), int(pos.z // CHUNK_SIZE)
        
        # Vérifier les limites du monde
        if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:
            chunk_index = cx + WORLD_W * cz + WORLD_AREA * cy
            chunk = world_instance.chunks[chunk_index]

            # Position locale dans le chunk
            lx, ly, lz = int(pos.x % CHUNK_SIZE), int(pos.y % CHUNK_SIZE), int(pos.z % CHUNK_SIZE)
            
            # Vérifier les limites du chunk
            if 0 <= lx < CHUNK_SIZE and 0 <= ly < CHUNK_SIZE and 0 <= lz < CHUNK_SIZE:
                voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
                voxel_id = chunk.voxels[voxel_index]
                return voxel_id
            
        # Retourner 0 si hors des limites
        return 0
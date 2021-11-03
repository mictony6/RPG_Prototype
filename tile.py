import pygame
from config import tile_size


class Tile(pygame.sprite.Sprite):
    def __init__(self, chunk_pos, chunk_size):
        super().__init__()
        self.image = pygame.Surface((chunk_size, chunk_size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=chunk_pos)

    def update(self, vector):
        self.rect.x += vector.x
        self.rect.y += vector.y


class TileSlab(pygame.sprite.Sprite):
    # dirty version of the Chunk system
    # is 32x32 by default but can be 64x32 or 32x64
    def __init__(self, chunk_pos, chunk_size=(tile_size/2, tile_size/2), pos='center'):
        super().__init__()
        self.image = pygame.Surface(chunk_size)
        self.image.fill('grey')
        width = chunk_size[0]
        lenght = chunk_size[1]
        if pos == "topleft":
            self.rect = self.image.get_rect(topleft=chunk_pos)
        elif pos == "topright":
            chunk_pos = (chunk_pos[0] + width, chunk_pos[1])
            self.rect = self.image.get_rect(topleft=chunk_pos)
        elif pos == "bottomleft":
            chunk_pos = (chunk_pos[0], chunk_pos[1] + lenght)
            self.rect = self.image.get_rect(topleft=chunk_pos)
        elif pos == "bottomright":
            chunk_pos = (chunk_pos[0] + width, chunk_pos[1] + lenght)
            self.rect = self.image.get_rect(topleft=chunk_pos)
        elif pos == "top":
            chunk_pos = (chunk_pos[0] + width/2, chunk_pos[1])
            self.rect = self.image.get_rect(topleft=chunk_pos)
        elif pos == "bottom":
            chunk_pos = (chunk_pos[0] + width/2, chunk_pos[1] + lenght)
            self.rect = self.image.get_rect(topleft=chunk_pos)
        elif pos == "left":
            chunk_pos = (chunk_pos[0], chunk_pos[1] + lenght/2)
            self.rect = self.image.get_rect(topleft=chunk_pos)
        elif pos == "right":
            chunk_pos = (chunk_pos[0]+width, chunk_pos[1] + lenght/2)
            self.rect = self.image.get_rect(topleft=chunk_pos)
        else:
            chunk_pos = (chunk_pos[0] + width / 2, chunk_pos[1] + lenght / 2)
            self.rect = self.image.get_rect(topleft=chunk_pos)

    def update(self, vector):
        self.rect.x += vector.x
        self.rect.y += vector.y

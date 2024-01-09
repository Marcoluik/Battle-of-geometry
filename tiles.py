import pygame
from settings import WIDTH, HEIGHT
import random

class Tiles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        tile_size = 32
        rows = HEIGHT // tile_size + 1
        cols = WIDTH // tile_size + 1
        self.tiles = []
        for i in range(cols):
            for k in range(rows):
                tile_chords = (i*tile_size, k*tile_size)
                tile_rect = pygame.Rect(tile_chords[0], tile_chords[1], tile_size, tile_size)
                offset = random.randint(-20, 20)
                depth = (HEIGHT - tile_chords[1]) / HEIGHT * 255 + offset
                depth = max(0, min(100-offset, depth))

                tile_color = (depth, depth, depth)
                tile = {"rect": tile_rect, "color": tile_color}
                self.tiles.append(tile)
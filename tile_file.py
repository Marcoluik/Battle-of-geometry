import pygame
import random
import math
import screens
WIDTH, HEIGHT = screens.WIDTH, screens.HEIGHT

class Tiles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tile_size = 32
        self.randomm = random.choice(
            ["Moon", "Red_Moon", "Green_Moon", "Blue_Moon", "Yellow_Moon", "Cyan_Moon", "Purple_Moon"])
        self.rows = HEIGHT // self.tile_size + 1
        self.cols = WIDTH // self.tile_size + 1
        self.center_x, self.center_y = WIDTH // 2, HEIGHT // 2
        self.max_radius = min(self.center_x, self.center_y)  # Radius for the brightest area
        self.update_interval = 300  # Number of frames to wait before updatin
        self.last_update_time = pygame.time.get_ticks()  # Last update time
        self.horizontal_shift = 0  # Horizontal shift for the moon
        self.tiles = []
        self.generate_tiles()  # Initial tile generation

    def generate_tiles(self):


        self.tiles.clear()  # Clear existing tiles
        for i in range(self.cols):
            for k in range(self.rows):
                tile_chords = (i * self.tile_size + self.horizontal_shift, k * self.tile_size)
                tile_rect = pygame.Rect(tile_chords[0], tile_chords[1], self.tile_size, self.tile_size)

                # Calculate the distance from the shifted center
                distance = math.sqrt((tile_chords[0] - (self.center_x + self.horizontal_shift)) ** 2 +
                                     (tile_chords[1] - self.center_y) ** 2)

                # Adjust depth based on the distance from the center
                if distance < self.max_radius:
                    depth = 150
                else:
                    depth = max(0, 150 - (distance - self.max_radius))

                offset = random.randint(-40, 40)
                depth = max(0, min(150, depth + offset))
                moon_colors = {
                    "Moon": (depth, depth, depth),
                    "Red_Moon": (depth, 0, 0),
                    "Green_Moon": (0, depth, 0),
                    "Blue_Moon": (0, 0, depth),
                    "Yellow_Moon": (depth, depth, 0),
                    "Cyan_Moon": (0, depth, depth),
                    "Purple_Moon": (depth, 0, depth)
                }

                tile = {"rect": tile_rect, "color": moon_colors[self.randomm]}
                self.tiles.append(tile)

    def update(self):
        #self.randomm = random.choice(
            #["Moon", "Red_Moon", "Green_Moon", "Blue_Moon", "Yellow_Moon", "Cyan_Moon", "Purple_Moon"])
        current_time = pygame.time.get_ticks()
        # Check if the current time exceeds the last update time by the update interval
        if current_time - self.last_update_time > self.update_interval:
            self.horizontal_shift += self.tile_size  # Increase the horizontal shift
            self.generate_tiles()  # Generate new tiles
            self.last_update_time = current_time  # Update the last update time
import pygame
import random
import math
import screens
from collections import deque
WIDTH, HEIGHT = screens.WIDTH, screens.HEIGHT

class Tiles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.tile_size = 32
        self.rows = HEIGHT // self.tile_size + 1
        self.cols = WIDTH // self.tile_size + 2  # +2 to accommodate the sliding in of the new moon
        self.center_x, self.center_y = WIDTH // 2, HEIGHT // 2
        self.max_radius = min(self.center_x, self.center_y)
        self.update_interval = 400
        self.last_update_time = pygame.time.get_ticks()
        self.horizontal_shift = 0
        self.moon_colors_queue = deque(self.generate_moon_sequence(10))
        self.current_moon_tiles = []
        self.next_moon_tiles = []
        self.generate_tiles()
    def generate_moon_sequence(self, length):
        options = ["Moon", "Red_Moon", "Green_Moon", "Blue_Moon", "Yellow_Moon", "Cyan_Moon", "Purple_Moon"]
        return [random.choice(options) for _ in range(length)]

    def generate_tiles(self):
        self.current_moon_tiles = self.create_moon_tiles(self.moon_colors_queue[0], 0)
        self.next_moon_tiles = self.create_moon_tiles(self.moon_colors_queue[1], -WIDTH)


    def create_moon_tiles(self, moon_color, initial_shift):
        tiles = []
        for i in range(self.cols):
            for k in range(self.rows):
                tile_chords = (i * self.tile_size + initial_shift, k * self.tile_size)
                tile_rect = pygame.Rect(tile_chords[0], tile_chords[1], self.tile_size, self.tile_size)
                distance = math.sqrt(
                    (tile_chords[0] - (self.center_x + initial_shift)) ** 2 + (tile_chords[1] - self.center_y) ** 2)
                depth = self.calculate_depth(distance)
                color = self.get_moon_color(depth, moon_color)
                tile = {"rect": tile_rect, "color": color}
                tiles.append(tile)
        return tiles


    def calculate_depth(self, distance):
            if distance < self.max_radius:
                depth = 150
            else:
                depth = max(0, 150 - (distance - self.max_radius))
            offset = random.randint(-40, 40)
            return max(0, min(150, depth + offset))

    def get_moon_color(self, depth, moon_type):

        moon_colors = {
            "Moon": (depth, depth, depth),
            "Red_Moon": (depth, 0, 0),
            "Green_Moon": (0, depth, 0),
            "Blue_Moon": (0, 0, depth),
            "Yellow_Moon": (depth, depth, 0),
            "Cyan_Moon": (0, depth, depth),
            "Purple_Moon": (depth, 0, depth)
        }
        return moon_colors[moon_type]


    def update(self):
        print("Yes")
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > self.update_interval:
            self.horizontal_shift += self.tile_size /4  # Adjust the speed of the slide

            # Update the positions of current and next moon tiles
            for tile in self.current_moon_tiles:
                tile['rect'].x += self.tile_size / 4
            for tile in self.next_moon_tiles:
                tile['rect'].x += self.tile_size / 4

            # Check if the current moon has completely left the screen
            if self.current_moon_tiles[0]['rect'].x > WIDTH:
                self.horizontal_shift = 0
                self.moon_colors_queue.popleft()  # Move to the next moon
                self.current_moon_tiles = self.next_moon_tiles
                next_moon_color = self.moon_colors_queue[1] if len(self.moon_colors_queue) > 1 else random.choice(
                    ["Moon", "Red_Moon", "Green_Moon", "Blue_Moon", "Yellow_Moon", "Cyan_Moon", "Purple_Moon"])
                self.next_moon_tiles = self.create_moon_tiles(next_moon_color, -WIDTH)

            self.last_update_time = current_time


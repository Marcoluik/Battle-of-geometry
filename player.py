import pygame
import main
from settings import WIDTH, HEIGHT, WHITE

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.color = WHITE
        self.speed = 5
        self.health = 3
        self.dash_speed = 40  # Speed of dash
        self.dash_cooldown = 500  # Cooldown in milliseconds
        self.last_dash = 0  # Time since last dash
        self.experience = 0
        self.coins = 0

    def draw(self, screen):
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        pygame.draw.circle(screen, self.color, (center_x, center_y), self.size // 2)

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Constrain the new position to be within the screen boundaries
        # Adjust for the size of the player to prevent partial off-screen movement
        half_size = self.size // 2
        new_x = max(half_size, min(WIDTH - half_size, new_x))
        new_y = max(half_size, min(HEIGHT - half_size, new_y))

        # Update player's position
        self.x = new_x
        self.y = new_y

    def collides_with(self, other):
        distance_x = (self.x + self.size // 2) - (other.x + other.size // 2)
        distance_y = (self.y + self.size // 2) - (other.y + other.size // 2)
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

        # Check if the distance is less than the sum of the radii
        return distance < (self.size // 2 + other.size // 2)

    def dash(self, current_time):
        if current_time - self.last_dash > self.dash_cooldown:
            self.last_dash = current_time
            # Dash mechanics (e.g., increase speed or teleport forward)
            # Example: Increase speed for a single frame
            self.speed += self.dash_speed
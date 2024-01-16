import pygame
import math
class Projectile:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.size = 5
        self.color = (255, 255, 0)
        self.speed = 10
        self.dx = dx
        self.dy = dy

        self.image = pygame.image.load("FrostLaser.png").convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.center = (self.x, self.y)

        # Calculate the angle (in degrees)
        angle = math.degrees(math.atan2(-self.dy, self.dx))
        self.rotated_image = pygame.transform.rotate(self.image, angle)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)


    def draw(self, screen):
        screen.blit(self.rotated_image, self.rect)

    def collides_with(self, other):
        return (self.x < other.x + other.size and self.x + self.size > other.x and
                self.y < other.y + other.size and self.y + self.size > other.y)
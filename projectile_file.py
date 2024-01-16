import pygame

class Projectile:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.size = 5
        self.color = (255, 255, 0)
        self.speed = 10
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def collides_with(self, other):
        return (self.x < other.x + other.size and self.x + self.size > other.x and
                self.y < other.y + other.size and self.y + self.size > other.y)
import pygame
from settings import WHITE, HEIGHT, WIDTH, BLACK

class MeteorEvent:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.speed = 5
        self.size = 25
        self.color = (255, 255, 255)

        self.image = pygame.image.load("Images/meteor.png")
        self.image = pygame.transform.scale(self.image, (64, 64))


        self.sprite_mask = pygame.mask.from_surface(self.image)
        self.angle = 0  # Initial rotation angle

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, self.rect)

    def update(self):
        self.x -= 0.8*self.speed
        self.y += self.speed
        # Update rotation angle
        self.angle += 4  # You can adjust the rotation speed by changing this value

        # Keep the angle within 360 degrees
        if self.angle >= 360:
            self.angle = 0

    def collides_with(self, other):
        return (self.x < other.x and self.x + self.radius > other.x and
                self.y < other.y and self.y + self.radius > other.y)
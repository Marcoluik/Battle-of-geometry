import pygame
import math
from settings import WHITE, HEIGHT, WIDTH, BLACK


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy, sprite_sheet, frame_width, frame_height):
        super().__init__()
        self.sprite_sheet = sprite_sheet
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 10
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.current_frame = 0
        self.angle = math.degrees(math.atan2(-self.dy, self.dx))  # Initialize angle before calling get_image
        self.image = self.get_image(0, frame_width, frame_height)  # Get the first frame after setting the angle
        self.rect = self.image.get_rect(center=(x, y))

    def get_image(self, frame, width, height):
        image = pygame.Surface((width, height), pygame.SRCALPHA)  # Use SRCALPHA to handle transparency
        image.blit(self.sprite_sheet, (0, 0), (frame * width, 0, width, height))
        image = pygame.transform.rotate(image, self.angle)  # Rotate the image by the current angle
        image.set_colorkey(BLACK)  # Set transparency color
        return image

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.center = (self.x, self.y)
        self.angle = math.degrees(math.atan2(-self.dy, self.dx))
        self.current_frame = (self.current_frame + 1) % 3  # Assuming you have 3 frames
        self.image = self.get_image(self.current_frame, self.frame_width, self.frame_height)

    def collides_with(self, other):
        return self.rect.colliderect(other.rect)

class Laser(Projectile):
    def __init__(self, x, y, dx, dy):
        sprite_sheet = pygame.image.load("PureLaserSheet.png").convert_alpha()
        super().__init__(x, y, dx, dy, sprite_sheet, 32, 32)  # Assuming frame width and height are 32

class FireLaser(Projectile):
    def __init__(self, x, y, dx, dy):
        sprite_sheet = pygame.image.load("FireLaserSheet.png").convert_alpha()
        super().__init__(x, y, dx, dy, sprite_sheet, 32, 32)  # Assuming frame width and height are 32

class FrostLaser(Projectile):
    def __init__(self, x, y, dx, dy):
        sprite_sheet = pygame.image.load("FrostLaserSheet.png").convert_alpha()
        super().__init__(x, y, dx, dy, sprite_sheet, 32, 32)  # Assuming frame width and height are 32

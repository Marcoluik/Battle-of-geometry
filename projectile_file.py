import pygame
import math
from settings import WHITE, HEIGHT, WIDTH, BLACK

def get_image(sheet, frame, width, height, scale, angle):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0,0), ((frame*width), 0, width, height))
    image = pygame.transform.scale(image, (width*scale, height*scale))
    image = pygame.transform.rotate(image, angle)
    image.set_colorkey((0, 0, 0))

    return image
class Projectile:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.size = 5
        self.color = (255, 255, 0)
        self.speed = 10
        self.dx = dx
        self.dy = dy
        self.stylesheet = ""
        self.rect = self.image.get_rect(center=(self.x, self.y))


    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.center = (self.x, self.y)

        self.angle = math.degrees(math.atan2(-self.dy, self.dx))
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)


    def draw(self, screen):
        sprite = get_image(self.style_sheet, self.frame, 32, 32, 2, self.angle)
        screen.blit(sprite, self.rect)


    def collides_with(self, other):
        return (self.x < other.x + other.size and self.x + self.size > other.x and
                self.y < other.y + other.size and self.y + self.size > other.y)

class Beam(Projectile):
    def __init__(self):
        super().__init__()

class Laser(Projectile):
    def __init__(self):
        super().__init__()
        self.style_sheet = pygame.image.load("PureLaserSheet.png").convert_alpha()

class FireLaser(Projectile):
    def __init__(self):
        super().__init__()
        self.style_sheet = pygame.image.load("FireLaserSheet.png").convert_alpha()

        self.rect = self.image.get_rect()
class FrostLaser(Projectile):
    def __init__(self):
        super().__init__()
        self.style_sheet = pygame.image.load("FrostLaserSheet.png").convert_alpha()

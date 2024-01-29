import pygame
import math
from settings import WHITE, HEIGHT, WIDTH, BLACK

def get_image(sheet, frame, width, height, scale, angle):
    image = pygame.Surface((width, height))
    image.blit(sheet, (0,0), ((frame*width), 0, width, height))
    image = pygame.transform.scale(image, (width*scale, height*scale))
    image = pygame.transform.rotate(image, angle)
    image.set_colorkey((0, 0, 0))


    return image

class Projectile:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.color = (255, 255, 0)
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.center = (self.x, self.y)

        # Calculate the angle (in degrees)
        angle = math.degrees(math.atan2(-self.dy, self.dx))+90
        self.rotated_image = pygame.transform.rotate(self.image, angle)
        self.rect = self.rotated_image.get_rect(center=self.rect.center)


    def draw(self, screen):
        screen.blit(self.rotated_image, self.rect)

    def collides_with(self, other):
        return (self.x < other.x + other.size and self.x + self.size > other.x and
                self.y < other.y + other.size and self.y + self.size > other.y)

class Laser_Projectile(Projectile):
    def __init__(self, x, y, dx, dy):
        super(Laser_Projectile, self).__init__(x, y, dx, dy)
        self.size = 3
        self.speed = 10

        self.frame = 0
        #self.sprite_sheet = pygame.image.load("Images/LaserSprite.png").convert_alpha()
        self.angle = math.degrees(math.atan2(-self.dy, self.dx))+90
        self.image = pygame.image.load("Images/LaserSprite.png").convert_alpha()

        self.sprite_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.x, self.y))

class Rotating_Enemy_Projectile(Projectile):
    def __init__(self, x, y, dx, dy, vinkel):
        super(Rotating_Enemy_Projectile, self).__init__(x, y, dx, dy)
        self.size = 4
        self.speed = 10

        self.frame = 2
        self.sprite_sheet = pygame.image.load("Images/RotatingProjectileEnemy.png").convert_alpha()
        self.angle = vinkel+90
        self.image = get_image(self.sprite_sheet, self.frame, 32, 32, 2, self.angle)

        self.sprite_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rect)
        if self.frame >= 3:
            self.frame = 0
        else:
            self.frame += 1
        self.image = get_image(self.sprite_sheet, math.floor(self.frame), 32, 32, 3, self.angle)

class ProjectileEffect():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.frame = 0
        self.radius = 1

    def draw(self, screen):
        self.radius = 20/(1+5*math.e**(-0.01*20*self.frame))+2
        pygame.draw.circle(screen, center=(self.x, self.y), color=(255, 0, 0), radius=self.radius)
        pygame.draw.circle(screen, center=(self.x, self.y), color=(255, 255, 255), radius=self.radius-2)
        self.frame += 1


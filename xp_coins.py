import pygame, math

def get_image(sheet, frame, width, height, scale, angle):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0,0), ((frame*width), 0, width, height))
    image = pygame.transform.scale(image, (width*scale, height*scale))
    image = pygame.transform.rotate(image, angle)
    image.set_colorkey((0, 0, 0))

    return image

class Item:
    def __init__(self, x, y, size, color, sprite_amount, spritesheet):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.frame = 0
        self.spritesheet = spritesheet
        self.sprite_amount = sprite_amount

    def draw(self, screen):
        #pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        if self.frame >= self.sprite_amount:
            self.frame = 0
        else:
            self.frame+=0.4
        sprite = get_image(self.spritesheet, math.floor(self.frame), 32, 32, 1, 0)
        screen.blit(sprite, (self.x-32, self.y-32))


class Coin(Item):
    def __init__(self, x, y):
        super().__init__(x+5, y+5, 10, (255, 215, 0), 9, pygame.image.load("Images/Coin-Spritesheet.png").convert_alpha())  # Gold color

class Experience(Item):
    def __init__(self, x, y):
        super().__init__(x-5, y-5, 8, (0, 255, 0), 7, pygame.image.load("Images/XP-Spritesheet.png").convert_alpha())  # Green color
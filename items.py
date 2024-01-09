import pygame

class Item:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

class Coin(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 10, (255, 215, 0))  # Gold color

class Experience(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 8, (0, 255, 0))  # Green color
import pygame
import math
from settings import WIDTH, HEIGHT
from utilities import generate_safe_spawn
# Import Coin and Experience classes if they are in separate modules
from items import Coin, Experience

class Enemy:
    def __init__(self, player):
        safe_x, safe_y = generate_safe_spawn(player)
        self.x = safe_x
        self.y = safe_y
        self.size = 15
        self.color = (255, 0, 0)
        self.speed = 2
        self.health = 2

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move_towards_player(self, player, enemies):
        # Proposed movement
        new_x = self.x
        new_y = self.y

        if self.x < player.x:
            new_x += self.speed
        elif self.x > player.x:
            new_x -= self.speed
        if self.y < player.y:
            new_y += self.speed
        elif self.y > player.y:
            new_y -= self.speed

        # Check for collision with other enemies
        for enemy in enemies:
            if enemy != self and self.collides_with(new_x, new_y, enemy):
                return  # Skip movement if collision detected

        # Update position
        self.x = new_x
        self.y = new_y

    def collides_with(self, x, y, other):
        return (x < other.x + other.size and x + self.size > other.x and
                y < other.y + other.size and y + self.size > other.y)

    def take_damage(self, coins, experience_points):
        self.health -= 1
        if self.health <= 0:
            for _ in range(self.vertices):
                coins.append(Coin(self.x, self.y))
                experience_points.append(Experience(self.x, self.y))
            return True
        return False

class TriangleEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.vertices = 3  # Triangle
        self.color = (255, 0, 0)  # Red color
        self.health = 3  # Health value for TriangleEnemy
        self.size = 10
        self.speed = 4

    def draw(self, screen):
        radius = self.size
        points = []
        for i in range(3):
            angle = math.radians(120 * i - 30)  # Equilateral triangle points
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(screen, self.color, points)



class SquareEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.vertices = 4  # Square
        self.color = (0, 255, 0)  # Green color
        self.health = 4  # Health value for SquareEnemy
        self.size = 15
        self.speed = 3

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))


class PentagonEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.vertices = 5  # Pentagon
        self.color = (0, 0, 255)  # Blue color
        self.health = 5  # Health value for PentagonEnemy
        self.size = 20
        self.speed = 2

    def draw(self, screen):
        radius = self.size
        points = []
        for i in range(5):  # Pentagon has 5 sides
            angle = math.radians(72 * i - 36)  # 360 degrees / 5 sides
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(screen, self.color, points)


class HexagonEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.vertices = 6
        self.color = (255, 255, 0)  # Yellow color
        self.health = 6  # Health value for HexagonEnemy
        self.size = 30
        self.speed = 1

    def draw(self, screen):
        radius = self.size
        points = []
        for i in range(6):  # Hexagon has 6 sides
            angle = math.radians(60 * i - 30)  # 360 degrees / 6 sides
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(screen, self.color, points)
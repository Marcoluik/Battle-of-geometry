import pygame
import math
import random
import player_file
import xp_coins
import screens

WIDTH, HEIGHT = screens.WIDTH, screens.HEIGHT
player = player_file.Player(WIDTH // 2, HEIGHT // 2)
def generate_safe_spawn(player, min_distance=400):
    while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        distance = math.sqrt((player.x - x) ** 2 + (player.y - y) ** 2)
        if distance >= min_distance:
            return x, y

class Enemy:
    def __init__(self):
        safe_x, safe_y = generate_safe_spawn(player)
        self.x = safe_x
        self.y = safe_y
        self.size = 15
        self.color = (255, 0, 0)
        self.speed = 2
        self.health = 2
        self.avoidance_radius = 20  # Radius for collision avoidance

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def move_towards_player(self, player, enemies):
        # Adjusted movement to be more fluid
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize

        # Potential new position
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Avoidance behavior
        new_x, new_y = self.avoid_collisions(new_x, new_y, enemies)

        # Update position
        self.x = new_x
        self.y = new_y

    def avoid_collisions(self, new_x, new_y, enemies):
        for enemy in enemies:
            if enemy != self and self.too_close(new_x, new_y, enemy):
                # Calculate direction vector from enemy to self
                avoid_dx, avoid_dy = new_x - enemy.x, new_y - enemy.y
                avoid_dist = math.hypot(avoid_dx, avoid_dy)

                # If too close, adjust position to avoid collision
                if avoid_dist < self.avoidance_radius:
                    # Normalize the direction vector
                    avoid_dx, avoid_dy = avoid_dx / avoid_dist, avoid_dy / avoid_dist
                    # Move away from the other enemy
                    new_x += avoid_dx * self.speed
                    new_y += avoid_dy * self.speed

        return new_x, new_y

    def too_close(self, x, y, other):
        # Check if the current enemy position is too close to another enemy
        return math.hypot(x - other.x, y - other.y) < self.avoidance_radius

    def collides_with(self, x, y, other):
        return (x < other.x + other.size and x + self.size > other.x and
                y < other.y + other.size and y + self.size > other.y)

    def take_damage(self, coins, experience_points):
        self.health -= player.attackdmg
        if self.health <= 0:
            for _ in range(self.vertices):
                coins.append(xp_coins.Coin(self.x, self.y))
                experience_points.append(xp_coins.Experience(self.x, self.y))
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
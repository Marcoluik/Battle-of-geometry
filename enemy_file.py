import pygame
import math
import random
import player_file
import xp_coins
import screens

from settings import WHITE, HEIGHT, WIDTH, BLACK
player = player_file.Player(WIDTH // 2, HEIGHT // 2)
def generate_safe_spawn(player, min_distance=400):
    while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        distance = math.sqrt((player.x - x) ** 2 + (player.y - y) ** 2)
        if distance >= min_distance:
            return x, y

def get_image(sheet, frame, width, height, scale, angle):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0,0), ((frame*width), 0, width, height))
    image = pygame.transform.scale(image, (width*scale, height*scale))
    image = pygame.transform.rotate(image, angle)
    image.set_colorkey((0, 0, 0))

    return image

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
        self.player_instance = player
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
        self.size = 20
        self.speed = 4
        self.frame = 0
        self.sprite_sheet = pygame.image.load("Images/TriangleSpaceshipSpritesheet.png").convert_alpha()

    def draw(self, screen):
        """radius = self.size
        points = []
        for i in range(3):
            angle = math.radians(120 * i - 30)  # Equilateral triangle points
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(screen, self.color, points)"""
        #pygame.draw.circle(screen, self.color, center=(self.x, self.y), radius=self.size)
        vector_enemy_player = (self.player_instance.x-self.x, self.player_instance.y-self.y)
        if vector_enemy_player[0] < 0:
            vinkel = -math.degrees(math.atan(vector_enemy_player[1]/vector_enemy_player[0]))+90
        else:
            vinkel = -math.degrees(math.atan(vector_enemy_player[1]/vector_enemy_player[0]))-90
        sprite = get_image(self.sprite_sheet, math.floor(self.frame), 32, 32, 2, vinkel)
        if self.frame >= 2:
            self.frame = 0
        else:
            self.frame+=0.4
            print(self.frame)
        screen.blit(sprite, (self.x-32, self.y-32))




class SquareEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.vertices = 4  # Square
        self.color = (0, 255, 0)  # Green color
        self.health = 4  # Health value for SquareEnemy
        self.size = 20
        self.speed = 3
        self.frame = 0
        self.sprite_sheet = pygame.image.load("Images/SmallSpaceshipSpritesheetHorizontal.png").convert_alpha()


    def draw(self, screen):
        #pygame.draw.circle(screen, self.color, center=(self.x, self.y), radius=self.size)
        vector_enemy_player = (self.player_instance.x - self.x, self.player_instance.y - self.y)
        if vector_enemy_player[0] < 0:
            vinkel = -math.degrees(math.atan(vector_enemy_player[1] / vector_enemy_player[0])) + 90
        else:
            vinkel = -math.degrees(math.atan(vector_enemy_player[1] / vector_enemy_player[0])) - 90
        sprite = get_image(self.sprite_sheet, math.floor(self.frame), 32, 32, 2, vinkel)
        if self.frame >= 2:
            self.frame = 0
        else:
            self.frame += 0.4
            print(self.frame)
        screen.blit(sprite, (self.x-32, self.y-32))


class PentagonEnemy(Enemy):
    def __init__(self):
        super().__init__()
        self.vertices = 5  # Pentagon
        self.color = (0, 0, 255)  # Blue color
        self.health = 5  # Health value for PentagonEnemy
        self.size = 20
        self.speed = 2
        self.frame = 0
        self.sprite_sheet = pygame.image.load("Images/SpaceshipRotatingSpritesheet.png").convert_alpha()


    def draw(self, screen):
        """radius = self.size
        points = []
        for i in range(5):  # Pentagon has 5 sides
            angle = math.radians(72 * i - 36)  # 360 degrees / 5 sides
            x = self.x + radius * math.cos(angle)
            y = self.y + radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(screen, self.color, points)"""
        pygame.draw.circle(screen, self.color, center=(self.x,self.y), radius=self.size)
        vector_enemy_player = (self.player_instance.x - self.x, self.player_instance.y - self.y)
        if vector_enemy_player[0] < 0:
            vinkel = -math.degrees(math.atan(vector_enemy_player[1] / vector_enemy_player[0])) + 90
        else:
            vinkel = -math.degrees(math.atan(vector_enemy_player[1] / vector_enemy_player[0])) - 90
        sprite = get_image(self.sprite_sheet, math.floor(self.frame), 32, 32, 2, vinkel)
        if self.frame >= 3:
            self.frame = 0
        else:
            self.frame += 0.4
        screen.blit(sprite, (self.x - 32, self.y - 32))


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
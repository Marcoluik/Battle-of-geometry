import pygame
import random
import math
# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle of geometry")
enemy_spawn_time = 2  # Timer for enemy spawning
spawn_interval = 3000  # 10 seconds in milliseconds
spawn_count = 2  # Initial number of enemies to spawn
# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game clock
clock = pygame.time.Clock()
FPS = 60
#font = pygame.font.SysFont(None, 36)
font = pygame.font.Font("pixelletters.ttf",36)
# Game loop flag
running = True


def start_screen(screen):
    title_font = pygame.font.Font("pixelletters.ttf", 72)
    start_font = pygame.font.Font("pixelletters.ttf", 36)
    guide_font = pygame.font.Font("pixelletters.ttf", 30)

    title_text = title_font.render('Battle of Geometry', True, WHITE)
    start_text = start_font.render('Press Any Key to Start', True, WHITE)
    guide_text = guide_font.render('WASD to move, shoot with left click, aim with mouse, dash on space', True, WHITE)



    screen.fill(BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))
    screen.blit(guide_text, (WIDTH // 2 - guide_text.get_width() // 2, HEIGHT // 2 + 150))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

def generate_safe_spawn(player, min_distance=100):
    while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        distance = math.sqrt((player.x - x) ** 2 + (player.y - y) ** 2)
        if distance >= min_distance:
            return x, y

def game_over_screen(screen, coins_collected):
    game_over_font = pygame.font.Font("pixelletters.ttf",72)
    coins_font = pygame.font.Font("pixelletters.ttf",50)
    try_again_font = pygame.font.Font("pixelletters.ttf",50)
    back_to_start_font = pygame.font.Font("pixelletters.ttf", 40)

    game_over_text = game_over_font.render('Game Over', True, WHITE)
    coins_text = coins_font.render(f'You earned {coins_collected} coins', True, WHITE)
    try_again_text = try_again_font.render('Try Again', True, BLACK)
    back_to_start_text = back_to_start_font.render('Back to Start', True, BLACK)

    # Button dimensions
    button_x = WIDTH // 2 - 100
    button_y = HEIGHT // 2 + 50
    button_width = 200
    button_height = 50

    back_button_x = WIDTH // 2 - 100
    back_button_y = HEIGHT // 2 + 120


    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (button_x <= mouse_x <= button_x + button_width and
                        button_y <= mouse_y <= button_y + button_height):
                    waiting_for_input = False
                if (back_button_x <= mouse_x <= back_button_x + button_width and
                        back_button_y <= mouse_y <= back_button_y + button_height):
                    # Reset game state as needed
                    # (e.g., reset player position, health, coins, etc.)
                    start_screen(screen)
                    waiting_for_input = False


        screen.fill(BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(coins_text, (WIDTH // 2 - coins_text.get_width() // 2, HEIGHT // 2 - 30))
        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
        screen.blit(try_again_text, (button_x + 10, button_y))
        pygame.draw.rect(screen, WHITE, (back_button_x, back_button_y, button_width, button_height))
        screen.blit(back_to_start_text, (back_button_x + 10, back_button_y))
        pygame.display.flip()
        clock.tick(30)
def upgrade_window(screen, player_coins):
    upgrade_font = pygame.font.Font("pixelletters.ttf", 36)

    upgrade_text = upgrade_font.render('Choose an Upgrade', True, WHITE)
    button_texts = ['Bullet spread', 'Health boost', 'Attack damage']

    buttons = []
    for i, text in enumerate(button_texts):
        button_x = WIDTH // 2 - 100
        button_y = HEIGHT // 2 - 50 + i * 60
        button_width = 200
        button_height = 40
        buttons.append((button_x, button_y, button_width, button_height, text))

    upgrade_selected = False
    while not upgrade_selected:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for button in buttons:
                    bx, by, bw, bh, _ = button
                    if bx <= mouse_x <= bx + bw and by <= mouse_y <= by + bh:
                        upgrade_selected = True
                        break

        screen.fill(BLACK)
        screen.blit(upgrade_text, (WIDTH // 2 - upgrade_text.get_width() // 2, HEIGHT // 2 - 150))
        for bx, by, bw, bh, text in buttons:
            pygame.draw.rect(screen, WHITE, (bx, by, bw, bh))
            button_text = upgrade_font.render(text, True, BLACK)
            screen.blit(button_text, (bx + 10, by))
        pygame.display.flip()
        clock.tick(30)

def move_coins_towards_player(coins, player, move_speed=4, attraction_radius=150):
    for coin in coins:
        dx, dy = player.x - coin.x, player.y - coin.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < attraction_radius:
            # Normalize the direction
            dx, dy = dx / distance, dy / distance
            # Move the coin towards the player
            coin.x += dx * move_speed
            coin.y += dy * move_speed

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.color = WHITE
        self.speed = 5
        self.health = 3
        self.dash_speed = 40  # Speed of dash
        self.dash_cooldown = 500  # Cooldown in milliseconds
        self.last_dash = 0  # Time since last dash

    def draw(self, screen):
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        pygame.draw.circle(screen, self.color, (center_x, center_y), self.size // 2)

    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Constrain the new position to be within the screen boundaries
        # Adjust for the size of the player to prevent partial off-screen movement
        half_size = self.size // 2
        new_x = max(half_size, min(WIDTH - half_size, new_x))
        new_y = max(half_size, min(HEIGHT - half_size, new_y))

        # Update player's position
        self.x = new_x
        self.y = new_y

    def collides_with(self, other):
        distance_x = (self.x + self.size // 2) - (other.x + other.size // 2)
        distance_y = (self.y + self.size // 2) - (other.y + other.size // 2)
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

        # Check if the distance is less than the sum of the radii
        return distance < (self.size // 2 + other.size // 2)

    def dash(self, current_time):
        if current_time - self.last_dash > self.dash_cooldown:
            self.last_dash = current_time
            # Dash mechanics (e.g., increase speed or teleport forward)
            # Example: Increase speed for a single frame
            self.speed += self.dash_speed

class Enemy:
    def __init__(self):
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

    def take_damage(self, coins):
        self.health -= 1
        if self.health <= 0:
            coins.append(Coin(self.x, self.y))
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

    def take_damage(self, coins):
        self.health -= 1
        if self.health <= 0:
            for _ in range(self.vertices):
                coins.append(Coin(self.x, self.y))
            return True
        return False


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

    def take_damage(self, coins):
        self.health -= 1
        if self.health <= 0:
            for _ in range(self.vertices):
                coins.append(Coin(self.x, self.y))
            return True
        return False

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

    def take_damage(self, coins):
        self.health -= 1
        if self.health <= 0:
            for _ in range(self.vertices):
                coins.append(Coin(self.x, self.y))
            return True
        return False

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

    def take_damage(self, coins):
        self.health -= 1
        if self.health <= 0:
            for _ in range(self.vertices):
                coins.append(Coin(self.x, self.y))
            return True
        return False


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

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.color = (255, 215, 0)  # Gold color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

class Tiles(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        tile_size = 32
        rows = HEIGHT // tile_size + 1
        cols = WIDTH // tile_size + 1
        self.tiles = []
        for i in range(cols):
            for k in range(rows):
                tile_chords = (i*tile_size, k*tile_size)
                tile_rect = pygame.Rect(tile_chords[0], tile_chords[1], tile_size, tile_size)
                offset = random.randint(-20, 20)
                depth = (HEIGHT - tile_chords[1]) / HEIGHT * 255 + offset
                depth = max(0, min(100-offset, depth))

                tile_color = (depth, depth, depth)
                tile = {"rect": tile_rect, "color": tile_color}
                self.tiles.append(tile)


player = Player(WIDTH // 2, HEIGHT // 2)
enemies = []
projectiles = []
player_coins = 0
coins = []
tiles = Tiles()

start_screen(screen)

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Shoot a projectile
            mx, my = pygame.mouse.get_pos()
            dx, dy = mx - player.x, my - player.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance != 0:
                dx, dy = dx / distance, dy / distance
                projectiles.append(Projectile(player.x, player.y, dx, dy))
    for tile_data in tiles.tiles:
        pygame.draw.rect(screen, tile_data["color"], tile_data["rect"])
    if pygame.time.get_ticks() - enemy_spawn_time > spawn_interval:
        enemy_spawn_time = pygame.time.get_ticks()  # Reset spawn timer

        # Spawn enemies based on spawn_count
        for _ in range(spawn_count):
            enemy_types = [TriangleEnemy, SquareEnemy, PentagonEnemy, HexagonEnemy]
            chosen_enemy_type = random.choice(enemy_types)
            enemies.append(chosen_enemy_type())

        # Increase the spawn count following the power of 1.5 rule
        spawn_count = int(spawn_count ** 1.5)

    current_time = pygame.time.get_ticks()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.dash(current_time)
    if keys[pygame.K_a]:
        player.move(-1, 0)
    if keys[pygame.K_d]:
        player.move(1, 0)
    if keys[pygame.K_w]:
        player.move(0, -1)
    if keys[pygame.K_s]:
        player.move(0, 1)


    player.speed = 5
    # Update and draw player
    player.draw(screen)

    move_coins_towards_player(coins, player)
    for coin in coins[:]:
        coin.draw(screen)
        if player.collides_with(coin):
            coins.remove(coin)
            player_coins += 1

    if player_coins >= 20:
        player_coins -= 20  # Deduct coins after upgrading
        upgrade_window(screen, player_coins)
        # Display coin count
    coin_text = font.render(f"Coins: {player_coins}", True, WHITE)
    screen.blit(coin_text, (10, 10))
    # Display player's health
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    screen.blit(health_text, (10, 40))  # Position below the coin count


    # Update and draw enemies
    for projectile in projectiles[:]:
        projectile.move()
        projectile.draw(screen)
        if projectile.x < 0 or projectile.x > WIDTH or projectile.y < 0 or projectile.y > HEIGHT:
            projectiles.remove(projectile)

        # Update and draw enemies
    for enemy in enemies[:]:
        enemy.move_towards_player(player, enemies)
        enemy.draw(screen)

        # Check collision with projectiles
        for projectile in projectiles[:]:
            if projectile.collides_with(enemy):
                projectiles.remove(projectile)
                if enemy.take_damage(coins):  # Pass coins list to take_damage
                    enemies.remove(enemy)
                    break
    for enemy in enemies:
        if player.collides_with(enemy):
            player.health -= 1  # Reduce player health
            # Optionally, you can remove the enemy or move it away
            # enemies.remove(enemy)  # Remove the enemy
            # or reposition the enemy
            enemy.x = random.randint(0, WIDTH)
            enemy.y = random.randint(0, HEIGHT)

            if player.health <= 0:
                print("Player has died!")
                running = False
                game_over_screen(screen, player_coins)  # Display game over screen
                # Reset game state for a new game
                player = Player(WIDTH // 2, HEIGHT // 2)
                enemies=[]
                projectiles = []
                player_coins = 0
                coins = []
                enemy_spawn_time = 0
                spawn_count = 2
                running = True
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

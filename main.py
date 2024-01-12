import pygame
import random
import math
# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1680, 920
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle of geometry")
enemy_spawn_time = 2  # Timer for enemy spawning
spawn_interval = 5000  # 10 seconds in milliseconds
spawn_count = 3  # Initial number of enemies to spawn
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
def upgrade_window(screen, experience):
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
                for index, button in enumerate(buttons):
                    bx, by, bw, bh, _ = button
                    if bx <= mouse_x <= bx + bw and by <= mouse_y <= by + bh:
                        # Handle each button click separately
                        if index == 0:
                            # Handle 'Bullet spread' button
                            print("Bullet size selected")
                            projectile.size += 1
                        elif index == 1:
                            # Handle 'Health boost' button
                            print("Health boost selected")
                            player.health += 1
                        elif index == 2:
                            # Handle 'Attack damage' button
                            print("Attack damage selected")
                            player.attackdmg += 1

                        upgrade_selected = True
                        break
        screen.fill(BLACK)  # Clear the screen with a background color

        # Draw the header text
        screen.blit(upgrade_text, (WIDTH // 2 - upgrade_text.get_width() // 2, HEIGHT // 2 - 150))

        for bx, by, bw, bh, text in buttons:
            pygame.draw.rect(screen, WHITE, (bx, by, bw, bh))
            button_text = upgrade_font.render(text, True, BLACK)
            screen.blit(button_text, (bx + 10, by))

        pygame.display.flip()  # Update the screen
        clock.tick(30)  # Control the frame rate

def move_items_towards_player(items, player, move_speed=4, attraction_radius=150):
    for item in items:
        dx, dy = player.x - item.x, player.y - item.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < attraction_radius:
            # Normalize the direction
            dx, dy = dx / distance, dy / distance
            # Move the item towards the player
            item.x += dx * move_speed
            item.y += dy * move_speed

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.color = (255, 255, 255)  # Assuming white color
        self.speed = 5
        self.health = 3
        self.dash_speed = 15  # Adjusted for multi-frame dash
        self.dash_duration = 10  # Dash duration in frames
        self.dash_cooldown = 500  # Cooldown in milliseconds
        self.last_dash = 0  # Time since last dash
        self.is_dashing = False
        self.dash_trail = []  # Store positions for the dash trail
        self.dash_frames_remaining = 0
        self.speed_reduction_per_frame = 0
        self.attackdmg = 1

    def draw(self, screen):
        # Draw the dash trail
        for pos, alpha in self.dash_trail:
            trail_color = (*self.color[:3], alpha)
            trail_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, trail_color, (self.size // 2, self.size // 2), self.size // 2.3)
            screen.blit(trail_surface, pos)

        # Draw the player
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

    def update(self, current_time):
        if self.dash_frames_remaining > 0:
            # Reduce the speed
            self.speed -= self.speed_reduction_per_frame

            # Ensure the speed does not go below normal
            self.speed = max(self.speed, 5)

            # Decrement the counter
            self.dash_frames_remaining -= 1

            # Add current position to the dash trail
            self.dash_trail.append(((self.x, self.y), 255))
        else:
            # If dashing is over, start fading the trail
            self.fade_dash_trail()

        if current_time - self.last_dash > self.dash_cooldown and self.is_dashing:
            self.is_dashing = False
            self.speed = 5  # Resetting the speed to normal after dash ends

    def dash(self, current_time):
        if current_time - self.last_dash > self.dash_cooldown and not self.is_dashing:
            self.last_dash = current_time
            self.is_dashing = True  # Start dashing
            # Reset dash trail for new dash
            self.dash_trail.clear()
            # Add initial position to the dash trail with full opacity
            self.dash_trail.append(((self.x, self.y), 255))
            # Increase speed for the dash
            self.speed += self.dash_speed
            # Schedule to reset the speed and start fading the trail
            self.schedule_speed_reset()

    def schedule_speed_reset(self):
        # Define the duration of the dash effect in terms of frames or time
        dash_duration_frames = 8  # for example, 1 second at 60 FPS

        # Calculate the amount of speed reduction per frame
        speed_reduction_per_frame = (self.speed - 5) / dash_duration_frames

        # Store these values for use in the update method
        self.dash_frames_remaining = dash_duration_frames
        self.speed_reduction_per_frame = speed_reduction_per_frame

    def fade_dash_trail(self):
        # Fade out the dash trail
        new_trail = []
        alpha_decrement = max(1, 255 // self.dash_duration)  # Ensure at least 1 alpha decrement
        for pos, alpha in self.dash_trail:
            new_alpha = alpha - alpha_decrement
            if new_alpha > 0:
                new_trail.append((pos, new_alpha))
        self.dash_trail = new_trail

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

    def take_damage(self, coins):
        self.health -= player.attackdmg
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
player_experience = 0
experience_points = []
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
        if spawn_count < 20:
            spawn_count = int(spawn_count ** 1.3)

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

    # Update and draw player
    player.draw(screen)
    player.update(current_time)

    move_items_towards_player(coins + experience_points, player)

    # Handle coins
    for coin in coins[:]:
        coin.draw(screen)
        if player.collides_with(coin):
            coins.remove(coin)
            player_coins += 1

    # Handle experience points
    for exp in experience_points[:]:
        exp.draw(screen)
        if player.collides_with(exp):
            experience_points.remove(exp)
            # Handle experience gain here, for example:
            player_experience += 1

    if player_experience >= 20:
        player_experience -= 20  # Deduct exp after upgrading
        upgrade_window(screen, player_experience)
        # Display coin count
    coin_text = font.render(f"Coins: {player_coins}", True, WHITE)
    screen.blit(coin_text, (10, 10))
    exp_text = font.render(f"Experience: {player_experience}", True, WHITE)
    screen.blit(exp_text, (10, 40))
    # Display player's health
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    screen.blit(health_text, (10, 70))  # Position below the coin count


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
                player_experience
                experience_points = []
                enemy_spawn_time = 0
                spawn_count = 2
                running = True
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

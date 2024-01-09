import math
import random
from settings import WIDTH, HEIGHT
import math
import pygame

def generate_safe_spawn(player, min_distance=100):
    while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        distance = math.sqrt((player.x - x) ** 2 + (player.y - y) ** 2)
        if distance >= min_distance:
            return x, y

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

def create_projectile_from_player(player):
    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - player.x, my - player.y
    distance = math.sqrt(dx ** 2 + dy ** 2)
    if distance != 0:
        dx, dy = dx / distance, dy / distance
    return Projectile(player.x, player.y, dx, dy)

def spawn_enemies(enemies, spawn_count, enemy_spawn_time, spawn_interval, current_time, EnemyClasses):
    if current_time - enemy_spawn_time > spawn_interval:
        for _ in range(spawn_count):
            chosen_enemy_type = random.choice(EnemyClasses)
            enemies.append(chosen_enemy_type())
        return current_time, int(spawn_count ** 1.5)  # Returning updated values
    return enemy_spawn_time, spawn_count  # Returning original values if no spawning occurred

# Function to handle player input
def handle_player_input(player, keys, current_time):
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


# Function to handle collectible items like coins and experience points
def handle_collectibles(coins, experience_points, player):
    collected_coins = 0
    collected_experience = 0

    # Check for collision with coins
    for coin in coins[:]:  # Use a slice copy to iterate over a static list copy
        if check_collision(player, coin):
            coins.remove(coin)
            collected_coins += 1  # Increment the coin count

    # Check for collision with experience points
    for exp in experience_points[:]:  # Use a slice copy to iterate over a static list copy
        if check_collision(player, exp):
            experience_points.remove(exp)
            collected_experience += 1  # Increment the experience count

    return collected_coins, collected_experience

def check_collision(entity1, entity2):
    # Simple box collision detection
    return (entity1.x < entity2.x + entity2.size and
            entity1.x + entity1.size > entity2.x and
            entity1.y < entity2.y + entity2.size and
            entity1.y + entity1.size > entity2.y)


# Function to display the UI elements like score, health, etc.
def display_ui(screen, font, coins, experience, health):
    coin_text = font.render(f"Coins: {coins}", True, (255, 255, 255))
    screen.blit(coin_text, (10, 10))
    exp_text = font.render(f"Experience: {experience}", True, (255, 255, 255))
    screen.blit(exp_text, (10, 40))
    health_text = font.render(f"Health: {health}", True, (255, 255, 255))
    screen.blit(health_text, (10, 70))

def handle_projectile_enemy_collisions(projectiles, enemies, on_hit_callback):
    for projectile in projectiles[:]:  # Use a slice copy to iterate over a static list copy
        for enemy in enemies[:]:  # Use a slice copy to iterate over a static list copy
            if check_collision(projectile, enemy):
                projectiles.remove(projectile)
                if on_hit_callback:  # on_hit_callback is a function to execute when a hit occurs
                    on_hit_callback(enemy)

# Function to update the positions and draw the projectiles
def update_projectiles(projectiles, screen):
    for projectile in projectiles:
        projectile.move()
        projectile.draw(screen)
        # If projectiles go off-screen, remove them
        # ...

# Function to update the positions and draw the enemies
def update_enemies(enemies, projectiles, player, screen):
    for enemy in enemies[:]:  # Use slice copy to iterate over a static list copy
        enemy.move_towards_player(player, enemies)
        enemy.draw(screen)
        # Check collision with projectiles
        for projectile in projectiles[:]:
            if check_collision(projectile, enemy):
                projectiles.remove(projectile)
                if enemy.take_damage():
                    enemies.remove(enemy)
                    break

# Function to reset the game state after the player dies or a new game starts
def reset_game_state(player, enemies, projectiles, coins, experience_points):
    # Assuming the Player class has a method to reset its state
    player.reset()

    # Clear all lists
    enemies.clear()
    projectiles.clear()
    coins.clear()
    experience_points.clear()

    # Re-initialize any other game state variables
    # ...
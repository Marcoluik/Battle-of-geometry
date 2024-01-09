import pygame
import random
from settings import WIDTH, HEIGHT, BLACK, WHITE, FPS
from player import Player
from enemies import TriangleEnemy, SquareEnemy, PentagonEnemy, HexagonEnemy
from projectiles import Projectile
from items import Coin, Experience
from tiles import Tiles
from ui import start_screen, game_over_screen, upgrade_window
import utilities

# Initialize Pygame and set up the display
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle of Geometry")

# Initialize game variables
enemy_spawn_time = pygame.time.get_ticks()
spawn_interval = 3000  # Interval for enemy spawning in milliseconds
spawn_count = 2  # Initial number of enemies to spawn

# Load font
font_path = "pixelletters.ttf"  # Update the path if the font is in a different directory
try:
    font = pygame.font.Font(font_path, 36)
except FileNotFoundError:
    print(f"Unable to load font from {font_path}. Falling back to default font.")
    font = pygame.font.SysFont(None, 36)

# Create game objects
player = Player(WIDTH // 2, HEIGHT // 2)
enemies = []
projectiles = []
coins = []
experience_points = []
tiles = Tiles()

# Game clock
clock = pygame.time.Clock()

# Start the game with the start screen
start_screen(screen)

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            projectiles.append(utilities.create_projectile_from_player(player))

    EnemyClasses = (TriangleEnemy, SquareEnemy, PentagonEnemy, HexagonEnemy)
    current_time = pygame.time.get_ticks()
    enemy_spawn_time, spawn_count = utilities.spawn_enemies(
        enemies,
        spawn_count,
        enemy_spawn_time,
        spawn_interval,
        current_time,
        EnemyClasses
    )
    keys = pygame.key.get_pressed()
    utilities.handle_player_input(player, keys, current_time)
    player.draw(screen)
    utilities.move_items_towards_player(coins + experience_points, player)
    utilities.handle_collectibles(coins, experience_points, player)

    # Check for player's experience to upgrade
    if player.experience >= 20:
        player.experience -= 20
        upgrade_window(screen, player.experience)

    collected_coins, collected_experience = utilities.handle_collectibles(coins, experience_points, player)

    # Add the collected experience to the player's total
    player.experience += collected_experience

    # Display UI elements
    utilities.display_ui(screen, font, coins, experience_points, player.health)

    # Update and draw projectiles and enemies
    utilities.update_projectiles(projectiles, screen, WIDTH, HEIGHT)
    utilities.update_enemies(enemies, projectiles, player, screen, coins)

    # Check player health for game over
    if player.health <= 0:
        game_over_screen(screen, coins)
        utilities.reset_game_state(player, enemies, projectiles, coins, experience_points)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

import pygame
import random
import math
import screens
import player_file
import xp_coins
import enemy_file
import projectile_file
import tile_file
from upgrade_file import upgrade_window
from magnet_file import move_items_towards_player
from settings import WHITE, HEIGHT, WIDTH, BLACK, FPS
# Initialize Pygame
pygame.init()



# Set up the display
pygame.display.set_caption("Battle of geometry")
enemy_spawn_time = 2  # Timer til enemies spawner i starten af spillet
spawn_interval = 5000
spawn_count = 2  # Initial number of enemies to spawn
# Define colors


# Game clock
clock = pygame.time.Clock()

font = pygame.font.Font("pixelletters.ttf",36)
# Game loop flag
running = True


player = player_file.Player(WIDTH // 2, HEIGHT // 2)
enemies = []
projectiles = []
player_coins = 0
coins = []
player_experience = 0
experience_points = []
tiles = tile_file.Tiles()
explosions = []
projectile_effects = []
frozen = False
frozen_timer = 0

screen_manager = screens.screenz()
screen = screen_manager.screen
screen_manager.start_screen(screen)

while running:
    screen.fill(BLACK)
    pygame.mouse.set_cursor(pygame.cursors.broken_x)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not frozen:
            # Shoot a projectile
            print(pygame.time.get_ticks(), frozen)
            mx, my = pygame.mouse.get_pos()
            dx, dy = mx - player.x, my - player.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance != 0:
                dx, dy = dx / distance, dy / distance
                projectiles.append(projectile_file.Projectile(player.x, player.y, dx, dy))
    for tile_data in tiles.current_moon_tiles + tiles.next_moon_tiles:
        pygame.draw.rect(screen, tile_data["color"], tile_data["rect"])
    if pygame.time.get_ticks() - enemy_spawn_time > spawn_interval:
        enemy_spawn_time = pygame.time.get_ticks()  # Reset spawn timer

        # Spawn enemies based on spawn_count
        for _ in range(spawn_count):

            enemy_types = [enemy_file.TriangleEnemy, enemy_file.SquareEnemy, enemy_file.PentagonEnemy] #
            chosen_enemy_type = random.choice(enemy_types)
            enemies.append(chosen_enemy_type())

        # Increase the spawn count following the power of 1.5 rule
        if spawn_count < 8:
            spawn_count = int(spawn_count ** 1.3)

    current_time = pygame.time.get_ticks()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and not frozen:
        player.dash(current_time)
    if keys[pygame.K_a] and not frozen:
        player.move(-1, 0)
    if keys[pygame.K_d] and not frozen:
        player.move(1, 0)
    if keys[pygame.K_w] and not frozen:
        player.move(0, -1)
    if keys[pygame.K_s] and not frozen:
        player.move(0, 1)

    # Update and draw player
    if not frozen:
        player.update(current_time)
    player.draw(screen)
    # Update game state
    tiles.update()


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
        frozen = True
        upgrade = upgrade_window(screen, player_experience)
        frozen_timer = pygame.time.get_ticks() + 700
        print(frozen, frozen_timer)
        if upgrade == 1:
            projectile.size += 1
        elif upgrade == 2:
            player.health += 1
        elif upgrade == 3:
            player.attackdmg += 1
        # Display coin count
    coin_text = font.render(f"Coins: {player_coins}", True, WHITE)
    screen.blit(coin_text, (10, 10))
    exp_text = font.render(f"Experience: {player_experience}", True, WHITE)
    screen.blit(exp_text, (10, 40))
    # Display player's health
    health_text = font.render(f"Health: {player.health}", True, WHITE)
    screen.blit(health_text, (10, 70))  # Position below the coin count

    if pygame.time.get_ticks() > frozen_timer and frozen:
        frozen = False
        print(pygame.time.get_ticks())

    # Update and draw projectiles
    for projectile in projectiles[:]:
        if not frozen:
            projectile.move()
            if projectile.x < 0 or projectile.x > WIDTH or projectile.y < 0 or projectile.y > HEIGHT:
                projectiles.remove(projectile)
        projectile.draw(screen)




        # Update and draw enemies
    for enemy in enemies[:]:
        # Check collision with projectiles
        if not frozen:
            enemy.move_towards_player(player, enemies)
            for projectile in projectiles[:]:
                if projectile.collides_with(enemy):
                    projectiles.remove(projectile)
                    projectile_effects.append(projectile_file.ProjectileEffect(projectile.x, projectile.y))
                    if enemy.take_damage(coins, experience_points, screen):  # Pass coins list to take_damage
                        explosion_effect = enemy_file.ParticleAnimation('explosion.png', 1, 8, screen, enemy.x-32, enemy.y-32, 3)
                        explosions.append(explosion_effect)
                        enemies.remove(enemy)
                        break
        enemy.draw(screen)

    for projectile_effect in projectile_effects:
        projectile_effect.draw(screen)
        if projectile_effect.frame > 10:
            projectile_effects.remove(projectile_effect)

    for explosion_effect in explosions[:]:
        explosion_effect.update()
        explosion_effect.draw()
        if explosion_effect.current_frame == len(explosion_effect.images) - 1:
            explosions.remove(explosion_effect)

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
                screen_manager.game_over_screen(screen, player_coins)  # Display game_over_screen
                # Reset game state for a new game
                player = player_file.Player(WIDTH // 2, HEIGHT // 2)
                enemies=[]
                projectiles = []
                player_coins = 0
                coins = []
                player_experience = 0
                experience_points = []
                enemy_spawn_time = pygame.time.get_ticks()
                spawn_count = 2
                running = True
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

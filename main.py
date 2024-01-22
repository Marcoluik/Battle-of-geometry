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
enemy_spawn_time = 2  # Timer for enemy spawning
spawn_interval = 5000  # 10 seconds in milliseconds
spawn_count = 2  # Initial number of enemies to spawn
next_lvl = 20
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

screen_manager = screens.screenz()
screen = screen_manager.screen
screen_manager.start_screen(screen)

while running:
    screen.fill(BLACK)
    current_time = pygame.time.get_ticks()
    dt = clock.tick()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Shoot a projectile
            mx, my = pygame.mouse.get_pos()
            dx, dy = mx - player.x, my - player.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance != 0 and current_time - player.last_shot > player.shoot_cd:
                dx, dy = dx / distance, dy / distance
                projectiles.append(projectile_file.Projectile(player.x, player.y, dx, dy))
                player.last_shot = current_time  # Update the time when the player last shot
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


        # Display coin count


    pygame.draw.rect(screen, "black", (0, 0, WIDTH, 30))
    pygame.draw.rect(screen, "green", (0, 0, WIDTH * (player_experience/next_lvl), 30))
    hearthicon = pygame.image.load("Images/Hearth.png")
    hearthicon = pygame.transform.scale(hearthicon, (50, 50))
    for i in range(player.health):
        screen.blit(hearthicon, (20+i*40, 40))
    moneyicon = pygame.image.load("Images/Money.png")
    moneyicon = pygame.transform.scale(moneyicon, (50, 50))
    screen.blit(moneyicon, (20, 90))
    coin_text = font.render(f"{player_coins}", True, WHITE)
    screen.blit(coin_text, (70, 100))




    # Update and draw enemies
    for projectile in projectiles[:]:
        projectile.move()
        projectile.draw(screen)
        if projectile.x < 0 or projectile.x > WIDTH or projectile.y < 0 or projectile.y > HEIGHT:
            projectiles.remove(projectile)

    if player_experience >= next_lvl:
        player_experience -= next_lvl  # Deduct exp after upgrading
        next_lvl *= 2
        upgrade = upgrade_window(screen, player_experience)
        if upgrade == 1:
            player.speed += 2
        elif upgrade == 2:
            player.health += 1
        elif upgrade == 3:
            player.attackdmg += 1
        elif upgrade == 4:
            player.dash_duration += 3
        elif upgrade == 5:
            player.dash_cooldown -= 500
        elif upgrade == 6:
            player.shoot_cd -= 150

        # Update and draw enemies
    for enemy in enemies[:]:
        enemy.move_towards_player(player, enemies)
        enemy.draw(screen)

        # Check collision with projectiles
        for projectile in projectiles[:]:
            if projectile.collides_with(enemy):
                projectiles.remove(projectile)
                if enemy.take_damage(coins, experience_points):  # Pass coins list to take_damage
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
                screen_manager.game_over_screen(screen, player_coins)  # Display game over screen
                # Reset game state for a new game
                player = player_file.Player(WIDTH // 2, HEIGHT // 2)
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

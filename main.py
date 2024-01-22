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


#sound effects
shooting_sfx = pygame.mixer.Sound("laserpew.ogg")
game_over_sfx = pygame.mixer.Sound("gameoversound.ogg")
damage_taken_sfx = pygame.mixer.Sound('spawn.ogg')
enemy_death_sfx = pygame.mixer.Sound('explosion01.ogg')
coin_pickup_sfx = pygame.mixer.Sound('1_Coins.ogg')


#sound effects adjusting volumes
shooting_sfx.set_volume(0.5)
game_over_sfx.set_volume(0.8)
damage_taken_sfx.set_volume(0.1)
enemy_death_sfx.set_volume(0.05)
coin_pickup_sfx.set_volume(0.2)

pygame.mixer.music.load('Space-Sprinkles.ogg')
pygame.mixer.music.set_volume(0.06)
pygame.mixer.music.play(2, 00.00, 50)



player = player_file.Player(WIDTH // 2, HEIGHT // 2)
enemies = []
projectiles = []
player_coins = 0
coins = []
player_experience = 0
experience_points = []
tiles = tile_file.Tiles()
explosions = []

screen_manager = screens.screenz()
screen = screen_manager.screen
screen_manager.start_screen(screen)

while running:
    screen.fill(BLACK)
    pygame.mouse.set_cursor(pygame.cursors.broken_x)
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
                shooting_sfx.play()
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
            coin_pickup_sfx.play()
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
                if enemy.take_damage(coins, experience_points, screen):  # Pass coins list to take_damage
                    explosion_effect = enemy_file.ParticleAnimation('explosion.png', 1, 8, screen, enemy.x-32, enemy.y-32, 3)
                    explosions.append(explosion_effect)
                    enemies.remove(enemy)
                    enemy_death_sfx.play()
                    break

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

            if player.health > 0:
                damage_taken_sfx.play()

            if player.health <= 0:
                print("Player has died!")
                game_over_sfx.play()
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

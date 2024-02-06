import pygame
import random
import math
import events
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
spawn_interval = 4000
spawn_count = 2  # Initial number of enemies to spawn
next_lvl = 20
# Define colors





with open("upgrades.txt", "r") as fil:
    data = fil.readlines()

total_coins = int(data[0])
asteroid_bought = int(data[1])
lives_bought = int(data[2])


# Game clock
clock = pygame.time.Clock()

font = pygame.font.Font("pixelletters.ttf",36)
# Game loop flag
running = True


#sound effects
shooting_sfx = pygame.mixer.Sound("sounds/laserpew.ogg")
game_over_sfx = pygame.mixer.Sound("sounds/gameoversound.ogg")
damage_taken_sfx = pygame.mixer.Sound('sounds/spawn.ogg')
enemy_death_sfx = pygame.mixer.Sound('sounds/explosion01.ogg')
coin_pickup_sfx = pygame.mixer.Sound('sounds/1_Coins.ogg')


#sound effects adjusting volumes
shooting_sfx.set_volume(0.5)
game_over_sfx.set_volume(0.8)
damage_taken_sfx.set_volume(0.1)
enemy_death_sfx.set_volume(0.05)
coin_pickup_sfx.set_volume(0.2)

pygame.mixer.music.load('sounds/Space-Sprinkles.ogg')
pygame.mixer.music.set_volume(0.06)
pygame.mixer.music.play(2, 00.00, 50)


meteors = []
for _ in range(15):
    meteor_event = events.MeteorEvent(WIDTH - random.randint(10, 500), -random.randint(50, 600))
    meteors.append(meteor_event)

enemies = []
projectiles = []
player_coins = 0
coins = []
player_experience = 0
experience_points = []
tiles = tile_file.Tiles()
explosions = []
game_time = 0
projectile_effects = []
frozen = False
frozen_timer = 0

screen_manager = screens.screenz()
screen = screen_manager.screen
screen_manager.start_screen(screen)

player = player_file.Player(WIDTH // 2, HEIGHT // 2)
circle_upgrade = player_file.CirclingUpgrade(WIDTH//2, HEIGHT//2)



last_reset = 0
add_to_spawn_count = spawn_count
while running:
    screen.fill(BLACK)
    pygame.mouse.set_cursor(pygame.cursors.broken_x)
    current_time = pygame.time.get_ticks() - last_reset
    dt = clock.tick()
    game_time = current_time // 1000  # integer division
    gt_minutes = game_time // 60
    gt_seconds = game_time % 60



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #elif event.type == pygame.MOUSEBUTTONDOWN and not frozen:
        elif event.type and not frozen:
            # Shoot a projectile
            pass
            """mx, my = pygame.mouse.get_pos()

            mx, my = pygame.mouse.get_pos()
            dx, dy = mx - player.x, my - player.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance != 0 and current_time - player.last_shot > player.shoot_cd:
                dx, dy = dx / distance, dy / distance
                shooting_sfx.play()
                projectiles.append(projectile_file.Projectile(player.x, player.y, dx, dy))
                player.last_shot = current_time  # Update the time when the player last shot"""
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
        if spawn_count < 5 and spawn_interval > 2500:
            spawn_interval -= 10
            add_to_spawn_count *= 1.05
            spawn_count = math.floor(add_to_spawn_count)

        if spawn_count >= 5  and spawn_count < 8 and spawn_interval > 2500:
            spawn_interval -= 15
            add_to_spawn_count *= 1.025
            spawn_count = math.floor(add_to_spawn_count)

        if spawn_count >= 8 and spawn_interval > 2500:
            spawn_interval -= 25

    if not frozen:
        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - player.x, my - player.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0 and current_time - player.last_shot > player.shoot_cd:
            dx, dy = dx / distance, dy / distance
            shooting_sfx.play()
            projectiles.append(projectile_file.Laser_Projectile(player.x, player.y, dx, dy))
            player.last_shot = current_time  # Update the time when the player last shot

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
    if gt_minutes < 10 and gt_seconds < 10:
        time_text = font.render(f"0{gt_minutes} : 0{gt_seconds}", True, WHITE)
        screen.blit(time_text, (WIDTH // 2-30, 70))
    elif gt_minutes < 10:
        time_text = font.render(f"0{gt_minutes} : {gt_seconds}", True, WHITE)
        screen.blit(time_text, (WIDTH // 2-30, 70))
    else:
        time_text = font.render(f"{gt_minutes} : {gt_seconds}", True, WHITE)
        screen.blit(time_text, (WIDTH // 2-30, 70))
    if gt_minutes == 0 and gt_seconds < 10:
        instructions_text = font.render("WASD to move. Space to dash. Survive, Destroy and Upgrade!", True, WHITE)
        screen.blit(instructions_text, (50, HEIGHT-100))

    if screen_manager.asteroid_bought:
        circle_upgrade.draw(screen)
        circle_upgrade.update(current_time, player.x, player.y)


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


    pygame.draw.rect(screen, "black", (0, 0, WIDTH, 40))
    pygame.draw.rect(screen, "green", (0, 7, WIDTH * (player_experience/next_lvl), 25))
    hearthicon = pygame.image.load("Images/Hearth.png")
    hearthicon = pygame.transform.scale(hearthicon, (50, 50))
    for i in range(player.health):
        screen.blit(hearthicon, (20+i*40, 40))
    moneyicon = pygame.image.load("Images/Money.png")
    moneyicon = pygame.transform.scale(moneyicon, (50, 50))
    screen.blit(moneyicon, (20, 90))
    coin_text = font.render(f"{player_coins}", True, WHITE)
    screen.blit(coin_text, (70, 100))



    if pygame.time.get_ticks() > frozen_timer and frozen:
        frozen = False

    # Update and draw projectiles
    for projectile in projectiles[:]:
        if not frozen:
            projectile.move()
            if projectile.x < 0 or projectile.x > WIDTH or projectile.y < 0 or projectile.y > HEIGHT:
                projectiles.remove(projectile)
            if projectile.size == 4 and player.collides_with(projectile):
                projectiles.remove(projectile)
                player.health -= 1
                if player.health > 0:
                    damage_taken_sfx.play()
                if player.health <= 0:
                    print("Player has died!")
                    total_coins += player_coins
                    data[0] = f"{total_coins}\n"
                    with open("upgrades.txt", "w") as fil:
                        fil.writelines(data)


                    game_over_sfx.play()
                    running = False
                    screen_manager.game_over_screen(screen, player_coins)  # Display game_over_screen
                    # Reset game state for a new game
                    player = player_file.Player(WIDTH // 2, HEIGHT // 2)
                    enemies = []
                    projectiles = []
                    player_coins = 0
                    coins = []
                    player_experience = 0
                    experience_points = []
                    enemy_spawn_time = pygame.time.get_ticks()
                    spawn_count = 2
                    running = True

        projectile.draw(screen)




    if player_experience >= next_lvl:
        player_experience -= next_lvl  # Deduct exp after upgrading
        next_lvl *= 2
        frozen = True
        upgrade = upgrade_window(screen)
        frozen_timer = pygame.time.get_ticks() + 700
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
        # Check collision with projectiles
        if not frozen:
            enemy.move_towards_player(player, enemies)
            for projectile in projectiles[:]:
                if projectile.size != 4  and enemy in enemies and projectile.sprite_mask.overlap(enemy.sprite_mask, (projectile.x-enemy.x-32, projectile.y-enemy.y-32)):


                    projectiles.remove(projectile)
                    projectile_effects.append(projectile_file.ProjectileEffect(projectile.x, projectile.y))
                    if enemy.take_damage(coins, experience_points, screen):  # Pass coins list to take_damage
                        explosion_effect = enemy_file.ParticleAnimation('Images/explosion.png', 1, 8, screen, enemy.x - 32,
                                                                        enemy.y - 32, 3)
                        explosions.append(explosion_effect)
                        if enemy.vertices == 5:
                            dx, dy = player.x - enemy.x, player.y - enemy.y
                            distance = (dx ** 2 + dy ** 2) ** 0.5
                            dx, dy = dx/distance, dy/distance
                            projectiles.append(projectile_file.Rotating_Enemy_Projectile(enemy.x, enemy.y, dx, dy, enemy.vinkel))
                        enemies.remove(enemy)
                        enemy_death_sfx.play()
                        break

            if enemy in enemies and screen_manager.asteroid_bought and circle_upgrade.sprite_mask.overlap(enemy.sprite_mask,
                                                  (circle_upgrade.x - enemy.x - 32, circle_upgrade.y - enemy.y - 32)):
                if enemy.take_damage(coins, experience_points, screen):
                    explosion_effect = enemy_file.ParticleAnimation('Images/explosion.png', 1, 8, screen, enemy.x - 32,
                                                                    enemy.y - 32, 3)
                    explosions.append(explosion_effect)
                    enemies.remove(enemy)
                    enemy_death_sfx.play()
                    break

        enemy.draw(screen)

    for projectile_effect in projectile_effects:
        projectile_effect.draw(screen)
        if projectile_effect.frame > 10:
            projectile_effects.remove(projectile_effect)

    #METEOR EVENT
    if (current_time > 55000 and current_time < 60000) or (current_time > 115000 and current_time < 120000):
        meteor_warning_text = font.render("WARNING: METEOR SHOWER INCOMING", True, WHITE)
        screen.blit(meteor_warning_text, (WIDTH//2, HEIGHT//2 - 100))

    if (current_time > 70000 and current_time < 71000) or (current_time > 130000 and current_time < 131000):
        for meteor in meteors:
            meteor.reset(WIDTH - random.randint(10, 500), -random.randint(50, 600))


    if (current_time > 60000 and current_time < 70000) or (current_time > 120000 and current_time < 130000):
        for meteor in meteors:
            meteor.draw(screen)
            meteor.update()

            for enemy in enemies[:]:
                if enemy in enemies and meteor in meteors and meteor.sprite_mask.overlap(enemy.sprite_mask, (meteor.x-enemy.x-32, meteor.y-enemy.y-32)):
                    meteors.remove(meteor)
                    if enemy.take_damage(coins, experience_points, screen):  # Pass coins list to take_damage
                        explosion_effect = enemy_file.ParticleAnimation('Images/explosion.png', 1, 8, screen, enemy.x - 32, enemy.y - 32, 3)
                        explosions.append(explosion_effect)
                        enemies.remove(enemy)
                        enemy_death_sfx.play()
                        break

            if player.collides_with(meteor):
                player.health -= 1
                meteors.remove(meteor)

                if player.health > 0:
                    damage_taken_sfx.play()

                if player.health <= 0:
                    print("Player has died!")
                    total_coins += player_coins
                    data[0] = f"{total_coins}\n"
                    with open("upgrades.txt", "w") as fil:
                        fil.writelines(data)
                    game_over_sfx.play()
                    running = False
                    last_reset = pygame.time.get_ticks()
                    screen_manager.game_over_screen(screen, player_coins)  # Display game_over_screen
                    # Reset game state for a new game
                    player = player_file.Player(WIDTH // 2, HEIGHT // 2)
                    enemies = []
                    projectiles = []
                    player_coins = 0
                    coins = []
                    player_experience = 0
                    experience_points = []
                    next_lvl = 20
                    enemy_spawn_time = pygame.time.get_ticks()
                    spawn_interval = 4000
                    spawn_count = 2
                    add_to_spawn_count = spawn_count
                    running = True






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
                total_coins += player_coins
                data[0] = f"{total_coins}\n"
                with open("upgrades.txt", "w") as fil:
                    fil.writelines(data)
                game_over_sfx.play()
                running = False
                last_reset = pygame.time.get_ticks()
                screen_manager.game_over_screen(screen, player_coins)  # Display game_over_screen
                # Reset game state for a new game
                player = player_file.Player(WIDTH // 2, HEIGHT // 2)
                enemies=[]
                projectiles = []
                player_coins = 0
                coins = []
                player_experience = 0
                experience_points = []
                next_lvl = 20
                enemy_spawn_time = pygame.time.get_ticks()
                spawn_interval = 4000
                spawn_count = 2
                add_to_spawn_count = spawn_count
                running = True
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

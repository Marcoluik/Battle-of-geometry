import pygame
import random
import math
import screens
import player_file
import xp_coins
import enemy_file
import projectile_file
import tile_file
# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle of geometry")
enemy_spawn_time = 2  # Timer for enemy spawning
spawn_interval = 5000  # 10 seconds in milliseconds
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
            if distance < attraction_radius/2:
                #Normalize the direction
                dx, dy = dx / distance, dy / distance
                # Move the item towards the player
                item.x += dx * move_speed * 2
                item.y += dy * move_speed * 2

            else:
                # Normalize the direction
                dx, dy = dx / distance, dy / distance
                # Move the item towards the player
                item.x += dx * move_speed
                item.y += dy * move_speed


player = player_file.Player(WIDTH // 2, HEIGHT // 2)
enemies = []
projectiles = []
player_coins = 0
coins = []
player_experience = 0
experience_points = []
tiles = tile_file.Tiles()

screen_manager = screens.screenz()
screen_manager.start_screen(screen)

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
                projectiles.append(projectile_file.Projectile(player.x, player.y, dx, dy))
    for tile_data in tiles.tiles:
        pygame.draw.rect(screen, tile_data["color"], tile_data["rect"])
    if pygame.time.get_ticks() - enemy_spawn_time > spawn_interval:
        enemy_spawn_time = pygame.time.get_ticks()  # Reset spawn timer

        # Spawn enemies based on spawn_count
        for _ in range(spawn_count):
            enemy_types = [enemy_file.TriangleEnemy, enemy_file.SquareEnemy, enemy_file.PentagonEnemy, enemy_file.HexagonEnemy]
            chosen_enemy_type = random.choice(enemy_types)
            enemies.append(chosen_enemy_type())

        # Increase the spawn count following the power of 1.5 rule
        if spawn_count < 8:
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

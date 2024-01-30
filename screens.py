import pygame

import settings
from settings import WHITE, HEIGHT, WIDTH, BLACK
clock = pygame.time.Clock()

class screenz:
    def __init__(self):
        self.title_font = pygame.font.Font("pixelletters.ttf", 72)
        self.start_font = pygame.font.Font("pixelletters.ttf", 36)
        self.guide_font = pygame.font.Font("pixelletters.ttf", 30)
        self.upgrade_font = pygame.font.Font("pixelletters.ttf", 30)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.upgrade_button_color = (255, 255, 255)
        self.asteroid_upgrade_price = 50
        self.health_upgrade_price = 500
        self.coins = 10000

    def start_screen(self, screen):
        pygame.mouse.set_cursor(pygame.cursors.arrow)
        title_text = self.title_font.render('Inter-Galactic Star Warrior', True, WHITE)
        start_text = self.start_font.render('Press Any Key to Start', True, WHITE)
        guide_text = self.guide_font.render('WASD to move, shoot with left click, aim with mouse, dash on space', True, WHITE)
        upgrade_text = self.upgrade_font.render("Permanent upgrades", True, (0, 0, 0))
        iconsettings = pygame.image.load("Images/settingsicon.png")
        iconsettings = pygame.transform.scale(iconsettings, (50, 50))

        enemy_rocket_image_one = pygame.image.load("Images/SmallSpaceshipV1.png")
        enemy_rocket_image_one = pygame.transform.scale(enemy_rocket_image_one, (64, 64))
        enemy_rocket_image_one = pygame.transform.rotate(enemy_rocket_image_one, 30)
        enemy_rocket_image_two = pygame.transform.rotate(enemy_rocket_image_one, 100)

        enemy_rotating_spaceship_image = pygame.transform.scale(pygame.image.load("Images/Spaceship-rotating-1.png"), (64, 64))
        enemy_rotating_spaceship_image_one = pygame.transform.rotate(enemy_rotating_spaceship_image, -120)


        button_x = WIDTH//20
        button_y = HEIGHT//30
        button_width = 50
        button_height = 50

        upgrade_button_width = WIDTH/5
        upgrade_button_height = 50
        upgrade_button_x = WIDTH/2-upgrade_button_width/2
        upgrade_button_y = HEIGHT/2-18

        screen.fill(BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(guide_text, (WIDTH // 2 - guide_text.get_width() // 2, HEIGHT // 2 + 150))

        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
        screen.blit(iconsettings, (WIDTH // 20, HEIGHT // 30))

        # Upgrade-knappen bliver tegnet i while-løkken herunder.

        screen.blit(enemy_rocket_image_one, (WIDTH // 18, HEIGHT / 2))
        screen.blit(enemy_rocket_image_two, (WIDTH /1.3, HEIGHT / 5))
        screen.blit(enemy_rotating_spaceship_image_one, (WIDTH/1.2, HEIGHT/1.3))

        waiting = True
        while waiting:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (upgrade_button_x <= mouse_x <= upgrade_button_x + upgrade_button_width and
                            upgrade_button_y <= mouse_y <= upgrade_button_y + upgrade_button_height):
                self.upgrade_button_color = (205, 205, 205)
                pygame.draw.rect(screen, self.upgrade_button_color,
                                 (upgrade_button_x, upgrade_button_y, upgrade_button_width, upgrade_button_height))
                screen.blit(upgrade_text, (upgrade_button_x + (upgrade_button_width - upgrade_text.get_width()) / 2,
                                           upgrade_button_y + (upgrade_button_height - upgrade_text.get_height()) / 2))
            else:
                self.upgrade_button_color = (255, 255, 255)
                pygame.draw.rect(screen, self.upgrade_button_color,
                                 (upgrade_button_x, upgrade_button_y, upgrade_button_width, upgrade_button_height))
                screen.blit(upgrade_text, (upgrade_button_x + (upgrade_button_width - upgrade_text.get_width()) / 2,
                                           upgrade_button_y + (upgrade_button_height - upgrade_text.get_height()) / 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if (button_x <= mouse_x <= button_x + button_width and
                            button_y <= mouse_y <= button_y + button_height):
                        waiting = False
                        self.settings_screen(screen)
                    elif (upgrade_button_x <= mouse_x <= upgrade_button_x + upgrade_button_width and
                            upgrade_button_y <= mouse_y <= upgrade_button_y + upgrade_button_height):
                        waiting = False
                        self.permanent_upgrades_screen(screen)
            pygame.display.flip()


    def permanent_upgrades_screen(self, screen):
        screen.fill(BLACK)
        pygame.mouse.set_cursor(pygame.cursors.arrow)
        upgrade_text = self.title_font.render("Permanent upgrades", True, (255, 255, 255))

        # Return Button
        return_button_x = WIDTH // 20
        return_button_y = HEIGHT // 30
        return_button_width = 50
        return_button_height = 50

        # Asteroid upgrade button
        asteroid_upgrade_text = self.upgrade_font.render("Permanent Asteroid", True, (0, 0, 0))
        asteroid_button_width = WIDTH/3.5
        asteroid_button_height = HEIGHT/12
        asteroid_button_x = WIDTH/2-asteroid_button_width/2
        asteroid_button_y = HEIGHT/5
        asteroid_image = pygame.transform.scale(pygame.image.load("Images/asteroid_circle.png"), (64, 64))
        coin_image = pygame.transform.scale(pygame.image.load("Images/Money.png"), (64, 64))
        asteroid_price_text = self.upgrade_font.render(str(self.asteroid_upgrade_price), True, (0, 0, 0))

        # Health upgrade button
        health_upgrade_text = self.upgrade_font.render("Upgrade Starting Health", True, (0, 0, 0))
        health_button_width = WIDTH / 3.5
        health_button_height = HEIGHT / 12
        health_button_x = WIDTH / 2 - health_button_width / 2
        health_button_y = HEIGHT / 5 + 1.5*health_button_height
        health_image = pygame.transform.scale(pygame.image.load("Images/Hearth.png"), (64, 64))
        coin_image = pygame.transform.scale(pygame.image.load("Images/Money.png"), (64, 64))
        health_price_text = self.upgrade_font.render(str(self.health_upgrade_price), True, (0, 0, 0))

        # Coins
        coins_text = self.upgrade_font.render(str(self.coins), True, WHITE)
        coins_x = WIDTH-100
        coins_y = 24


        waiting = True
        while waiting:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Coins
            screen.blit(coins_text, (coins_x, coins_y))
            screen.blit(coin_image, (coins_x-52, coins_y-14))

            # Return button
            if (return_button_x <= mouse_x <= return_button_x + return_button_width and
                    return_button_y <= mouse_y <= return_button_y + return_button_height):
                return_button_color = (205, 205, 205)
            else:
                return_button_color = WHITE
            pygame.draw.rect(screen, return_button_color,
                             (return_button_x, return_button_y, return_button_width, return_button_height))
            screen.blit(pygame.transform.scale((pygame.image.load("Images/back.png")), (50, 50)), (WIDTH // 20, HEIGHT // 30))

            # Asteroid upgrade button
            if (asteroid_button_x <= mouse_x <= asteroid_button_x + asteroid_button_width and
                    asteroid_button_y <= mouse_y <= asteroid_button_y + asteroid_button_height):
                asteroid_button_color = (205, 205, 205)
            else:
                asteroid_button_color = (255, 255, 255)
            pygame.draw.rect(screen, asteroid_button_color, (asteroid_button_x, asteroid_button_y, asteroid_button_width, asteroid_button_height))
            screen.blit(asteroid_image, (asteroid_button_x, HEIGHT/5))
            screen.blit(coin_image, (WIDTH/2.05, HEIGHT/5+asteroid_upgrade_text.get_height()/1.8))
            screen.blit(asteroid_upgrade_text, (WIDTH / 1.85 - asteroid_upgrade_text.get_width() / 2, HEIGHT / 5))
            screen.blit(asteroid_price_text, (WIDTH/2.05+64, HEIGHT/5+asteroid_upgrade_text.get_height()*1.1))

            # Health upgrade button
            if (health_button_x <= mouse_x <= health_button_x + health_button_width and
                    health_button_y <= mouse_y <= health_button_y + health_button_height):
                health_button_color = (205, 205, 205)
            else:
                health_button_color = (255, 255, 255)
            pygame.draw.rect(screen, health_button_color,
                             (health_button_x, health_button_y, health_button_width, health_button_height))
            screen.blit(health_image, (health_button_x, health_button_y))
            screen.blit(coin_image, (WIDTH / 2.05, health_button_y + health_upgrade_text.get_height() / 1.8))
            screen.blit(health_upgrade_text, (WIDTH / 1.9 - health_upgrade_text.get_width() / 2, health_button_y))
            screen.blit(health_price_text, (WIDTH / 2.05 + 64,
                                              health_button_y + health_upgrade_text.get_height() * 1.1))

            screen.blit(upgrade_text, (WIDTH/2 - upgrade_text.get_width()/2, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and (return_button_x <= mouse_x <= return_button_x + return_button_width and
                        return_button_y <= mouse_y <= return_button_y + return_button_height):
                    # Reset game state as needed
                    # (e.g., reset player position, health, coins, etc.)
                    self.start_screen(screen)
                    waiting = False

            pygame.display.flip()



    def game_over_screen(self, screen, coins_collected):
        pygame.mouse.set_cursor(pygame.cursors.arrow)
        game_over_font = pygame.font.Font("pixelletters.ttf", 72)
        coins_font = pygame.font.Font("pixelletters.ttf", 50)
        try_again_font = pygame.font.Font("pixelletters.ttf", 50)
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
                        self.start_screen(screen)
                        waiting_for_input = False

            screen.fill(BLACK)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
            screen.blit(coins_text, (WIDTH // 2 - coins_text.get_width() // 2, HEIGHT // 2 - 30))
            pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
            screen.blit(try_again_text, (button_x + 10, button_y))
            pygame.draw.rect(screen, WHITE, (back_button_x, back_button_y, button_width, button_height))
            screen.blit(back_to_start_text, (back_button_x + 10, back_button_y))
            pygame.display.flip()

    def settings_screen(self, screen):
        pygame.init()
        pygame.mouse.set_cursor(pygame.cursors.arrow)

        # Colors
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREY = (200, 200, 200)

        # Fonts
        settings_font = pygame.font.Font("pixelletters.ttf", 50)

        # Difficulty Slider Variables
        slider_x = WIDTH // 2 - 100
        slider_y = HEIGHT // 2 - 50
        slider_width = 200
        slider_height = 10
        slider_handle = pygame.Rect(slider_x, slider_y - 5, 20, 20)
        slider_value = 50  # Adjust based on your game's difficulty scale

        # Dropdown for Screen Size
        screen_size_options = ["800x600", "1024x768", "1280x720", "1920x1080"]
        dropdown_x = WIDTH // 2 - 100
        dropdown_y = HEIGHT // 2 + 50
        dropdown_width = 200
        dropdown_height = 50
        dropdown_open = False
        selected_size = screen_size_options[0]

        back = pygame.image.load("Images/back.png")
        back = pygame.transform.scale(back, (50, 50))



        #Back Button
        button_x = WIDTH // 20
        button_y = HEIGHT // 30
        button_width = 50
        button_height = 50
        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if slider_handle.collidepoint(mouse_x, mouse_y):
                        dragging = True
                    if dropdown_x <= mouse_x <= dropdown_x + dropdown_width and \
                            dropdown_y <= mouse_y <= dropdown_y + dropdown_height:
                        dropdown_open = not dropdown_open
                    if (button_x <= mouse_x <= button_x + button_width and
                            button_y <= mouse_y <= button_y + button_height):
                        waiting_for_input = False
                        self.start_screen(screen)

                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False

                elif event.type == pygame.MOUSEMOTION:
                    if dragging:
                        slider_handle.x = max(min(event.pos[0], slider_x + slider_width - slider_handle.width),
                                              slider_x)
                        slider_value = int((slider_handle.x - slider_x) / slider_width * 100)

            # Drawing the settings screen
            screen.fill(BLACK)
            settings_text = settings_font.render('Settings', True, WHITE)
            screen.blit(settings_text, (WIDTH // 2 - settings_text
                                        .get_width() // 2, HEIGHT // 2 - 150))

            # Draw the difficulty slider
            pygame.draw.line(screen, GREY, (slider_x, slider_y), (slider_x + slider_width, slider_y), 5)
            pygame.draw.rect(screen, WHITE, slider_handle)

            # Draw the dropdown for screen size
            dropdown_rect = pygame.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height)
            pygame.draw.rect(screen, GREY, dropdown_rect)
            current_size_text = settings_font.render(selected_size, True, BLACK)
            screen.blit(current_size_text, (dropdown_x + 5, dropdown_y + 5))

            pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
            screen.blit(back, (WIDTH // 20, HEIGHT // 30))

            # If the dropdown is open, show the options
            if dropdown_open:
                for i, size in enumerate(screen_size_options):
                    option_rect = pygame.Rect(dropdown_x, dropdown_y + (i + 1) * dropdown_height, dropdown_width,
                                              dropdown_height)
                    pygame.draw.rect(screen, GREY, option_rect)
                    option_text = settings_font.render(size, True, BLACK)
                    screen.blit(option_text, (dropdown_x + 5, dropdown_y + (i + 1) * dropdown_height + 5))

                    # Check if an option is selected
                    if event.type == pygame.MOUSEBUTTONDOWN and option_rect.collidepoint(pygame.mouse.get_pos()):
                        selected_size = size
                        dropdown_open = False
                        screen_size_options = ["800x600", "1024x768", "1280x720", "1920x1080"]
                        if selected_size == screen_size_options[0]:
                            settings.WIDTH = 800
                            settings.HEIGHT = 600
                            self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
                        elif selected_size == screen_size_options[1]:
                            settings.WIDTH = 1024
                            settings.HEIGHT = 768
                            self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
                        elif selected_size == screen_size_options[2]:
                            settings.WIDTH = 1280
                            settings.HEIGHT = 720
                            self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
                        elif selected_size == screen_size_options[3]:
                            settings.WIDTH = 1920
                            settings.HEIGHT = 1080
                            self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))



            pygame.display.flip()
            clock.tick(30)



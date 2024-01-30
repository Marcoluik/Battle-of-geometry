import pygame

import settings
from settings import WHITE, HEIGHT, WIDTH, BLACK
clock = pygame.time.Clock()

class screenz:
    def __init__(self):
        self.title_font = pygame.font.Font("pixelletters.ttf", 72)
        self.start_font = pygame.font.Font("pixelletters.ttf", 36)
        self.guide_font = pygame.font.Font("pixelletters.ttf", 30)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.background_image = pygame.image.load("images/background.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

    def start_screen(self, screen):
        pygame.mouse.set_cursor(pygame.cursors.arrow)
        title_text = self.title_font.render('Battle of Geometry', True, WHITE)
        start_text = self.start_font.render('Press Any Key to Start', True, WHITE)
        guide_text = self.guide_font.render('WASD to move, shoot with left click, aim with mouse, dash on space', True, WHITE)
        iconsettings = pygame.image.load("Images/settingsicon.png")
        iconsettings = pygame.transform.scale(iconsettings, (50, 50))

        button_x = WIDTH//20
        button_y = HEIGHT//30
        button_width = 50
        button_height = 50

        screen.blit(self.background_image, (0, 0))
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(guide_text, (WIDTH // 2 - guide_text.get_width() // 2, HEIGHT // 2 + 150))

        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
        screen.blit(iconsettings, (WIDTH // 20 , HEIGHT//30))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if (button_x <= mouse_x <= button_x + button_width and
                            button_y <= mouse_y <= button_y + button_height):
                        waiting = False
                        self.settings_screen(screen)


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

            screen.blit(self.background_image, (0, 0))
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





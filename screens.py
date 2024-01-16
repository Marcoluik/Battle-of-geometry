import pygame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 1080, 540
clock = pygame.time.Clock()

class screenz:
    def __init__(self):
        self.title_font = pygame.font.Font("pixelletters.ttf", 72)
        self.start_font = pygame.font.Font("pixelletters.ttf", 36)
        self.guide_font = pygame.font.Font("pixelletters.ttf", 30)
    def start_screen(self, screen):


        title_text = self.title_font.render('Battle of Geometry', True, WHITE)
        start_text = self.start_font.render('Press Any Key to Start', True, WHITE)
        guide_text = self.guide_font.render('WASD to move, shoot with left click, aim with mouse, dash on space', True,
                                       WHITE)

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

    def game_over_screen(self, screen, coins_collected):
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
            clock.tick(30)
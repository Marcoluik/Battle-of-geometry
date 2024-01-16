import pygame
import screens


WIDTH, HEIGHT = screens.WIDTH, screens.HEIGHT
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
clock = pygame.time.Clock()
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
                            return 1
                        elif index == 1:
                            # Handle 'Health boost' button
                            print("Health boost selected")
                            return 2
                        elif index == 2:
                            # Handle 'Attack damage' button
                            print("Attack damage selected")
                            return 3

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
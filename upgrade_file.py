import pygame
import screens
import random

from settings import WHITE, HEIGHT, WIDTH, BLACK
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
clock = pygame.time.Clock()
def upgrade_window(screen, experience):
    upgrade_font = pygame.font.Font("pixelletters.ttf", 36)

    upgrade_text = upgrade_font.render('Choose an Upgrade', True, WHITE)
    button_texts = ['Movement speed', 'Health boost', 'Attack damage',"Dash length", "Shorter dash cooldown", "Shoot faster" ]
    upgrade_mapping = {
        'Movement speed': 1,
        'Health boost': 2,
        'Attack damage': 3,
        'Dash length': 4,
        'Shorter dash cooldown': 5,
        'Shoot faster': 6
    }

    selected_texts = random.sample(button_texts, 3)  # Randomly select three options
    buttons = []
    for i, text in enumerate(selected_texts):
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
                for button in buttons:
                    bx, by, bw, bh, btn_text = button
                    if bx <= mouse_x <= bx + bw and by <= mouse_y <= by + bh:
                        upgrade_id = upgrade_mapping[btn_text]
                        print(f"{btn_text} selected")
                        return upgrade_id

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
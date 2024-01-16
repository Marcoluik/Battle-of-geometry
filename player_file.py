import pygame
import screens
WIDTH, HEIGHT = screens.WIDTH, screens.HEIGHT

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 25
        self.color = (200, 200, 200)  # Assuming white color
        self.speed = 5
        self.health = 3
        self.dash_speed = 15  # Adjusted for multi-frame dash
        self.dash_duration = 10  # Dash duration in frames
        self.dash_cooldown = 500  # Cooldown in milliseconds
        self.last_dash = 0  # Time since last dash
        self.is_dashing = False
        self.dash_trail = []  # Store positions for the dash trail
        self.dash_frames_remaining = 0
        self.speed_reduction_per_frame = 0
        self.attackdmg = 1

    def draw(self, screen):
        # Draw the dash trail
        for pos, alpha in self.dash_trail:
            trail_color = (*self.color[:3], alpha)
            trail_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, trail_color, (self.size // 2, self.size // 2), self.size // 2.3)
            screen.blit(trail_surface, pos)

        # Draw the player
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        pygame.draw.circle(screen, (0,255,255), (center_x, center_y), self.size // 2)



        # Draw an ellipse on top of the circle to create a UFO effect
        ellipse_width = self.size * 2  # Adjust the width as needed
        ellipse_height = self.size * 0.8  # Adjust the height as needed
        ellipse_x = center_x - ellipse_width // 2
        ellipse_y = center_y - ellipse_height // 2.4
        pygame.draw.ellipse(screen, self.color, (ellipse_x, ellipse_y, ellipse_width, ellipse_height))

        # Draw the player
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2.2
        pygame.draw.circle(screen, (0, 255, 0), (center_x, center_y), self.size // 6)

        # Draw the player
        center_x = self.x + self.size // 1.1
        center_y = self.y + self.size // 2
        pygame.draw.circle(screen, (0, 255, 0), (center_x, center_y), self.size // 6)

        # Draw the player
        center_x = self.x + self.size // 8
        center_y = self.y + self.size // 2
        pygame.draw.circle(screen, (0, 255, 0), (center_x, center_y), self.size // 6)



    def move(self, dx, dy):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Constrain the new position to be within the screen boundaries
        # Adjust for the size of the player to prevent partial off-screen movement
        half_size = self.size // 2
        new_x = max(half_size, min(WIDTH - half_size, new_x))
        new_y = max(half_size, min(HEIGHT - half_size, new_y))

        # Update player's position
        self.x = new_x
        self.y = new_y

    def collides_with(self, other):
        distance_x = (self.x + self.size // 2) - (other.x + other.size // 2)
        distance_y = (self.y + self.size // 2) - (other.y + other.size // 2)
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

        # Check if the distance is less than the sum of the radii
        return distance < (self.size // 2 + other.size // 2)

    def update(self, current_time):
        if self.dash_frames_remaining > 0:
            # Reduce the speed
            self.speed -= self.speed_reduction_per_frame

            # Ensure the speed does not go below normal
            self.speed = max(self.speed, 5)

            # Decrement the counter
            self.dash_frames_remaining -= 1

            # Add current position to the dash trail
            self.dash_trail.append(((self.x, self.y), 255))
        else:
            # If dashing is over, start fading the trail
            self.fade_dash_trail()

        if current_time - self.last_dash > self.dash_cooldown and self.is_dashing:
            self.is_dashing = False
            self.speed = 5  # Resetting the speed to normal after dash ends

    def dash(self, current_time):
        if current_time - self.last_dash > self.dash_cooldown and not self.is_dashing:
            self.last_dash = current_time
            self.is_dashing = True  # Start dashing
            # Reset dash trail for new dash
            self.dash_trail.clear()
            # Add initial position to the dash trail with full opacity
            self.dash_trail.append(((self.x, self.y), 255))
            # Increase speed for the dash
            self.speed += self.dash_speed
            # Schedule to reset the speed and start fading the trail
            self.schedule_speed_reset()

    def schedule_speed_reset(self):
        # Define the duration of the dash effect in terms of frames or time
        dash_duration_frames = 8  # for example, 1 second at 60 FPS

        # Calculate the amount of speed reduction per frame
        speed_reduction_per_frame = (self.speed - 5) / dash_duration_frames

        # Store these values for use in the update method
        self.dash_frames_remaining = dash_duration_frames
        self.speed_reduction_per_frame = speed_reduction_per_frame

    def fade_dash_trail(self):
        # Fade out the dash trail
        new_trail = []
        alpha_decrement = max(1, 255 // self.dash_duration)  # Ensure at least 1 alpha decrement
        for pos, alpha in self.dash_trail:
            new_alpha = alpha - alpha_decrement
            if new_alpha > 0:
                new_trail.append((pos, new_alpha))
        self.dash_trail = new_trail
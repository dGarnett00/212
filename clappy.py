import pygame
import random

# Constants defining the game's main settings
SCREEN_WIDTH = 400            # Set the width of the game window to 400 pixels
SCREEN_HEIGHT = 600           # Set the height of the game window to 600 pixels
BIRD_START_X = 100            # Initial horizontal position for the bird
BIRD_START_Y = SCREEN_HEIGHT // 2  # Initial vertical position for the bird, centered vertically
PIPE_SPEED = 5                # The speed at which the pipes move to the left
GRAVITY = 0.5                 # The amount of downward force applied to the bird each frame
JUMP_STRENGTH = -10           # The upward force applied to the bird when it jumps (negative for upward motion)
FONT_SIZE = 36                # Font size for displaying the score

# Define colors using RGB values
WHITE = (255, 255, 255)       # White color
BLACK = (0, 0, 0)             # Black color
SKY_BLUE = (135, 206, 235)    # Light blue color representing the sky

class Bird:
    """Class to manage the bird's attributes and behaviors."""
    def __init__(self):
        # Load the bird's image and convert it for optimal usage
        self.image = pygame.image.load('bird.png').convert_alpha()
        # Create a rectangle to represent the bird's position and size
        self.rect = self.image.get_rect(center=(BIRD_START_X, BIRD_START_Y))
        # Initialize the bird's movement (i.e., its speed in the y-axis)
        self.movement = 0

    def update(self):
        """Update the bird's position by applying gravity."""
        self.movement += GRAVITY           # Increase the downward movement by gravity
        self.rect.centery += self.movement  # Move the bird's vertical position down by the movement value

    def jump(self):
        """Make the bird jump by applying a negative movement (upward)."""
        self.movement = JUMP_STRENGTH  # Set the bird's movement to the jump strength for an upward motion

class Pipe:
    """Class to manage the pipes' attributes and behaviors."""
    def __init__(self):
        # Load the pipe's image and convert it for optimal usage
        self.surface = pygame.image.load('pipe.png').convert_alpha()
        # Randomly set the height for the bottom pipe
        self.height = random.randint(200, 400)
        # Create a rectangle for the bottom pipe positioned at the generated height
        self.bottom_pipe = self.surface.get_rect(midtop=(500, self.height))
        # Create a rectangle for the top pipe positioned based on the bottom pipe
        self.top_pipe = self.surface.get_rect(midbottom=(500, self.height - 150))

    def update(self):
        """Move the pipes to the left by the PIPE_SPEED."""
        self.bottom_pipe.x -= PIPE_SPEED  # Decrease the x position of the bottom pipe
        self.top_pipe.x -= PIPE_SPEED      # Decrease the x position of the top pipe

    def reset(self):
        """Reset the pipe's position and height for the next set of pipes."""
        self.height = random.randint(200, 400)            # Randomly generate a new height for the pipes
        self.bottom_pipe.height = self.height              # Update the bottom pipe's height
        self.top_pipe.height = self.height - 150           # Set the height for the top pipe based on the bottom pipe
        self.bottom_pipe.x = 500                           # Reset the x position of the bottom pipe
        self.top_pipe.x = 500                              # Reset the x position of the top pipe
        # Position the bottom pipe correctly in the game world
        self.bottom_pipe.midtop = (self.bottom_pipe.centerx, self.bottom_pipe.top)
        # Position the top pipe correctly based on the bottom pipe
        self.top_pipe.midbottom = (self.bottom_pipe.centerx, self.bottom_pipe.top)

def check_collision(bird_rect, pipes):
    """Check if the bird has collided with pipes or the boundaries of the game window."""
    # Check if the bird has hit the top or bottom of the window
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True  # Collision detected with the window boundaries
    # Iterate through the pipes to check for collisions
    for pipe in pipes:
        if bird_rect.colliderect(pipe.bottom_pipe) or bird_rect.colliderect(pipe.top_pipe):
            return True  # Collision detected with a pipe
    return False  # No collisions detected

def draw_window(screen, bird, pipes, score):
    """Function to draw the current game state on the screen."""
    screen.fill(SKY_BLUE)  # Fill the screen with the sky blue color
    screen.blit(bird.image, bird.rect)  # Draw the bird on the screen

    # Draw each pipe in the pipes list
    for pipe in pipes:
        screen.blit(pipe.surface, pipe.bottom_pipe)  # Draw the bottom pipe
        screen.blit(pipe.surface, pipe.top_pipe)     # Draw the top pipe

    # Render the score text surface and draw it at the specified coordinates
    score_surface = pygame.font.Font(None, FONT_SIZE).render(f'Score: {score}', True, BLACK)
    screen.blit(score_surface, (10, 10))  # Draw the score text at (10, 10)
    
    pygame.display.update()  # Update the display so the new frame appears

def main():
    """Main function to run the game."""
    pygame.init()  # Initialize all Pygame modules
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Create a game window
    pygame.display.set_caption("Flappy Bird Clone")  # Set the title of the game window
    clock = pygame.time.Clock()  # Create a clock object to control the game's frame rate

    # Create instances of the game objects
    bird = Bird()  # Create a new bird object
    pipes = [Pipe()]  # Start the game with one pipe object
    score = 0  # Initialize the player's score to 0
    game_active = True  # Flag to track whether the game is active

    # Continue the game until a quit event occurs
    while True:
        for event in pygame.event.get():  # Check for all events in the Pygame event queue
            if event.type == pygame.QUIT:  # If the quit event is triggered
                pygame.quit()  # Close the game window
                exit()  # Exit the program
            # Handle the spacebar key press for jumping or restarting the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird.jump()  # Make the bird jump if the game is active
                    else:  # If the game is not active, restart
                        bird.rect.center = (BIRD_START_X, BIRD_START_Y)  # Reset the bird's position
                        score = 0  # Reset the score to 0
                        pipes = [Pipe()]  # Reset pipes for a new game
                        game_active = True  # Set the game to active state

        if game_active:
            bird.update()  # Update the bird's position based on gravity
            for pipe in pipes:
                pipe.update()  # Update each pipe's position

            # Check for scoring when the bottom pipe is at the specific position
            if pipes[0].bottom_pipe.x < 100 and pipes[0].bottom_pipe.x > 95:
                score += 1  # Increase the score by 1 when the bird passes through the pipes
            # If the bottom pipe moves off the screen, reset it and add a new pipe
            if pipes[0].bottom_pipe.x < -50:
                pipes.append(Pipe())  # Add a new pipe to the right of the screen
                pipes.pop(0)  # Remove the oldest pipe from the list

            # Check for collisions between the bird and pipes
            game_active = not check_collision(bird.rect, pipes)  # Set active state based on collision results

        draw_window(screen, bird, pipes, score)  # Draw the current game state
        clock.tick(120)  # Limit the frame rate to 120 FPS

# Start the game by calling the main function
if __name__ == "__main__":
    main()  # Run the main function to start the game
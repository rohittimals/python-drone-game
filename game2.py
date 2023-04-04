import pygame
import random
import sys

# Set the dimensions of the screen
WIDTH = 1000
HEIGHT = 1000

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Drone Dodger')

# Set up the font
font = pygame.font.SysFont(None, 36)

# Set up the clock
clock = pygame.time.Clock()

# Set up game variables
DRONE_X = 50
DRONE_Y = HEIGHT/2
DRONE_WIDTH = 50
DRONE_HEIGHT = 50
drone_speed = 5
obstacle_speed = 5
obstacle_width = 50
obstacle_height = 300
obstacle_gap = 200
score = 0 

# Define theDrone class
class Drone(pygame.Rect):
    pass

# Define the Obstacle class
class Obstacle():
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, obstacle_width, obstacle_height)
        self.passed = False

# Define the function to start/restart the game
def start_game():
    # Initialize variables
    drone = Drone(DRONE_X, DRONE_Y, DRONE_WIDTH, DRONE_HEIGHT)
    obstacles = [Obstacle(WIDTH, random.randint(0, HEIGHT - obstacle_height))]
    game_running = True
    game_ended = False
    start_button_hidden = True
    restart_button_hidden = True 
    global score; 

    # Main game loop
    while game_running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

        # Check for key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            drone.y -= drone_speed
        if keys[pygame.K_DOWN]:
            drone.y += drone_speed
        if keys[pygame.K_LEFT]:
            drone.x -= drone_speed
        if keys[pygame.K_RIGHT]:
            drone.x += drone_speed

        # Move the drone within screen boundaries
        if drone.top < 0:
            drone.top = 0
        if drone.bottom > HEIGHT:
            drone.bottom = HEIGHT
        if drone.left < 0:
            drone.left = 0
        if drone.right > WIDTH:
            drone.right = WIDTH

        # Move the obstacles
        for obstacle in obstacles:
            obstacle.rect.x -= obstacle_speed

        # Add new obstacle when there are none
        if not obstacles:
            new_obstacle_x = WIDTH
            new_obstacle_y = random.randint(0, HEIGHT - obstacle_height)
            new_obstacle = Obstacle(new_obstacle_x, new_obstacle_y)
            obstacles.append(new_obstacle)

        # Add new obstacle when the last one is close to the gap
        elif obstacles[-1].rect.right < WIDTH - obstacle_gap:
            new_obstacle_x = obstacles[-1].rect.x + obstacle_width + obstacle_gap
            new_obstacle_y = random.randint(0, HEIGHT - obstacle_height)
            new_obstacle = Obstacle(new_obstacle_x, new_obstacle_y)
            obstacles.append(new_obstacle)

        # Remove passed obstacles
        for obstacle in obstacles:
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)
                score += 1

        # Check for collision
        for obstacle in obstacles:
            if drone.colliderect(obstacle.rect):
                game_running = False
                game_ended = True

        # Draw the screen
        screen.fill(BLACK)

        # Draw the drone
        pygame.draw.rect(screen, BLUE, drone)

        # Draw the obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, GREEN, obstacle.rect)

        # Draw the score
        score_text = font.render(f"Score: {score}", True, RED)
        screen.blit(score_text, (20, 20))

        # Update the display
        pygame.display.update()

        # Set the frame rate
        clock.tick(60)

    # Game over screen
    while game_ended:
            # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_ended = True

                # Draw the screen
                screen.fill(BLACK)

                    # Draw the game over text
            game_over_text = font.render("Game Over", True, BLUE)
            screen.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2))

                # Draw the final score
            final_score_text = font.render(f"Final Score: {score}", True, BLUE)
            screen.blit(final_score_text, (WIDTH/2 - final_score_text.get_width()/2, HEIGHT/2 - final_score_text.get_height()/2 + 25))


            # Draw the restart button
            restart_button = pygame.Rect(WIDTH/2 - 100, HEIGHT/2 + 50, 200, 50)
            pygame.draw.rect(screen, RED, restart_button)


            restart_text = font.render("Restart", True, BLUE)
            screen.blit(restart_text, (WIDTH/2 - restart_text.get_width()/2, HEIGHT/2 + 65 - restart_text.get_height()/2))
            pygame.display.update()

                    # Check for restart button click
            mouse_pos = pygame.mouse.get_pos()
            if restart_button.collidepoint(mouse_pos):
                restart_button_hidden = False
                if pygame.mouse.get_pressed()[0]:
                    score = 0
                    start_game()

        # Update the display
            pygame.display.update()

    # Set the frame rate
            clock.tick(60)

start_game()
pygame.QUIT()
sys.exit()

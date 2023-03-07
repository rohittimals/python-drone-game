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

# Define the Drone class
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
    score = 0
    game_running = True
    start_button_hidden = True
    restart_button_hidden = False

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
            if not obstacles:
                obstacles.append(Obstacle(WIDTH, random.randint(0, HEIGHT - obstacle_height)))
            else:
                new_obstacle_x = obstacles[-1].rect.x + obstacle_width + obstacle_gap
                new_obstacle_y = random.randint(0, HEIGHT - obstacle_height)
                new_obstacle = Obstacle(new_obstacle_x, new_obstacle_y)
                obstacles.append(new_obstacle)

            # If obstacle goes off the screen, remove it from the list and add a new one
            if obstacle.rect.right < 0:
                obstacles.remove(obstacle)
                new_obstacle_x = obstacles[-1].rect.x + obstacle_width + obstacle_gap
                new_obstacle_y = random.randint(0, HEIGHT - obstacle_height)
                new_obstacle = Obstacle(new_obstacle_x, new_obstacle_y)
                obstacles.append(new_obstacle)

            # If drone collides
            # Check for collisions with obstacles
        for obstacle in obstacles:
            if drone.colliderect(obstacle.rect):
                game_running = False

                 # Update the score
            for obstacle in obstacles:
                if obstacle.rect.right < drone.left and obstacle.passed:
                    obstacle.passed = True
                    score += 1

        # Draw everything
            screen.fill(BLACK)

            for obstacle in obstacles:
                pygame.draw.rect(screen, GREEN, obstacle.rect)

                pygame.draw.rect(screen, BLUE, drone)

            score_text = font.render('Score: ' + str(score), True, WHITE)
            screen.blit(score_text, (10, 10))

    # Update the screen
            pygame.display.flip()

     #Tick the clock
            clock.tick(60)

    # Show the restart button
            start_button_hidden = True
            restart_button_hidden = False

    # Wait for a click on the restart button
        while restart_button_hidden:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    restart_button_hidden = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos): 
                        start_game()

        # Draw everything
        screen.fill(BLACK)

        restart_text = font.render('Restart', True, WHITE)
        restart_button = pygame.draw.rect(screen, BLUE, (WIDTH/2-50, HEIGHT/2-25, 100, 50))
        screen.blit(restart_text, (WIDTH/2-30, HEIGHT/2))

        # Update the screen
        pygame.display.flip()

    # Quit the game
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    start_game()

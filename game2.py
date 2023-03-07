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
    start_button_hidden = True
    restart_button_hidden = False
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

        
        final_score_text = font.render('Final Score: ' + str(score), True, WHITE)
        screen.blit(final_score_text, (WIDTH/2 - 100, HEIGHT/2 + 18))
        pygame.display.update()

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

        # Remove obstacles that have gone off the screen
        if obstacles[0].rect.right < 0:
            obstacles.pop(0)

        # Check for collision with obstacles
        for obstacle in obstacles:
            if drone.colliderect(obstacle.rect):
                game_running = False
                final_score_text = font.render('Final Score: ' + str(score), True, RED)
                screen.blit(final_score_text, (WIDTH/2 - 100, HEIGHT/2 + 18))
                restart_button_rect = pygame.draw.rect(screen, BLUE, (WIDTH/2 - 75, HEIGHT/2 + 54, 150, 50))
                restart_button_text = font.render('Restart', True, WHITE)
                screen.blit(restart_button_text, (WIDTH/2 - 40, HEIGHT/2 + 68))

        # Check for passing obstacles and update score
        for obstacle in obstacles:
            if obstacle.rect.right < drone.left and not obstacle.passed:
                obstacle.passed = True
                score += 1
                

            # Draw everything
            screen.fill(BLACK)
            pygame.draw.rect(screen, WHITE, drone)
            for obstacle in obstacles:
                pygame.draw.rect(screen, GREEN, obstacle.rect)
                score_text = font.render('Score: ' + str(score), True, BLUE)
                screen.blit(score_text, (10, 10))
                

        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        clock.tick(60)



# End game loop
# Display game over message and final score


# Wait for the player to click the restart button
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over_text = font.render('Game Over!', True, RED)
            screen.blit(game_over_text, (WIDTH/2 - 100, HEIGHT/2 - 18))
            final_score_text = font.render('Final Score: ' + str(score), True, WHITE)
            screen.blit(final_score_text, (WIDTH/2 - 100, HEIGHT/2 + 18))
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if restart_button_rect.collidepoint(mouse_pos):
                game_over_text = font.render('Game Over!', True, RED)
                
    # Draw the restart button
                restart_button_rect = pygame.draw.rect(screen, BLUE, (WIDTH/2 - 75, HEIGHT/2 + 54, 150, 50))
                restart_button_text = font.render('Restart', True, WHITE)
                screen.blit(restart_button_text, (WIDTH/2 - 40, HEIGHT/2 + 68))

    # Update the screen
    pygame.display.update()

    start_game()
    pygame.quit()


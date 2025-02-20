import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game Constants
BLOCK_SIZE = 20
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
FPS = 15

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

def generate_food(snake):
    """Generate food at random position not occupied by snake"""
    while True:
        x = random.randint(0, (SCREEN_WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (SCREEN_HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake:
            return (x, y)

def draw_snake(snake):
    """Draw snake on the screen"""
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def game_over_screen(score):
    """Display game over screen with score"""
    screen.fill(BLACK)
    text = font.render(f"Game Over! Score: {score}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()))
    text = font.render("Press Q to Quit", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2))
    pygame.display.flip()

def main():
    snake = [(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)]
    direction = (BLOCK_SIZE, 0)
    new_direction = direction  # Track pending direction changes
    food = generate_food(snake)
    score = 0
    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_q:
                        running = False
                else:
                    # Handle direction changes with queueing
                    if event.key == pygame.K_UP and direction != (0, BLOCK_SIZE):
                        new_direction = (0, -BLOCK_SIZE)
                    elif event.key == pygame.K_DOWN and direction != (0, -BLOCK_SIZE):
                        new_direction = (0, BLOCK_SIZE)
                    elif event.key == pygame.K_LEFT and direction != (BLOCK_SIZE, 0):
                        new_direction = (-BLOCK_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-BLOCK_SIZE, 0):
                        new_direction = (BLOCK_SIZE, 0)

        if not game_over:
            # Update direction once per frame
            direction = new_direction
            
            # Move snake
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            
            # Check collisions
            if (new_head in snake or
                new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
                new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT):
                game_over = True

            snake.insert(0, new_head)
            
            # Check food collision
            if new_head == food:
                score += 10
                food = generate_food(snake)
            else:
                snake.pop()

            # Draw everything
            screen.fill(BLACK)
            pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
            draw_snake(snake)
            text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(text, (10, 10))
            pygame.display.flip()

        else:
            game_over_screen(score)

        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
'''
snake_plus.py
- Use Deepseek R1 to iteratively develop Python-based Snake game
- Code should be complex, well-structured, well-commented
'''
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Game Constants (Increased window size)
BLOCK_SIZE = 20
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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
large_font = pygame.font.Font(None, 72)

def countdown():
    """Display 3-2-1-Go! countdown before game start"""
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        count_text = large_font.render(str(i), True, WHITE)
        count_rect = count_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(count_text, count_rect)
        pygame.display.flip()
        pygame.time.wait(1000)
    
    screen.fill(BLACK)
    go_text = large_font.render("GO!", True, GREEN)
    go_rect = go_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    screen.blit(go_text, go_rect)
    pygame.display.flip()
    pygame.time.wait(500)

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
    text = large_font.render(f"Game Over!", True, RED)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - 50))
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 + 20))
    text = font.render("Press Q to Quit or any key to restart", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 + 80))
    pygame.display.flip()

def title_screen():
    """Display title screen with start and settings buttons"""
    while True:
        screen.fill(BLACK)
        title_text = large_font.render("Snake Game", True, GREEN)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        screen.blit(title_text, title_rect)
        
        # Start Button
        start_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50)
        pygame.draw.rect(screen, GREEN, start_button)
        start_text = font.render("Start Game", True, BLACK)
        start_rect = start_text.get_rect(center=start_button.center)
        screen.blit(start_text, start_rect)
        
        # Settings Button
        settings_button = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 80, 200, 50)
        pygame.draw.rect(screen, WHITE, settings_button)
        settings_text = font.render("Settings", True, BLACK)
        settings_rect = settings_text.get_rect(center=settings_button.center)
        screen.blit(settings_text, settings_rect)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    countdown()
                    return
                elif settings_button.collidepoint(event.pos):
                    settings_screen()

def settings_screen():
    """Display settings screen"""
    while True:
        screen.fill(BLACK)
        title_text = large_font.render("Settings", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        screen.blit(title_text, title_rect)
        
        # Back Button
        back_button = pygame.Rect(SCREEN_WIDTH//2 - 60, SCREEN_HEIGHT - 100, 120, 40)
        pygame.draw.rect(screen, WHITE, back_button)
        back_text = font.render("Back", True, BLACK)
        back_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_rect)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return

def run_game():
    """Main game loop"""
    snake = [(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)]
    direction = (BLOCK_SIZE, 0)
    new_direction = direction
    food = generate_food(snake)
    score = 0
    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_q:
                        running = False
                    else:
                        running = False  # Return to title screen
                else:
                    if event.key == pygame.K_UP and direction != (0, BLOCK_SIZE):
                        new_direction = (0, -BLOCK_SIZE)
                    elif event.key == pygame.K_DOWN and direction != (0, -BLOCK_SIZE):
                        new_direction = (0, BLOCK_SIZE)
                    elif event.key == pygame.K_LEFT and direction != (BLOCK_SIZE, 0):
                        new_direction = (-BLOCK_SIZE, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-BLOCK_SIZE, 0):
                        new_direction = (BLOCK_SIZE, 0)

        if not game_over:
            direction = new_direction
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            
            if (new_head in snake or
                new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
                new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT):
                game_over = True

            snake.insert(0, new_head)
            
            if new_head == food:
                score += 10
                food = generate_food(snake)
            else:
                snake.pop()

            screen.fill(BLACK)
            pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
            draw_snake(snake)
            text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(text, (10, 10))
            pygame.display.flip()
        else:
            game_over_screen(score)

        clock.tick(FPS)

def main():
    """Main function handling screen transitions"""
    while True:
        title_screen()
        run_game()

if __name__ == "__main__":
    main()

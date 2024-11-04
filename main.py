import pygame
import random

# Initialize Pygame
pygame.init()

# Set up basic map settings
WIDTH, HEIGHT = 800, 600  # Size of the window
TILE_SIZE = 20  # Size of each tile in pixels

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WALL_COLOR = (100, 100, 100)
FLOOR_COLOR = (200, 200, 200)
PLAYER_COLOR = (0, 255, 0)
ENEMY_COLOR = (255, 0, 0)

# Set up display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roguelike Game")

# Set up the map grid
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
map_grid = [['#' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Player settings
player_x, player_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
player_health = 10
player_attack = 3

# Make sure player starts on a floor tile
map_grid[player_y][player_x] = '.'

# Enemy settings
enemies = []
num_enemies = 3

# Function to create rooms
def create_room(x, y, w, h):
    for i in range(y, y + h):
        for j in range(x, x + w):
            if 0 <= j < GRID_WIDTH and 0 <= i < GRID_HEIGHT:
                map_grid[i][j] = '.'

# Generate a few rooms for the dungeon
for _ in range(5):
    w, h = random.randint(3, 6), random.randint(3, 6)
    x, y = random.randint(1, GRID_WIDTH - w - 1), random.randint(1, GRID_HEIGHT - h - 1)
    create_room(x, y, w, h)

# Spawn enemies randomly in rooms
for _ in range(num_enemies):
    while True:
        enemy_x, enemy_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
        if map_grid[enemy_y][enemy_x] == '.':
            enemies.append({"x": enemy_x, "y": enemy_y, "health": 6, "attack": 2})
            break

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()  # Get current key states
    if keys[pygame.K_w] and player_y > 0 and map_grid[player_y - 1][player_x] == '.':
        player_y -= 1
    if keys[pygame.K_s] and player_y < GRID_HEIGHT - 1 and map_grid[player_y + 1][player_x] == '.':
        player_y += 1
    if keys[pygame.K_a] and player_x > 0 and map_grid[player_y][player_x - 1] == '.':
        player_x -= 1
    if keys[pygame.K_d] and player_x < GRID_WIDTH - 1 and map_grid[player_y][player_x + 1] == '.':
        player_x += 1

    # Clear the screen
    window.fill(BLACK)

    # Draw the map grid
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if map_grid[y][x] == '#':
                color = WALL_COLOR
            else:
                color = FLOOR_COLOR
            pygame.draw.rect(window, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw the player
    pygame.draw.rect(window, PLAYER_COLOR, (player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(window, ENEMY_COLOR, (enemy["x"] * TILE_SIZE, enemy["y"] * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Update the display
    pygame.display.flip()

    pygame.time.delay(100)  # Delay to slow down movement

# Quit Pygame
pygame.quit()

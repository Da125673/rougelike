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
player_health = 10  # Initialize player health
player_attack = 3  # Initialize player attack damage

# Room structure
rooms = []

# Function to create rooms
def create_room(x, y, w, h):
    for i in range(y, y + h):
        for j in range(x, x + w):
            if 0 <= j < GRID_WIDTH and 0 <= i < GRID_HEIGHT:
                map_grid[i][j] = '.'
    # Append the room’s center point to the list
    rooms.append((x + w // 2, y + h // 2))

# Function to create corridors between rooms
def create_corridor(start_x, start_y, end_x, end_y):
    # Horizontal corridor
    for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
        map_grid[start_y][x] = '.'
    # Vertical corridor
    for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
        map_grid[y][end_x] = '.'

# Generate a few rooms and connect them with corridors
for _ in range(5):
    w, h = random.randint(3, 6), random.randint(3, 6)
    x, y = random.randint(1, GRID_WIDTH - w - 1), random.randint(1, GRID_HEIGHT - h - 1)
    create_room(x, y, w, h)

# Connect each room to the next room with a corridor
for i in range(1, len(rooms)):
    create_corridor(rooms[i - 1][0], rooms[i - 1][1], rooms[i][0], rooms[i][1])

# Ensure the player starts on a floor tile in the first room
player_x, player_y = rooms[0]

# Enemy settings
enemies = []
num_enemies = 3

# Spawn enemies randomly in rooms
for _ in range(num_enemies):
    room = random.choice(rooms)
    enemy_x, enemy_y = room
    enemies.append({"x": enemy_x, "y": enemy_y, "health": 6, "attack": 2})

# Function to check for collision with enemies
def check_collision():
    global player_health, running  # Access global player_health and running variables
    for enemy in enemies:
        if enemy["x"] == player_x and enemy["y"] == player_y:
            # Combat interaction: reduce health
            player_health -= enemy["attack"]
            enemy["health"] -= player_attack
            print(f"Player health: {player_health}, Enemy health: {enemy['health']}")

            # Remove enemy if its health drops to zero or below
            if enemy["health"] <= 0:
                enemies.remove(enemy)
                print("Enemy defeated!")

            # End the game if player health is zero or below
            if player_health <= 0:
                print("Game Over! You have been defeated.")
                running = False  # Stop the main game loop

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
        check_collision()  # Check for collisions after movement
    if keys[pygame.K_s] and player_y < GRID_HEIGHT - 1 and map_grid[player_y + 1][player_x] == '.':
        player_y += 1
        check_collision()  # Check for collisions after movement
    if keys[pygame.K_a] and player_x > 0 and map_grid[player_y][player_x - 1] == '.':
        player_x -= 1
        check_collision()  # Check for collisions after movement
    if keys[pygame.K_d] and player_x < GRID_WIDTH - 1 and map_grid[player_y][player_x + 1] == '.':
        player_x += 1
        check_collision()  # Check for collisions after movement

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

# Display "Game Over" message before quitting
font = pygame.font.Font(None, 74)
text = font.render("Game Over", True, WHITE)
window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
pygame.display.flip()
pygame.time.delay(2000)  # Display for 2 seconds

# Quit Pygame
pygame.quit()

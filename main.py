import pygame
import random
from player import Player
from enemy import Enemy

# Initialize Pygame and define settings
pygame.init()
WIDTH, HEIGHT, TILE_SIZE = 800, 600, 20
BLACK, WHITE, WALL_COLOR, FLOOR_COLOR, PLAYER_COLOR, ENEMY_COLOR = (0, 0, 0), (255, 255, 255), (100, 100, 100), (200, 200, 200), (0, 255, 0), (255, 0, 0)
GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE

# Set up display
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roguelike Game")

# Create the game map
map_grid = [['#' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
rooms = []  # Store the rooms for connecting and enemy/player placement
enemies = []  # List to store enemies

# Function to create rooms
def create_room(x, y, w, h):
    for i in range(x, x + w):
        for j in range(y, y + h):
            if 0 <= i < GRID_WIDTH and 0 <= j < GRID_HEIGHT:
                map_grid[j][i] = '.'
    rooms.append((x + w // 2, y + h // 2))

# Function to create corridors between rooms
def create_corridor(start_x, start_y, end_x, end_y):
    if start_x != end_x:
        for x in range(min(start_x, end_x), max(start_x, end_x) + 1):
            if 0 <= x < GRID_WIDTH and 0 <= start_y < GRID_HEIGHT:
                map_grid[start_y][x] = '.'
    if start_y != end_y:
        for y in range(min(start_y, end_y), max(start_y, end_y) + 1):
            if 0 <= end_x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                map_grid[y][end_x] = '.'

# Generate rooms and corridors, ensuring they connect
for _ in range(5):
    room_x, room_y = random.randint(1, GRID_WIDTH - 10), random.randint(1, GRID_HEIGHT - 10)
    room_w, room_h = random.randint(4, 8), random.randint(4, 8)
    create_room(room_x, room_y, room_w, room_h)

    # Connect to previous room if it exists
    if len(rooms) > 1:
        prev_x, prev_y = rooms[-2]
        curr_x, curr_y = rooms[-1]
        create_corridor(prev_x, prev_y, curr_x, curr_y)

# Create player in the first room
player_x, player_y = rooms[0]
player = Player(player_x, player_y)

# Spawn enemies in other rooms, avoiding the player’s room
for room in rooms[1:]:
    enemy_x, enemy_y = room
    if (enemy_x, enemy_y) != (player.x, player.y):
        enemies.append(Enemy(enemy_x, enemy_y))

# Main game loop
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: 
        player.move(0, -1, map_grid, enemies)  # Pass enemies to check collision
    if keys[pygame.K_s]: 
        player.move(0, 1, map_grid, enemies)   # Pass enemies to check collision
    if keys[pygame.K_a]: 
        player.move(-1, 0, map_grid, enemies)  # Pass enemies to check collision
    if keys[pygame.K_d]: 
        player.move(1, 0, map_grid, enemies)   # Pass enemies to check collision

    # Get current time for attack cooldown
    current_time = pygame.time.get_ticks()

    # Handle player attack with spacebar
    if keys[pygame.K_SPACE] and player.can_attack(current_time):
        print("Attack initiated!")  # Debugging line
        for enemy in enemies:
            if enemy.x == player.x and enemy.y == player.y:
                print(f"Attacking enemy at ({enemy.x}, {enemy.y})")  # Debugging line
                player.attack_enemy(enemy)  # Attack enemy
                break  # You can only attack one enemy at a time

    # Enemy behavior
    for enemy in enemies:
        if abs(enemy.x - player.x) > 3 or abs(enemy.y - player.y) > 3:
            enemy.move_randomly(map_grid, enemies)  # Move randomly if not close
        else:
            enemy.move_towards_player(player.x, player.y, map_grid, enemies)  # Move towards player if close

        # Check if enemy touches the player (enemy attack)
        if enemy.x == player.x and enemy.y == player.y:
            print(f"Enemy attacks player at ({player.x}, {player.y})")  # Debugging line
            player.take_damage(enemy.attack)  # Player takes damage from enemy
            if player.health <= 0:
                print("Game Over! You have been defeated.")
                running = False

        # If an enemy is defeated, remove it
        if enemy.health <= 0:
            enemies.remove(enemy)

    # Check if all enemies are defeated
    if not enemies:
        print("You win! All enemies are defeated.")
        running = False

    # Rendering code
    window.fill(BLACK)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = WALL_COLOR if map_grid[y][x] == '#' else FLOOR_COLOR
            pygame.draw.rect(window, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw player and enemies
    pygame.draw.rect(window, PLAYER_COLOR, (player.x * TILE_SIZE, player.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    for enemy in enemies:
        pygame.draw.rect(window, ENEMY_COLOR, (enemy.x * TILE_SIZE, enemy.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()

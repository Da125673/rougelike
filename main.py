import random  # Import random module for random positions and values


# Basic map settings
WIDTH, HEIGHT = 40, 20  # Set map width and height
player_x, player_y = WIDTH // 2, HEIGHT // 2  # Initialize player at the map center
map_grid = [['#' for _ in range(WIDTH)] for _ in range(HEIGHT)]  # Fill map with walls ('#')

# Player attributes
player_health = 10  # Set initial player health
player_attack = 3  # Set player attack power

# Enemy settings
enemies = []  # List to store enemy data (position, health)
num_enemies = 3  # Number of enemies to spawn

# Function to create rooms
def create_room(x, y, w, h):
    for i in range(y, y + h):  # Loop over room height
        for j in range(x, x + w):  # Loop over room width
            if 0 <= j < WIDTH and 0 <= i < HEIGHT:  # Check if within map bounds
                map_grid[i][j] = '.'  # Mark cell as floor ('.')

# Function to create corridors between rooms
def create_corridor(x1, y1, x2, y2):
    x, y = x1, y1  # Start from the first point (x1, y1)
    while x != x2:  # Horizontal movement towards the second point
        map_grid[y][x] = '.'  # Mark as floor
        x += 1 if x < x2 else -1  # Move right if x1 < x2, else move left
    while y != y2:  # Vertical movement towards the second point
        map_grid[y][x] = '.'  # Mark as floor
        y += 1 if y < y2 else -1  # Move down if y1 < y2, else move up

# Generate rooms and corridors
rooms = []  # List to track room centers
num_rooms = 5  # Number of rooms to create
for _ in range(num_rooms):
    w, h = random.randint(5, 10), random.randint(3, 6)  # Random room dimensions
    x, y = random.randint(1, WIDTH - w - 1), random.randint(1, HEIGHT - h - 1)  # Random room position
    create_room(x, y, w, h)  # Create room with these parameters
    if rooms:  # If there's at least one room created
        prev_x, prev_y = rooms[-1]  # Get the last room's center
        create_corridor(prev_x, prev_y, x, y)  # Connect last room to current room
    rooms.append((x + w // 2, y + h // 2))  # Add the center of this room to rooms list

# Player starts in the first room created
player_x, player_y = rooms[0]  # Set player's initial position to the first room's center

# Spawn enemies in random rooms
for _ in range(num_enemies):
    room_x, room_y = random.choice(rooms)  # Choose a random room center
    enemy_x = random.randint(room_x - 2, room_x + 2)  # Random x near the room center
    enemy_y = random.randint(room_y - 2, room_y + 2)  # Random y near the room center
    if map_grid[enemy_y][enemy_x] == '.':  # Check if the cell is floor
        enemies.append({"x": enemy_x, "y": enemy_y, "health": 6, "attack": 2})  # Add enemy with health and attack

# Function to display the map
def display_map():
    for y in range(HEIGHT):  # Loop over map rows
        for x in range(WIDTH):  # Loop over map columns
            if x == player_x and y == player_y:
                print('@', end='')  # Display player character ('@')
            elif any(e["x"] == x and e["y"] == y for e in enemies):
                print('E', end='')  # Display enemy character ('E')
            else:
                print(map_grid[y][x], end='')  # Display map cell (floor or wall)
        print()  # Newline at end of each row
    print(f"\nPlayer Health: {player_health}")  # Show player's current health

# Function to move player
def move_player(dx, dy):
    global player_x, player_y
    new_x, new_y = player_x + dx, player_y + dy  # Calculate player's new position
    if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and map_grid[new_y][new_x] == '.':  # Check bounds and floor
        player_x, player_y = new_x, new_y  # Update player position

# Function to move enemies toward the player
def move_enemies():
    for enemy in enemies:
        if abs(enemy["x"] - player_x) + abs(enemy["y"] - player_y) <= 5:  # If within range
            dx = 1 if player_x > enemy["x"] else -1 if player_x < enemy["x"] else 0  # Determine x direction
            dy = 1 if player_y > enemy["y"] else -1 if player_y < enemy["y"] else 0  # Determine y direction
            new_x, new_y = enemy["x"] + dx, enemy["y"] + dy  # Calculate new enemy position
            if map_grid[new_y][new_x] == '.' and (new_x, new_y) != (player_x, player_y):  # If cell is floor and not player
                enemy["x"], enemy["y"] = new_x, new_y  # Update enemy position

# Function for player to attack adjacent enemies
def player_attack_action():
    global enemies
    for enemy in enemies:
        if abs(enemy["x"] - player_x) <= 1 and abs(enemy["y"] - player_y) <= 1:  # Check if enemy is adjacent
            print("You attack an enemy!")
            enemy["health"] -= player_attack  # Reduce enemy's health by player's attack
            if enemy["health"] <= 0:
                print("Enemy defeated!")  # Display defeat message
                enemies.remove(enemy)  # Remove enemy from list if health is zero
            return  # Stop after attacking one enemy

# Function to handle enemy engagement with the player
def enemy_engagement():
    global player_health
    for enemy in enemies:
        if abs(enemy["x"] - player_x) <= 1 and abs(enemy["y"] - player_y) <= 1:  # Check if enemy is adjacent
            print("An enemy attacks you!")  # Display attack message
            player_health -= enemy["attack"]  # Reduce player's health by enemy's attack
            if player_health <= 0:
                print("You have been defeated!")  # Game over message if health is zero
                return True  # Return True to indicate game over
    return False  # Return False if player survives

# Main game loop
while True:
    display_map()  # Show the map and player/enemy positions
    move = input("Move (WASD to move, F to attack, Q to quit): ").strip().lower()  # Get user input
    if move == 'w':
        move_player(0, -1)  # Move player up
    elif move == 's':
        move_player(0, 1)  # Move player down
    elif move == 'a':
        move_player(-1, 0)  # Move player left
    elif move == 'd':
        move_player(1, 0)  # Move player right
    elif move == 'f':  # Attack action
        player_attack_action()  # Call function for player attack
    elif move == 'q':
        print("Thanks for playing!")  # Exit message
        break  # End game loop
    else:
        print("Invalid move! Use W, A, S, D to move, F to attack, or Q to quit.")  # Invalid input message

    move_enemies()  # Move enemies closer to the player
    if enemy_engagement():  # Check if player is alive
        break  # End game loop if player health is zero

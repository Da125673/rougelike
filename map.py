import random  # Import random module to use for random positioning

# Basic map settings
WIDTH, HEIGHT = 40, 20  # Define the map's width and height
player_x, player_y = WIDTH // 2, HEIGHT // 2  # Set player's starting position in the center of the map
map_grid = [['#' for _ in range(WIDTH)] for _ in range(HEIGHT)]  # Initialize the map with walls ('#') in all cells

# Player attributes
player_health = 10  # Set the player's starting health

# Enemy settings
enemies = []  # Initialize a list to store enemy positions and health
num_enemies = 3  # Set the number of enemies to spawn

# Function to create a room on the map
def create_room(x, y, w, h):
    for i in range(y, y + h):  # Loop through each row in the room's height
        for j in range(x, x + w):  # Loop through each column in the room's width
            if 0 <= j < WIDTH and 0 <= i < HEIGHT:  # Check if position is within map bounds
                map_grid[i][j] = '.'  # Set the cell to floor ('.') to represent room space

# Function to create corridors connecting rooms
def create_corridor(x1, y1, x2, y2):
    x, y = x1, y1  # Start at the first position
    while x != x2:  # Move horizontally towards the target x-coordinate
        map_grid[y][x] = '.'  # Set cell to floor ('.') for the corridor
        x += 1 if x < x2 else -1  # Move right if x < x2, left if x > x2
    while y != y2:  # Move vertically towards the target y-coordinate
        map_grid[y][x] = '.'  # Set cell to floor ('.') for the corridor
        y += 1 if y < y2 else -1  # Move down if y < y2, up if y > y2

# Generate rooms and corridors on the map
rooms = []  # Initialize a list to store the center of each room
num_rooms = 5  # Define the number of rooms to create
for _ in range(num_rooms):
    w, h = random.randint(5, 10), random.randint(3, 6)  # Randomize room width and height
    x, y = random.randint(1, WIDTH - w - 1), random.randint(1, HEIGHT - h - 1)  # Randomize room position
    create_room(x, y, w, h)  # Call function to create the room at this position with given dimensions
    if rooms:  # If there are previous rooms
        prev_x, prev_y = rooms[-1]  # Get the center of the last room
        create_corridor(prev_x, prev_y, x, y)  # Connect the current room to the last room with a corridor
    rooms.append((x + w // 2, y + h // 2))  # Store the center of the room

# Set player's starting position in the first room
player_x, player_y = rooms[0]

# Spawn enemies at random positions within rooms
for _ in range(num_enemies):
    room_x, room_y = random.choice(rooms)  # Select a random room's center
    enemy_x = random.randint(room_x - 2, room_x + 2)  # Set enemy x position near the room center
    enemy_y = random.randint(room_y - 2, room_y + 2)  # Set enemy y position near the room center
    if map_grid[enemy_y][enemy_x] == '.':  # Check if the cell is floor (not a wall)
        enemies.append({"x": enemy_x, "y": enemy_y, "health": 5})  # Add enemy position and health to list

# Function to display the map in the console
def display_map():
    for y in range(HEIGHT):  # Loop through each row in the map
        for x in range(WIDTH):  # Loop through each cell in the row
            if x == player_x and y == player_y:  # Check if this cell is the player's position
                print('@', end='')  # Print the player symbol ('@')
            elif any(e["x"] == x and e["y"] == y for e in enemies):  # Check if this cell contains an enemy
                print('E', end='')  # Print the enemy symbol ('E')
            else:
                print(map_grid[y][x], end='')  # Print the map cell (wall or floor)
        print()  # New line after each row
    print(f"\nPlayer Health: {player_health}\n")  # Display the player's health after the map

# Function to move the player on the map
def move_player(dx, dy):
    global player_x, player_y  # Access the global player coordinates
    new_x, new_y = player_x + dx, player_y + dy  # Calculate the player's new position
    if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and map_grid[new_y][new_x] == '.':  # Check if the new position is within bounds and not a wall
        player_x, player_y = new_x, new_y  # Update player's position

# Function to move enemies towards the player
def move_enemies():
    for enemy in enemies:  # Loop through each enemy in the list
        # Check if the enemy is within 5 tiles of the player
        if abs(enemy["x"] - player_x) + abs(enemy["y"] - player_y) <= 5:
            # Move one step towards the player
            dx = 1 if player_x > enemy["x"] else -1 if player_x < enemy["x"] else 0
            dy = 1 if player_y > enemy["y"] else -1 if player_y < enemy["y"] else 0
            new_x, new_y = enemy["x"] + dx, enemy["y"] + dy  # Calculate new position for the enemy
            if map_grid[new_y][new_x] == '.' and (new_x, new_y) != (player_x, player_y):  # Ensure new cell is floor and not the player’s position
                enemy["x"], enemy["y"] = new_x, new_y  # Update enemy's position

# Function to check if an enemy is adjacent to the player and engage
def check_engagement():
    global player_health  # Access the player's health
    for enemy in enemies:  # Loop through each enemy
        if abs(enemy["x"] - player_x) <= 1 and abs(enemy["y"] - player_y) <= 1:  # Check if enemy is adjacent to player
            print("An enemy attacks you!")  # Inform the player of an attack
            player_health -= 1  # Decrease player health by 1
            if player_health <= 0:  # Check if player health has dropped to zero
                print("You have been defeated by the enemies!")  # Game over message
                return True  # Return True to indicate game over
    return False  # Return False if the player is still alive

# Main game loop
while True:
    display_map()  # Show the map, player, and enemies
    move = input("Move (WASD to move, Q to quit): ").strip().lower()  # Get user input for movement or quitting
    if move == 'w':  # Move up
        move_player(0, -1)
    elif move == 's':  # Move down
        move_player(0, 1)
    elif move == 'a':  # Move left
        move_player(-1, 0)
    elif move == 'd':  # Move right
        move_player(1, 0)
    elif move == 'q':  # Quit the game
        print("Thanks for playing!")
        break
    else:
        print("Invalid move! Use W, A, S, D to move, or Q to quit.")  # Error message for invalid input

    move_enemies()  # Move enemies closer to the player
    if check_engagement():  # Check if any enemies engage the player
        break  # Exit loop if game over

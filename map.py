import random

# Basic map settings
WIDTH, HEIGHT = 40, 20  # Dimensions of the map (width and height)
player_x, player_y = WIDTH // 2, HEIGHT // 2  # Starting position of the player
map_grid = [['#' for _ in range(WIDTH)] for _ in range(HEIGHT)]  # Map filled with walls ('#') initially

# Function to create a room on the map
def create_room(x, y, w, h):
    # Iterate over the area defined by the room dimensions
    for i in range(y, y + h):
        for j in range(x, x + w):
            # Ensure we're within map bounds before changing cells
            if 0 <= j < WIDTH and 0 <= i < HEIGHT:
                map_grid[i][j] = '.'  # Empty space (room floor) inside the room

# Function to create corridors between rooms
def create_corridor(x1, y1, x2, y2):
    # Start with the current position
    x, y = x1, y1
    # Randomly determine the direction of the corridor (horizontal first, then vertical, or vice versa)
    while x != x2:
        map_grid[y][x] = '.'  # Corridor floor
        x += 1 if x < x2 else -1
    while y != y2:
        map_grid[y][x] = '.'  # Corridor floor
        y += 1 if y < y2 else -1

# Generate random rooms and corridors on the map
rooms = []
num_rooms = 5  # Number of rooms to create

for _ in range(num_rooms):
    # Random width and height of the room
    w, h = random.randint(5, 10), random.randint(3, 6)
    # Random position for the top-left corner of the room
    x, y = random.randint(1, WIDTH - w - 1), random.randint(1, HEIGHT - h - 1)
    create_room(x, y, w, h)  # Create the room
    if rooms:
        # Connect the current room to the previous room with a corridor
        prev_x, prev_y = rooms[-1]
        create_corridor(prev_x, prev_y, x, y)
    # Store the center point of the room
    rooms.append((x + w // 2, y + h // 2))

# Set the player's starting position in the first room
player_x, player_y = rooms[0]

# Function to display the map in the console
def display_map():
    # Iterate over each row in the map
    for y in range(HEIGHT):
        # Iterate over each cell in the row
        for x in range(WIDTH):
            # Check if this cell is the player's position
            if x == player_x and y == player_y:
                print('@', end='')  # Display the player character
            else:
                print(map_grid[y][x], end='')  # Display the map element (floor or wall)
        print()  # Newline at the end of each row
    print()  # Extra newline for spacing after displaying the map

# Function to handle player movement
def move_player(dx, dy):
    global player_x, player_y
    # Calculate the new position of the player
    new_x, new_y = player_x + dx, player_y + dy
    # Ensure the new position is within bounds and not a wall
    if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and map_grid[new_y][new_x] == '.':
        player_x, player_y = new_x, new_y  # Update player position

# Main game loop
while True:
    display_map()  # Display the map with the player’s current position
    move = input("Move (WASD to move, Q to quit): ").strip().lower()  # Get player input
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
        print("Invalid move! Use W, A, S, D to move, or Q to quit.")

import random  # Importing random to use later for adding random elements like enemies or items

# Basic map settings
WIDTH, HEIGHT = 20, 10  # Dimensions of the map grid
player_x, player_y = WIDTH // 2, HEIGHT // 2  # Initial position of the player in the center of the map
map_grid = [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]  # Create a 2D list representing the map, filled with '.' (empty space)

# Function to display the map with the player
def display_map():
    # Loop over each row in the map
    for y in range(HEIGHT):
        # Loop over each column in the row
        for x in range(WIDTH):
            # If the current position is where the player is, display '@'
            if x == player_x and y == player_y:
                print('@', end='')  # '@' represents the player
            else:
                print(map_grid[y][x], end='')  # Print the current cell ('.' for empty spaces)
        print()  # Newline after each row to format the map correctly
    print()  # Extra newline for spacing after the map

# Function to move the player based on input direction
def move_player(dx, dy):
    global player_x, player_y  # Allow modification of the player's position
    new_x, new_y = player_x + dx, player_y + dy  # Calculate the new position based on movement direction
    
    # Check if the new position is within map bounds and if the cell is empty ('.')
    if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT and map_grid[new_y][new_x] == '.':
        player_x, player_y = new_x, new_y  # Update the player's position to the new position

# Main game loop
while True:
    display_map()  # Display the map with the player’s current position
    
    # Get movement input from the player
    move = input("Move (WASD): ").strip().lower()  # Strip whitespace and convert input to lowercase
    
    # Move player based on input
    if move == 'w':  # Move up
        move_player(0, -1)  # Decrease y-coordinate by 1 to move up
    elif move == 's':  # Move down
        move_player(0, 1)  # Increase y-coordinate by 1 to move down
    elif move == 'a':  # Move left
        move_player(-1, 0)  # Decrease x-coordinate by 1 to move left
    elif move == 'd':  # Move right
        move_player(1, 0)  # Increase x-coordinate by 1 to move right
    elif move == 'q':  # Quit the game
        print("Thanks for playing!")  # Friendly exit message
        break  # Exit the game loop to end the program
    else:
        print("Invalid move! Use W, A, S, D to move, or Q to quit.")  # Error message for invalid input

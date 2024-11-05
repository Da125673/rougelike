import random

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 10  # Example health value
        self.attack = 2    # Example attack value

    def move_randomly(self, map_grid):
        # Choose a random direction to move
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # Down, Up, Right, Left
        new_x = self.x + direction[0]
        new_y = self.y + direction[1]

        # Check if the new position is valid (within bounds and not a wall)
        if 0 <= new_x < len(map_grid[0]) and 0 <= new_y < len(map_grid) and map_grid[new_y][new_x] != '#':
            self.x = new_x
            self.y = new_y

    def move_towards_player(self, player_x, player_y, map_grid):
        # Move towards the player if within 3 blocks and valid space
        if abs(self.x - player_x) <= 3 and abs(self.y - player_y) <= 3:
            # Check horizontal movement
            if self.x < player_x and map_grid[self.y][self.x + 1] != '#':  # Move right
                self.x += 1
            elif self.x > player_x and map_grid[self.y][self.x - 1] != '#':  # Move left
                self.x -= 1

            # Check vertical movement
            if self.y < player_y and map_grid[self.y + 1][self.x] != '#':  # Move down
                self.y += 1
            elif self.y > player_y and map_grid[self.y - 1][self.x] != '#':  # Move up
                self.y -= 1

    def take_damage(self, damage):
        self.health -= damage

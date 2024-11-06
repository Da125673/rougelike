class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50  # Player starts with 50 health
        self.attack = 5   # Attack value for the player

    def move(self, dx, dy, map_grid):
        new_x, new_y = self.x + dx, self.y + dy
        # Check if the new position is not a wall
        if 0 <= new_x < len(map_grid[0]) and 0 <= new_y < len(map_grid):
            if map_grid[new_y][new_x] != '#':  # Ensure the new spot is not a wall
                self.x, self.y = new_x, new_y

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print("You have been defeated!")

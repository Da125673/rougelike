class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 10  # Enemies start with 10 health
        self.attack = 3    # Attack value for the enemy

    def move_randomly(self, map_grid):
        # Enemy randomly moves, ensuring it doesn't move through walls
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < len(map_grid[0]) and 0 <= new_y < len(map_grid):
            if map_grid[new_y][new_x] != '#':
                self.x, self.y = new_x, new_y

    def move_towards_player(self, player_x, player_y, map_grid):
        # Enemy moves towards the player if within a certain distance
        if self.x < player_x and map_grid[self.y][self.x + 1] != '#':
            self.x += 1
        elif self.x > player_x and map_grid[self.y][self.x - 1] != '#':
            self.x -= 1
        elif self.y < player_y and map_grid[self.y + 1][self.x] != '#':
            self.y += 1
        elif self.y > player_y and map_grid[self.y - 1][self.x] != '#':
            self.y -= 1

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"Enemy at ({self.x}, {self.y}) has been defeated!")

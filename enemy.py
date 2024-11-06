import random

class Enemy:
    def __init__(self, x, y, health=10, attack=2):
        self.x = x
        self.y = y
        self.health = health
        self.attack = attack

    def move_randomly(self, map_grid):
        # Logic for random movement (this should avoid walls and boundaries)
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
        random.shuffle(directions)  # Randomize the direction

        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < len(map_grid[0]) and 0 <= new_y < len(map_grid) and map_grid[new_y][new_x] == '.':
                self.x, self.y = new_x, new_y
                break

    def move_towards_player(self, player_x, player_y, map_grid):
        # Move towards the player
        dx = 0
        dy = 0
        if self.x < player_x:
            dx = 1
        elif self.x > player_x:
            dx = -1
        if self.y < player_y:
            dy = 1
        elif self.y > player_y:
            dy = -1

        # Check if the new position is valid (not a wall)
        if 0 <= self.x + dx < len(map_grid[0]) and 0 <= self.y + dy < len(map_grid):
            if map_grid[self.y + dy][self.x + dx] == '.':
                self.x += dx
                self.y += dy

    def take_damage(self, amount):
        """Reduce health by the specified amount."""
        self.health -= amount
        if self.health < 0:
            self.health = 0

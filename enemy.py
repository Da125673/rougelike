import random

class Enemy:
    def __init__(self, x, y, health=6, attack=2):
        self.x = x
        self.y = y
        self.health = health
        self.attack = attack

    def move_towards_player(self, player_x, player_y, map_grid):
        # Simple logic to move toward the player
        if self.x < player_x and map_grid[self.y][self.x + 1] == '.':
            self.x += 1
        elif self.x > player_x and map_grid[self.y][self.x - 1] == '.':
            self.x -= 1
        elif self.y < player_y and map_grid[self.y + 1][self.x] == '.':
            self.y += 1
        elif self.y > player_y and map_grid[self.y - 1][self.x] == '.':
            self.y -= 1

    def take_damage(self, amount):
        self.health -= amount

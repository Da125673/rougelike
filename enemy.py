# enemy.py
import random
import time

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 10
        self.attack = 5  # Enemy attack power
        self.attack_range = 1  # Can attack adjacent cells (within 1 tile)
        self.last_attack_time = 0  # Timestamp of last attack for cooldown

    def move_randomly(self, map_grid):
        dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < len(map_grid[0]) and 0 <= new_y < len(map_grid):
            if map_grid[new_y][new_x] != '#':  # If it's not a wall
                self.x = new_x
                self.y = new_y

    def move_towards_player(self, player_x, player_y, map_grid):
        if self.x < player_x:
            self.x += 1
        elif self.x > player_x:
            self.x -= 1

        if self.y < player_y:
            self.y += 1
        elif self.y > player_y:
            self.y -= 1

    def attack_player(self, player):
        # Check if the player is within attack range
        if abs(self.x - player.x) <= self.attack_range and abs(self.y - player.y) <= self.attack_range:
            damage = self.attack
            player.take_damage(damage)
            print(f"Enemy attacks player for {damage} damage!")
            return True
        return False

    def can_attack(self):
        return time.time() - self.last_attack_time > 1  # 1 second cooldown for attack

    def reset_attack_time(self):
        self.last_attack_time = time.time()

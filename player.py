# player.py
import random
import time

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 50
        self.attack = 10  # Player attack power
        self.attack_range = 1  # Can attack adjacent cells (within 1 tile)
        self.last_attack_time = 0  # Timestamp of last attack for cooldown

    def move(self, dx, dy, map_grid):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < len(map_grid[0]) and 0 <= new_y < len(map_grid):
            if map_grid[new_y][new_x] != '#':  # If it's not a wall
                self.x = new_x
                self.y = new_y

    def attack_enemy(self, enemy):
        # Check if the enemy is in range (adjacent to the player)
        if abs(self.x - enemy.x) <= self.attack_range and abs(self.y - enemy.y) <= self.attack_range:
            damage = self.attack
            enemy.health -= damage
            print(f"Player attacks enemy for {damage} damage!")
            return True
        return False

    def take_damage(self, amount):
        self.health -= amount
        print(f"Player takes {amount} damage!")
    
    def can_attack(self):
        return time.time() - self.last_attack_time > 1  # 1 second cooldown for attack

    def reset_attack_time(self):
        self.last_attack_time = time.time()

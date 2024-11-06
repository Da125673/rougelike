import pygame

class Player:
    def __init__(self, x, y, health=50, attack=5):
        self.x = x
        self.y = y
        self.health = 50
        self.attack = 2
        self.last_attack_time = 0  # For attack cooldown management
        self.attack_cooldown = 500  # Milliseconds cooldown between attacks

    def move(self, dx, dy, map_grid, enemies):
        new_x, new_y = self.x + dx, self.y + dy
        if 0 <= new_x < len(map_grid[0]) and 0 <= new_y < len(map_grid):
            if map_grid[new_y][new_x] == '.':  # Can move to this space
                for enemy in enemies:
                    if enemy.x == new_x and enemy.y == new_y:  # Collision with enemy
                        return  # Block movement if collision with enemy
                self.x, self.y = new_x, new_y

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print("Player is defeated!")

    def can_attack(self, current_time):
        # Check if enough time has passed since the last attack (cooldown)
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            return True
        return False

    def attack_enemy(self, enemy):
        enemy.take_damage(self.attack)

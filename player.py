import pygame

class Player:
    def __init__(self, x, y, health=10, attack=3):
        self.x = x
        self.y = y
        self.health = health
        self.attack = attack

    def move(self, dx, dy, map_grid):
        # Attempt to move the player and check map boundaries
        if map_grid[self.y + dy][self.x + dx] == '.':
            self.x += dx
            self.y += dy

    def take_damage(self, amount):
        self.health -= amount

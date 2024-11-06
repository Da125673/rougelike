import random

class Enemy:
    def __init__(self, x, y, health=10, attack=2):
        self.x = x
        self.y = y
        self.health = health
        self.attack = attack

    def move_randomly(self, map_grid, enemies):
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # up, down, left, right
        random.shuffle(directions)

        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy

            # Check if the new position is within bounds, not a wall, and not occupied by an enemy or player
            if 0 <= new_x < len(map_grid[0]) and 0 <= new_y < len(map_grid):
                if map_grid[new_y][new_x] == '.':  # It's a valid floor space
                    # Check if there's already another character (enemy or player)
                    occupied = False
                    for enemy in enemies:
                        if enemy.x == new_x and enemy.y == new_y:
                            occupied = True
                            break
                    if not occupied:
                        self.x, self.y = new_x, new_y
                        break

    def move_towards_player(self, player_x, player_y, map_grid, enemies):
        dx, dy = 0, 0
        if self.x < player_x:
            dx = 1
        elif self.x > player_x:
            dx = -1
        if self.y < player_y:
            dy = 1
        elif self.y > player_y:
            dy = -1

        # Check if the new position is valid (not a wall or occupied by another entity)
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < len(map_grid[0]) and 0 <= new_y < len(map_grid):
            if map_grid[new_y][new_x] == '.':  # It's a valid floor space
                # Check if there's already an enemy or player in the new position
                for enemy in enemies:
                    if enemy.x == new_x and enemy.y == new_y:
                        return  # Don't move if another enemy is there
                if player_x == new_x and player_y == new_y:
                    return  # Don't move if the player is in that space
                self.x, self.y = new_x, new_y

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print("Enemy is defeated!")

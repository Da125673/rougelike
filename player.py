class Player:
    def __init__(self, x, y, health=50, attack=5):
        self.x = x
        self.y = y
        self.health = health
        self.attack = attack

    def move(self, dx, dy, map_grid, enemies):
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the new position is within bounds and not a wall
        if 0 <= new_x < len(map_grid[0]) and 0 <= new_y < len(map_grid):
            if map_grid[new_y][new_x] == '.':  # If it's a floor space
                # Check if the new position is not occupied by any enemy
                for enemy in enemies:
                    if enemy.x == new_x and enemy.y == new_y:
                        return  # If there is an enemy, don't move

                # If no enemy, move the player
                self.x = new_x
                self.y = new_y

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            print("Player is defeated!")

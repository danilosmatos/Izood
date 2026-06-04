import pygame

from game.config import TILE_SIZE


class TileMap:
    def __init__(self, raw_map):
        self.raw_map = raw_map
        self.rows = len(raw_map)
        self.cols = len(raw_map[0])

        self.player_start = None
        self.restaurant_position = None
        self.client_positions = {}

        self._parse_map()

    def _parse_map(self):
        for row_index, row in enumerate(self.raw_map):
            for col_index, symbol in enumerate(row):
                position = (row_index, col_index)

                if symbol == "P":
                    self.player_start = position
                elif symbol == "R":
                    self.restaurant_position = position
                elif symbol.isdigit():
                    self.client_positions[symbol] = position

    def is_inside_map(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_wall(self, row, col):
        return self.raw_map[row][col] == "#"

    def is_walkable(self, row, col):
        if not self.is_inside_map(row, col):
            return False

        return not self.is_wall(row, col)

    def get_tile_symbol(self, row, col):
        return self.raw_map[row][col]

    def draw(self, screen):
        for row_index, row in enumerate(self.raw_map):
            for col_index, symbol in enumerate(row):
                rect = pygame.Rect(
                    col_index * TILE_SIZE,
                    row_index * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE,
                )

                if symbol == "#":
                    color = (40, 40, 40)
                elif symbol == "R":
                    color = (210, 90, 70)
                elif symbol.isdigit():
                    color = (80, 160, 220)
                else:
                    color = (180, 180, 180)

                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (80, 80, 80), rect, 1)
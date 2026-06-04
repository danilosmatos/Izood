import pygame

from game.config import TILE_SIZE


class Player:
    def __init__(self, start_position):
        self.row, self.col = start_position

    @property
    def position(self):
        return self.row, self.col

    def try_move(self, delta_row, delta_col, tilemap):
        new_row = self.row + delta_row
        new_col = self.col + delta_col

        if tilemap.is_walkable(new_row, new_col):
            self.row = new_row
            self.col = new_col

    def draw(self, screen):
        rect = pygame.Rect(
            self.col * TILE_SIZE + 6,
            self.row * TILE_SIZE + 6,
            TILE_SIZE - 12,
            TILE_SIZE - 12,
        )

        pygame.draw.rect(screen, (255, 230, 80), rect)
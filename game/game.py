import pygame

from game.config import (
    FPS,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MAP_WIDTH,
    TITLE,
)
from game.tilemap import TileMap
from game.player import Player

CITY_MAP = [
    "####################",
    "#P....#......1.....#",
    "#.##..#.####...##..#",
    "#..#..#....#.......#",
    "#..#..####.#.####..#",
    "#..#.......#....#..#",
    "#..####.######..#..#",
    "#R......#....#..2..#",
    "#######.#.##.#.##..#",
    "#3......#..#.......#",
    "#..######..#######.#",
    "#......4..........5#",
    "####################",
]
    

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.tilemap = TileMap(CITY_MAP)
        self.player = Player(self.tilemap.player_start)

        self.font = pygame.font.SysFont(None, 24)

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key in (pygame.K_w, pygame.K_UP):
                    self.player.try_move(-1, 0, self.tilemap)

                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    self.player.try_move(1, 0, self.tilemap)

                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    self.player.try_move(0, -1, self.tilemap)

                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    self.player.try_move(0, 1, self.tilemap)

                elif event.key == pygame.K_r:
                    print("Antônio")

                elif event.key == pygame.K_i:
                    print("Eudes")

    def draw(self):
        self.screen.fill((20, 20, 20))

        self.tilemap.draw(self.screen)
        self.player.draw(self.screen)

        self.draw_hud()

        pygame.display.flip()

    def draw_hud(self):
        hud_x = MAP_WIDTH + 20

        title = self.font.render("iZood", True, (255, 255, 255))
        self.screen.blit(title, (hud_x, 30))

        position_text = self.font.render(
            f"Posição: {self.player.position}",
            True,
            (230, 230, 230),
        )
        self.screen.blit(position_text, (hud_x, 70))

        controls = [
            "WASD/Setas: mover",
            "R: calcular rota",
            "I: inventário",
            "ESC: sair",
        ]

        for index, text in enumerate(controls):
            rendered = self.font.render(text, True, (210, 210, 210))
            self.screen.blit(rendered, (hud_x, 120 + index * 30))
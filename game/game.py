import pygame

from game.config import (
    FPS,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MAP_WIDTH,
    TITLE,
    TILE_SIZE,
    FONT_SIZE,
    SMALL_FONT_SIZE,
)
from game.tilemap import TileMap
from game.player import Player
from game.coleta import SistemaColeta
from game.entrega import SistemaEntrega
from game.passos import ContadorDePassosJogo


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


PEDIDOS_INICIAIS = [
    {"id": 1, "cliente_id": "1", "nome": "Pizza suspeita"},
    {"id": 2, "cliente_id": "2", "nome": "Hambúrguer frio"},
    {"id": 3, "cliente_id": "3", "nome": "Açaí sem banana"},
    {"id": 4, "cliente_id": "4", "nome": "Pastel de vento"},
    {"id": 5, "cliente_id": "5", "nome": "Sushi de bairro"},
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

        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.small_font = pygame.font.SysFont(None, SMALL_FONT_SIZE)

        self.coleta = SistemaColeta(capacidade_maxima=5)
        self.entrega = SistemaEntrega()
        self.contador_passos = ContadorDePassosJogo()

        self.pedidos_disponiveis = list(PEDIDOS_INICIAIS)
        self.pedidos_ja_coletados = False

        self.clientes = self.criar_clientes()

        self.mensagem = "Pegue os pedidos no restaurante."
        self.vitoria = False

    def criar_clientes(self):
        clientes = []

        for cliente_id, posicao in self.tilemap.client_positions.items():
            clientes.append(
                {
                    "id": cliente_id,
                    "posicao": posicao,
                    "entregue": False,
                }
            )

        return clientes

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

                if self.vitoria:
                    return

                if event.key in (pygame.K_w, pygame.K_UP):
                    self.mover_jogador(-1, 0)

                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    self.mover_jogador(1, 0)

                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    self.mover_jogador(0, -1)

                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    self.mover_jogador(0, 1)

                elif event.key == pygame.K_r:
                    print("Antônio")

                elif event.key == pygame.K_i:
                    print("Eudes")

    def mover_jogador(self, delta_row, delta_col):
        movimento_valido = self.player.try_move(delta_row, delta_col, self.tilemap)

        if not movimento_valido:
            self.mensagem = "Caminho bloqueado."
            return

        self.contador_passos.registrar_passo()
        self.verificar_interacoes()

    def verificar_interacoes(self):
        self.verificar_coleta_no_restaurante()
        self.verificar_entrega_cliente()
        self.verificar_vitoria()

    def verificar_coleta_no_restaurante(self):
        if self.player.position != self.tilemap.restaurant_position:
            return

        if self.pedidos_ja_coletados:
            if not self.todos_clientes_entregues():
                self.mensagem = "Pedidos já foram coletados. Faça as entregas."
            return

        mensagens = []

        for pedido in self.pedidos_disponiveis:
            sucesso, mensagem = self.coleta.coletar_pedido(
                self.player.position,
                self.tilemap.restaurant_position,
                pedido,
            )

            if sucesso:
                mensagens.append(mensagem)

        self.pedidos_ja_coletados = True
        self.mensagem = "Pedidos coletados."

    def verificar_entrega_cliente(self):
        sucesso, mensagem = self.entrega.entregar_pedido(
            self.player.position,
            self.clientes,
            self.coleta,
        )

        if mensagem:
            self.mensagem = mensagem

    def verificar_vitoria(self):
        if not self.todos_clientes_entregues():
            return

        if self.player.position != self.tilemap.restaurant_position:
            self.mensagem = "Todas as entregas foram feitas. Volte ao restaurante."
            return

        self.vitoria = True
        self.mensagem = "Vitória!"

    def todos_clientes_entregues(self):
        return all(cliente["entregue"] for cliente in self.clientes)

    def entregas_feitas(self):
        return sum(1 for cliente in self.clientes if cliente["entregue"])

    def draw(self):
        self.screen.fill((20, 20, 20))

        self.tilemap.draw(self.screen)
        self.desenhar_status_clientes()
        self.player.draw(self.screen)
        self.draw_hud()

        if self.vitoria:
            self.draw_victory_message()

        pygame.display.flip()

    def desenhar_status_clientes(self):
        for cliente in self.clientes:
            row, col = cliente["posicao"]

            rect = pygame.Rect(
                col * TILE_SIZE + 8,
                row * TILE_SIZE + 8,
                TILE_SIZE - 16,
                TILE_SIZE - 16,
            )

            if cliente["entregue"]:
                color = (40, 180, 80)
            else:
                color = (80, 160, 220)

            pygame.draw.rect(self.screen, color, rect)

            label = self.small_font.render(
                f"C{cliente['id']}",
                True,
                (255, 255, 255),
            )
            self.screen.blit(label, (col * TILE_SIZE + 5, row * TILE_SIZE - 2))

    def draw_hud(self):
        hud_x = MAP_WIDTH + 20

        title = self.font.render("iZood", True, (255, 255, 255))
        self.screen.blit(title, (hud_x, 30))

        position_text = self.font.render(
            f"Posição: {self.player.position}",
            True,
            (230, 230, 230),
        )
        self.screen.blit(position_text, (hud_x, 65))

        self.contador_passos.desenhar_contador(self.screen, hud_x, 95)

        entregas_text = self.font.render(
            f"Entregas: {self.entregas_feitas()}/{len(self.clientes)}",
            True,
            (230, 230, 230),
        )
        self.screen.blit(entregas_text, (hud_x, 125))

        mensagem_titulo = self.font.render("Mensagem:", True, (255, 255, 255))
        self.screen.blit(mensagem_titulo, (hud_x, 165))

        mensagem_texto = self.small_font.render(
            self.mensagem,
            True,
            (220, 220, 220),
        )
        self.screen.blit(mensagem_texto, (hud_x, 190))

        self.coleta.desenhar_inventario(self.screen, hud_x, 230)

        controls = [
            "WASD/Setas: mover",
            "R: calcular rota",
            "I: inventário",
            "ESC: sair",
        ]

        start_y = 370

        for index, text in enumerate(controls):
            rendered = self.small_font.render(text, True, (210, 210, 210))
            self.screen.blit(rendered, (hud_x, start_y + index * 24))

    def draw_victory_message(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        title = self.font.render(
            "ENTREGAS CONCLUÍDAS!",
            True,
            (255, 255, 255),
        )

        subtitle = self.font.render(
            f"Total de passos: {self.contador_passos.passos_efetuados}",
            True,
            (255, 255, 0),
        )

        instruction = self.font.render(
            "Pressione ESC para sair.",
            True,
            (220, 220, 220),
        )

        self.screen.blit(title, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2))
        self.screen.blit(instruction, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 40))
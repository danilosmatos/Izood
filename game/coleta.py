import pygame


class SistemaColeta:
    def __init__(self, capacidade_maxima=5):
        self.capacidade_maxima = capacidade_maxima
        self.itens = []

    def coletar_pedido(self, jogador_pos, restaurante_pos, pedido_disponivel):
        if jogador_pos != restaurante_pos:
            return False, "Você precisa estar no restaurante para coletar pedidos."

        if len(self.itens) >= self.capacidade_maxima:
            return False, "Inventário cheio! Entregue alguns pedidos primeiro."

        if pedido_disponivel is None:
            return False, "Não há pedido disponível."

        self.itens.append(pedido_disponivel)
        return True, f"Pedido coletado: {pedido_disponivel['nome']}"

    def tem_pedido_cliente(self, cliente_id):
        return any(item["cliente_id"] == cliente_id for item in self.itens)

    def remover_pedido_cliente(self, cliente_id):
        for item in self.itens:
            if item["cliente_id"] == cliente_id:
                self.itens.remove(item)
                return item

        return None

    def desenhar_inventario(self, tela, x, y):
        fonte = pygame.font.SysFont(None, 22)

        titulo = fonte.render(
            f"Mochila ({len(self.itens)}/{self.capacidade_maxima})",
            True,
            (255, 255, 255),
        )
        tela.blit(titulo, (x, y))

        if not self.itens:
            vazio = fonte.render("- vazia", True, (200, 200, 200))
            tela.blit(vazio, (x, y + 25))
            return

        for i, item in enumerate(self.itens):
            texto_item = fonte.render(
                f"- {item['nome']} -> C{item['cliente_id']}",
                True,
                (200, 200, 200),
            )
            tela.blit(texto_item, (x, y + 25 + (i * 20)))
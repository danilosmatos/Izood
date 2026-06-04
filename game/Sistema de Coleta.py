import pygame

class SistemaColeta:
    def __init__(self, capacidade_maxima=5):
        self.capacidade_maxima = capacidade_maxima
        self.itens = []  # Uso essa como placeholder para o sitema de inventario
        # Lista de dicionários: {'id': int, 'cliente_id': int, 'nome': str}

    def coletar_pedido(self, jogador_pos, restaurante_pos, pedido_disponivel):
        """Requisito 1: Pega o pedido se o jogador estiver no restaurante."""
        # Verifica se o jogador está na mesma posição do restaurante
        if jogador_pos != restaurante_pos:
            print("Você precisa estar no restaurante para coletar pedidos!")
            return False
            
        # Verifica limite de espaço no inventário
        if len(self.itens) >= self.capacidade_maxima:
            print("Inventário cheio! Entregue alguns pedidos primeiro.")
            return False

        if pedido_disponivel:
            self.itens.append(pedido_disponivel)
            print(f"Pedido {pedido_disponivel['nome']} coletado com sucesso!")
            return True
        return False

    # UI simples para o inventario
    def desenhar_inventario(self, tela, x, y):
        """Desenha visualmente os itens do inventário na tela."""
        fonte = pygame.font.SysFont(None, 24)
        titulo = fonte.render(f"Inventário ({len(self.itens)}/{self.capacidade_maxima}):", True, (255, 255, 255))
        tela.blit(titulo, (x, y))
        
        for i, item in enumerate(self.itens):
            texto_item = fonte.render(f"- {item['nome']} (Cliente {item['cliente_id']})", True, (200, 200, 200))
            tela.blit(texto_item, (x, y + 25 + (i * 20)))

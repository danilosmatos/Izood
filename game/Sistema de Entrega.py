class SistemaEntrega:
    def __init__(self):
        pass

    def entregar_pedido(self, jogador_pos, lista_clientes, inventario):
        """Requisito 2: Entrega o pedido correto para o cliente se estiver perto."""
        #lista_clientes: [{'id': int, 'posicao': [x:int, y:int], 'entregue': bool}]

        for cliente in lista_clientes:
            # Verifica se o cliente ainda precisa de entrega e se o jogador está na posição dele
            if not cliente['entregue'] and jogador_pos == cliente['posicao']:
                
                # Procura no inventário o pedido correspondente a este cliente
                for item in inventario.itens:
                    if item['cliente_id'] == cliente['id']:
                        inventario.itens.remove(item)
                        cliente['entregue'] = True
                        print(f"Pedido entregue com sucesso para o Cliente {cliente['id']}!")
                        return True
                        
                print(f"Você não tem o pedido do Cliente {cliente['id']} no inventário!")
                return False
        return False

    # UI simles
    def desenhar_clientes(self, tela, lista_clientes):
        """Desenha os clientes no mapa com cores diferentes para status de entrega."""
        for cliente in lista_clientes:
            cor = (0, 255, 0) if cliente['entregue'] else (255, 0, 0) # Verde se entregue, Vermelho se pendente
            pygame.draw.circle(tela, cor, cliente['posicao'], 15)
            
            fonte = pygame.font.SysFont(None, 20)
            texto = fonte.render(f"C{cliente['id']}", True, (255, 255, 255))
            tela.blit(texto, (cliente['posicao'][0] - 10, cliente['posicao'][1] - 30))

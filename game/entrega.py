class SistemaEntrega:
    def entregar_pedido(self, jogador_pos, lista_clientes, inventario):
        for cliente in lista_clientes:
            if cliente["entregue"]:
                continue

            if jogador_pos != cliente["posicao"]:
                continue

            pedido = inventario.remover_pedido_cliente(cliente["id"])

            if pedido is None:
                return False, f"Você não tem o pedido do Cliente {cliente['id']}."

            cliente["entregue"] = True
            return True, f"Pedido entregue ao Cliente {cliente['id']}!"

        return False, ""
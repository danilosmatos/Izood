from collections import deque


def caminho_minimo(tilemap, origem, destino):
    if origem == destino:
        return [origem]

    fila = deque([origem])
    visitados = {origem}
    anteriores = {origem: None}

    while fila:
        atual = fila.popleft()

        if atual == destino:
            break

        row, col = atual

        for delta_row, delta_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            vizinho = (row + delta_row, col + delta_col)

            if vizinho in visitados:
                continue

            if not tilemap.is_walkable(*vizinho):
                continue

            visitados.add(vizinho)
            anteriores[vizinho] = atual
            fila.append(vizinho)

    if destino not in anteriores:
        return []

    caminho = []
    atual = destino

    while atual is not None:
        caminho.append(atual)
        atual = anteriores[atual]

    caminho.reverse()
    return caminho


def distancia_minima(tilemap, origem, destino):
    caminho = caminho_minimo(tilemap, origem, destino)

    if not caminho:
        return None

    return len(caminho) - 1

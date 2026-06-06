from collections import deque


def bfs(tilemap, origem, destino):
    visitados = []
    fila = [origem]
    visitados.append(origem)
    anteriores = {origem: None}


    while len(fila) > 0:
        no_atual = fila.pop(0)

        if no_atual == destino:
            break

        row, col = no_atual

        for delta_row, delta_col in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            vizinho = (row + delta_row + delta_col)

            if vizinho not in visitados and tilemap.is_walkable(*vizinho):
                visitados.append(vizinho)
                anteriores[vizinho] = no_atual
                fila.append(vizinho)


    if destino not in anteriores:
        return []
    
    caminho = []
    return caminho


def distancia(tilemap, origem, destino):
    caminho = bfs(tilemap, origem, destino)

    if not caminho:
        return None
    return len(caminho) - 1

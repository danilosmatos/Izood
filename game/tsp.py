import itertools

from game.pathfinding import caminho_minimo, distancia_minima


def matriz_distancias(tilemap, pontos):
    tamanho = len(pontos)
    matriz = [[0] * tamanho for _ in range(tamanho)]

    for i in range(tamanho):
        for j in range(i + 1, tamanho):
            distancia = distancia_minima(tilemap, pontos[i], pontos[j])

            if distancia is None:
                raise ValueError(
                    f"Não há caminho entre {pontos[i]} e {pontos[j]}"
                )

            matriz[i][j] = distancia
            matriz[j][i] = distancia

    return matriz


def resolver_tsp(matriz, indice_depot=0):
    quantidade = len(matriz)

    if quantidade <= 1:
        return [], 0

    indices_clientes = [i for i in range(quantidade) if i != indice_depot]

    if not indices_clientes:
        return [], 0

    melhor_ordem = None
    melhor_custo = float("inf")

    for permutacao in itertools.permutations(indices_clientes):
        custo = matriz[indice_depot][permutacao[0]]

        for indice_atual, indice_proximo in zip(permutacao, permutacao[1:]):
            custo += matriz[indice_atual][indice_proximo]

        custo += matriz[permutacao[-1]][indice_depot]

        if custo < melhor_custo:
            melhor_custo = custo
            melhor_ordem = list(permutacao)

    return melhor_ordem, int(melhor_custo)


def calcular_rota_entregas(tilemap, restaurante_pos, clientes_posicoes):
    ids_ordenados = sorted(clientes_posicoes.keys(), key=lambda cliente_id: int(cliente_id))
    pontos = [restaurante_pos] + [clientes_posicoes[cliente_id] for cliente_id in ids_ordenados]

    matriz = matriz_distancias(tilemap, pontos)
    ordem_indices, custo_tsp = resolver_tsp(matriz, indice_depot=0)

    ordem_clientes = [ids_ordenados[indice - 1] for indice in ordem_indices]

    paradas = [restaurante_pos]
    for indice in ordem_indices:
        paradas.append(pontos[indice])
    paradas.append(restaurante_pos)

    caminho = []

    for origem, destino in zip(paradas, paradas[1:]):
        trecho = caminho_minimo(tilemap, origem, destino)

        if not trecho:
            raise ValueError(f"Não foi possível montar o caminho entre {origem} e {destino}")

        if caminho:
            trecho = trecho[1:]

        caminho.extend(trecho)

    return {
        "ordem_clientes": ordem_clientes,
        "passos_totais": len(caminho) - 1,
        "caminho": caminho,
        "custo_tsp": custo_tsp,
    }

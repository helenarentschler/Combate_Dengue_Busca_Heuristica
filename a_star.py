import heapq

# Tipos de tile:
# G = grama (custo 1), M = lama (custo 3)
# Qualquer outra letra representa um obstáculo.
CUSTOS = {"G": 1, "M": 3}


def check_neighbours(tile, end, came_from, g_score, open, closed, mapa):
    # No mapa: mapa[linha][coluna] -> mapa[y][x]
    tile_x = tile[0]
    tile_y = tile[1]

    end_x = end[0]
    end_y = end[1]

    ALTURA = len(mapa)
    LARGURA = len(mapa[0])

    # None significa que o tile está fora do mapa ou é um obstáculo.
    up = down = right = left = None

    if tile_y - 1 >= 0:
        up = mapa[tile_y - 1][tile_x]
    if tile_y + 1 < ALTURA:
        down = mapa[tile_y + 1][tile_x]
    if tile_x + 1 < LARGURA:
        right = mapa[tile_y][tile_x + 1]
    if tile_x - 1 >= 0:
        left = mapa[tile_y][tile_x - 1]

    # Agora guardamos o vizinho junto com o custo do seu terreno.
    vizinhos = []
    if right in CUSTOS:
            vizinhos.append(((tile_x + 1, tile_y), CUSTOS[right]))
    if left in CUSTOS:
        vizinhos.append(((tile_x - 1, tile_y), CUSTOS[left]))
    if down in CUSTOS:
        vizinhos.append(((tile_x, tile_y + 1), CUSTOS[down]))
    if up in CUSTOS:
            vizinhos.append(((tile_x, tile_y - 1), CUSTOS[up]))

    for vizinho, custo_terreno in vizinhos:
        if vizinho in closed:
            continue

        # Única mudança importante para os terrenos:
        # antes era g_score[tile] + 1; agora usamos o custo do tile.
        novo_g = g_score[tile] + custo_terreno

        if vizinho not in g_score or novo_g < g_score[vizinho]:
            came_from[vizinho] = tile
            g_score[vizinho] = novo_g

            # A menor movimentação possível ainda custa 1 (grama), então
            # a distância de Manhattan continua sendo uma boa heurística.
            h = abs(end_x - vizinho[0]) + abs(end_y - vizinho[1])
            f = novo_g + h
            heapq.heappush(open, (f, vizinho))


def find_path(start, end, mapa):
    came_from = {}
    g_score = {start: 0}

    # Open Set como Fila de Prioridade (Min-Heap)
    open = []
    closed = set()

    h_inicial = abs(end[0] - start[0]) + abs(end[1] - start[1])
    heapq.heappush(open, (h_inicial, start))

    # Loop principal do A*
    while len(open) > 0:
        _, atual = heapq.heappop(open)

        # Uma posição pode entrar mais de uma vez no heap.
        if atual in closed:
            continue

        if atual == end:
            break

        closed.add(atual)
        check_neighbours(atual, end, came_from, g_score, open, closed, mapa)

    # Reconstrução do caminho, igual ao algoritmo inicial.
    if end not in came_from and start != end:
        return None

    caminho = [end]
    passo = end
    while passo in came_from:
        passo = came_from[passo]
        caminho.append(passo)

    caminho.reverse()
    return caminho


def calcular_custo(caminho, mapa):
    """Soma os custos para a interface exibir o resultado."""
    if caminho is None:
        return None
    return sum(CUSTOS[mapa[y][x]] for x, y in caminho[1:])


# Mantém também o nome em português usado pela simulação.
def encontrar_caminho(mapa, inicio, destino):
    caminho = find_path(inicio, destino, mapa)
    return caminho, calcular_custo(caminho, mapa)


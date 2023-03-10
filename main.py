import heapq
# ! dentro do algoritmo Astar, a estação 0 é a 1, a 1 é a 2, a 2 é a 3 etc.

direct_distances = []
real_distances = []
number_of_stations = 14

# ? cores das linhas de cada estação
line_colors = [["azul"], ["azul", "amarela"], ["azul", "vermelha"], ["azul", "verde"], ["azul", "amarela"],
["azul"], ["amarela"], ["amarela", "verde"], ["amarela", "vermelha"], ["amarela"], ["vermelha"],
["verde"], ["vermelha", "verde"], ["verde"]]

def checkInputValidity(start, end):
    start_color = start[-1]
    end_color = end[-1]

    if not (start[1]).isnumeric() or not (end[1]).isnumeric():
        print("por favor indicar a estação da seguinte maneira: 'estação <número> na linha <cor>'")
        print('ex: estação 1 na linha azul')
        return False

    start = int(start[1]) - 1
    end = int(end[1]) - 1

    if start < 0 or start > number_of_stations - 1:
        print('Número da estação inicial não existente')
        return False
    if start_color not in line_colors[start]:
        print('A estação inicial não possui essa linha')
        return False
    if end < 0 or end > number_of_stations - 1:
        print('Número da estação de destino não existente')
        return False
    if end_color not in line_colors[end]:
        print('A estação de destino não possui essa linha')
        return False

    return True

def zero_or_one(node, node_color):
    return line_colors[node].index(node_color)

def define_color(v: int, u: int, u_color: str)-> str:
    """
    Define a cor da linha atual de v, de acordo com a cor da linha atual de u, e as cores das possíveis linhas de v

    Parâmetros:
    v (int): a estação vizinha.
    u (int): a estação atual.
    u_color: cor da linha atual de u

    Retorna:
    str: cor da linha atual de v
    """
    if u_color in line_colors[v]:
        return u_color
    else:
        for c in line_colors[u]:
            if c != u_color:
                return c

def heap_update(heap: list, item:tuple):
    nodesColors = [(x[1], x[2]) for x in heap]
    (f, node, color) = item
    if (node, color) not in nodesColors:
        heapq.heappush(heap, item)
    else:
        for i in range(len(heap)):
            if heap[i][1] == node and heap[i][2] == color:
                if f < heap[i][0]:
                    heap[i] = item
                    heap = sorted(heap)
                break
    
def get_distances(): #cria matrizes de distancia
    direct_text = open("paris-direct.txt", 'r')
    for line in direct_text:
        row = line.split(',')
        row = list(map(float, row)) #transforma em lista de floats

        direct_distances.append(row)
    
    connect_text = open("paris-connect.txt", 'r')
    for line in connect_text:
        row = line.split(',')
        row = list(map(float, row)) #transforma em lista de floats
        
        real_distances.append(row)

def get_g(start, goal): # funcao para calcular g(n) => tempo em minutos sem contar baldiação
    node1 = start if start < goal else goal
    node2 = goal if start < goal else start

    g = real_distances[node1][node2] 
    return g*2 # como o trem vai a 30km/h a distância g em km * 2 é igual ao tempo em minutos

def get_h(start, goal): #funcao para calcular h(n) => tempo em minutos sem contar baldiação
    node1 = start if start < goal else goal
    node2 = goal if start < goal else start

    h = direct_distances[node1][node2]
    return h*2 # como o trem vai a 30km/h a distância h em km * 2 é igual ao tempo em minutos

def getAvailableCities(current): #retorna todas as cidades conectadas a cidade atual
    s1 = current
    availableCities = []
    for i in range(number_of_stations):
        if real_distances[s1][i] != 0.0:
            city = i
            availableCities.append(city)
        if real_distances[i][s1] != 0.0:
            city = i
            availableCities.append(city)
    return availableCities

def find_path(P: list, end: int, end_color) -> list: 
    """
    Encontra o caminho de uma estação a outra, considerando as baldeações.

    Parâmetros:
    P: (pai, cor da estação atual)[]
    end: estação final

    Retorna:
    path: [(1ª estação, cor da linha), (2ª estação, cor da linha), ...].
    """
    curNode = end
    curColor = end_color
    path = []
    
    while curNode != -1:
        path.append((curNode+1, curColor))

        fatherNode, fatherColor = P[zero_or_one(curNode, curColor)][curNode]

        if fatherColor != curColor and fatherNode != curNode and fatherNode != -1: # se houve baldeação
            path.append((fatherNode+1, curColor))  # adicionar baldeação
        
        curNode = fatherNode
        curColor = fatherColor
        
    return path[::-1]

def aStar(start: str, end: str) -> tuple:
    """
    Algoritmo A* para encontrar o caminho mais rápido entre duas estações.

    Parâmetros:
    start: estação inicial no formato "estação {nº da estação} na linha {cor}"
    end: estação final no formato "estação {nº da estação} na linha {cor}"

    Retorna:
    uma dupla no formato
    (
        P: (pai, cor da estação atual)[],
        G: distância do start até cada estação até o momento[]
        )
    """
    # ? processando o input para extrair nº da estação-1 e cor da linha para as estações inicial e final
    start = start.split(' ')
    end = end.split(' ')
    isInputValid = checkInputValidity(start, end)
    if not isInputValid:
        return
    start_color = start[-1]
    end_color = end[-1]
    start = int(start[1]) - 1
    end = int(end[1]) - 1

    # ? inicializando listas
    G = [[99999] * number_of_stations, [99999] *number_of_stations] # guarda a distância do start até cada estação até o momento
    P = [[(-1, None)] * number_of_stations, [(-1, None)] *number_of_stations] # guarda (estação anterior, cor da estação atual)

    # ? inicializando o valor de start na lista
    G[zero_or_one(start, start_color)][start] = 0

    # ? inicializando a heap
    heap = []
    heapq.heappush(heap, (0, start, start_color))

    iteration = 0

    while True:
        border = [(f, f"E{u+1}", u_color) for (f, u, u_color) in heap]
        border.sort(key=lambda x: x[0])

        (f, u, u_color) = heapq.heappop(heap) # escolhe a estação com menor f(n) e a remove da heap
        if iteration > 0:
            print(f"Fronteira heurística: {border}\n")
        iteration += 1
        print(f"Estação atual: {u+1} na linha {u_color}")

        new_root = 0 if len(heap) == 0 else heap[0][0]
        if (u == end):
            if u_color == end_color or (f+4) < new_root: # ou vc já chegou na estação com a cor certa, ou o tempo pra baldear ainda é curto o suficiente pra essa ser a melhor opção
                if u_color != end_color:
                    P[zero_or_one(end, end_color)][end] = (end, u_color)
                    G[zero_or_one(end, end_color)][end] = G[zero_or_one(end, u_color)][end] + 4   #adiciona o tempo da baldeação (4 min)
                
                path = find_path(P, end, end_color)
                
                print(f"Chegamos na estação {end+1} na linha {end_color}!")
                print(f"Custo: {G[zero_or_one(end, end_color)][end]} minutos")
                print("Caminho: ", path)

                return(P, G)
            else:
                if G[zero_or_one(end, u_color)][end] + 4 < G[zero_or_one(end, end_color)][end]: # se valer a pena a baldeação:
                    P[zero_or_one(end, end_color)][end] = (end, u_color)
                    G[zero_or_one(end, end_color)][end] = G[zero_or_one(end, u_color)][end] + 4
                    heap_update(heap, (f+4, u, end_color)) # atualiza o tempo para chegar no nó final e o adiciona à heap - # ! isso porque você só encontrou o caminho se o f(h) até o nó final for o menor possível (se for o primeiro elemento da heap)
                continue

        neighboring_nodes = getAvailableCities(u)
        
        for v in neighboring_nodes:
            g = get_g(u, v)
            transhipment = 4 if u_color not in line_colors[v] else 0 # decide se vai ter baldeação ou não => se sim, o valor será 4, se não, 0
            v_color = define_color(v, u, u_color)

            if G[zero_or_one(u, u_color)][u] + g + transhipment < G[zero_or_one(v, v_color)][v]:

                P[zero_or_one(v, v_color)][v] = (u, u_color) # (pai, cor do pai)
                G[zero_or_one(v, v_color)][v] = G[zero_or_one(u, u_color)][u] + g + transhipment
                f = G[zero_or_one(v, v_color)][v] + get_h(v, end)

                heap_update(heap, (f, v, v_color))

def main():
    get_distances()
    print("indique as estações da seguinte maneira: 'estação <número> na linha <cor>'")
    print('ex: estação 1 na linha azul')
    start = input("\nestação inicial: ")
    end = input("estação final: ")
    print(f"\nda {start} à {end}".upper())
    aStar(start, end)

if __name__ == "__main__":
    main()
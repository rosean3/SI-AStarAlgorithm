from heap import Heap
# ! dentro do algoritmo Astar, a estação 0 é a 1, a 1 é a 2, a 2 é a 3 etc.

direct_distances = []
real_distances = []
number_of_stations = 14

# ? cores das linhas de cada estação
line_colors = [["azul"], ["azul", "amarelo"], ["azul", "vermelho"], ["azul", "verde"], ["azul", "amarelo"],
["azul"], ["amarelo"], ["amarelo", "verde"], ["amarelo", "vermelho"], ["amarelo"], ["vermelho"],
["verde"], ["vermelho", "verde"], ["verde"]]



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

# def heap_update(heap: list, item:tuple):
#     nodes = [x[1] for x in heap]
#     (f, node, color) = item
#     if node not in nodes:
#         heap.append(item)
#         heap.sort(key=lambda x: x[0])
#     else:
#         for i in range(len(heap)):
#             if heap[i][1] == node:
#                 if f < heap[i][0]:
#                     heap[i] = item
#                     heap.sort(key=lambda x: x[0])
#                 break
    
# def heap_insert(heap: list, item: tuple):
#     heap.append(item)
#     heap.sort(key=lambda x: x[0])
    
def makearray(): #cria matrizes de distancia
    file1 = open("paris-direct.txt", 'r')
    for string in file1:
        row = string.split(',')
        for i in range(len(row)):
            row[i] = float(row[i])
        direct_distances.append(row)        
    file2 = open("paris-connect.txt", 'r')
    for string in file2:
        row = string.split(',')
        for i in range(len(row)):
            row[i] = float(row[i])
        real_distances.append(row)

def get_g(start, goal): # funcao para calcular g(n) => tempo em minutos sem contar baldiação
    s1 = start.split('E')
    s1 = int(s1[1]) - 1
    s2 = goal.split('E')
    s2 = int(s2[1]) - 1
    if s1 > s2:
        s1, s2 = s2, s1
    g = real_distances[s1][s2] 
    return g*2 # como o trem vai a 30km/h a distância g em km * 2 é igual ao tempo em minutos

def get_h(start, goal): #funcao para calcular h(n) => tempo em minutos sem contar baldiação
    s1 = start.split('E')
    s1 = int(s1[1]) - 1
    s2 = goal.split('E')
    s2 = int(s2[1]) - 1
    if s1 > s2:
        s1, s2 = s2, s1
    h = direct_distances[s1][s2]
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

def find_path(P: list, end: int) -> list: 
    """
    Encontra o caminho de uma estação a outra, considerando as baldeações.

    Parâmetros:
    P: (pai, cor da estação atual)[]
    end: estação final

    Retorna:
    path: [(1ª estação, cor da linha), (2ª estação, cor da linha), ...].
    """
    path = []
    aux = end
    color = P[aux][1] #cor da estação atual
    
    while aux != -1:
        path.append((aux+1, color)) #estação atual, cor da estação atual
        
        aux = P[aux][0] #estação anterior
        prevColor = color
        color = P[aux][1] #cor da estação anterior

        if(prevColor != color and aux != -1 ):  #repete a estação e muda a cor caso tenha baldeação
            path.append((aux+1, prevColor)) #estação anterior, cor da estação atual
        
        
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
    start_color = start[-1]
    start = int(start[1]) - 1
    end = end.split(' ')
    end_color = end[-1]
    end = int(end[1]) - 1

    # ? inicializando listas
    G = [99999] * number_of_stations # guarda a distância do start até cada estação até o momento
    F = [99999] * number_of_stations # guarda f = g(n) + h(n) para cada estação até o momento
    P = [(-1, None)] * number_of_stations # guarda (estação anterior, cor da estação atual)

    # ? inicializando os valores de start nas listas
    P[start]= (-1, start_color)
    G[start] = 0
    F[start] = 0

    # ? inicializando a heap
    heap = Heap(14)
    #heap_insert(heap, (F[start], start, start_color))
    heap.heap_add(F[start], start, start_color)

    for i in range(number_of_stations):
        (f, u, u_color) = heap.heap_extract() # escolhe a estação com menor f(n) e a remove da heap
        if (u == end):
            if u_color == end_color or (f+4) < heap.heap[0].distance: # ou vc já chegou na estação com a cor certa, ou o tempo pra baldear ainda é curto o suficiente pra essa ser a melhor opção
                
                path = find_path(P, end)

                if u_color != end_color:
                    path.append((end+1, end_color))     #adiciona mais uma baldeação no caminho
                    G[end] += 4                        #adiciona o tempo da baldeação (4 min)
                
                print(f"G: {G[end]} minutos")
                print(path)

                return(P, G)
            else:
                heap.heap_add(f+4, u, end_color)
                #heap_update(heap, (f+4, u, end_color))  # atualiza o tempo para chegar no nó final e o adiciona à heap - # ! isso porque você só encontrou o caminho se o f(h) até o nó final for o menor possível (se for o primeiro elemento da heap)
                continue

        neighboring_nodes = getAvailableCities(u)
        
        for v in neighboring_nodes:
            g = get_g("E" + str(u + 1), "E" + str(v + 1))
            transhipment = 4 if u_color not in line_colors[v] else 0 # decide se vai ter baldeação ou não => se sim, o valor será 4, se não, 0

            if G[u] + g + transhipment < G[v]:
                v_color = define_color(v, u, u_color)

                P[v] = (u, v_color) # (pai, cor atual)
                G[v] = G[u] + g + transhipment
                F[v] = G[v] + get_h("E" + str(v + 1), "E" + str(end+1))
             
                #heap_update(heap, (F[v], v, v_color))
                heap.heap_add(F[v], v, v_color)

makearray()
aStar("estação 9 na linha amarelo", "estação 5 na linha amarelo")


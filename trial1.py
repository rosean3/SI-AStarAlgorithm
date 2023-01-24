paris = []
parisConnect = []

line_colors = [["blue"], ["blue", "yellow"], ["blue", "red"], ["blue", "green"], ["blue", "yellow"],
["blue"], ["yellow"], ["yellow", "green"], ["yellow", "red"], ["yellow"], ["red"],
["green"], ["red", "green"], ["green"]]

def heap_insert(heap: list, item: tuple):
    heap.append(item)
    heap.sort(key=lambda x: x[0])

def define_color(v, u, color):
    if color in line_colors[v]:
        return color
    else:
        for c in line_colors[u]:
            if c != color:
                return c

def heap_update(heap: list, item:tuple):
    nodes = [x[1] for x in heap]
    (f, node, color) = item
    if node not in nodes:
        heap.append(item)
        heap.sort(key=lambda x: x[0])
    else:
        for i in range(len(heap)):
            if heap[i][1] == node:
                if f < heap[i][0]:
                    heap[i] = item
                    heap.sort(key=lambda x: x[0])
                break
    

def makearray(): #cria matrizes de distancia
    file1 = open("paris-direct.txt", 'r')
    for string in file1:
        row = string.split(',')
        for i in range(len(row)):
            row[i] = float(row[i])
        paris.append(row)        
    file2 = open("paris-connect.txt", 'r')
    for string in file2:
        row = string.split(',')
        for i in range(len(row)):
            row[i] = float(row[i])
        parisConnect.append(row)

def get_g(start, goal): # funcao para calcular g(n) => tempo em minutos para sem contar baldiação
    s1 = start.split('E')
    s1 = int(s1[1]) - 1
    s2 = goal.split('E')
    s2 = int(s2[1]) - 1
    if s1 > s2:
        s1, s2 = s2, s1
    g = parisConnect[s1][s2] 
    return g*2

def get_h(start, goal): #funcao para calcular h(n) => tempo em minutos para sem contar baldiação
    s1 = start.split('E')
    s1 = int(s1[1]) - 1
    s2 = goal.split('E')
    s2 = int(s2[1]) - 1
    if s1 > s2:
        s1, s2 = s2, s1
    h = paris[s1][s2]
    return h*2

def getAvailableCities(current): #retorna todas as cidades conectadas a cidade atual
    s1 = current
    availableCities = []
    for i in range(14):
        if parisConnect[s1][i] != 0.0:
            city = i
            availableCities.append(city)
        if parisConnect[i][s1] != 0.0:
            city = i
            availableCities.append(city)
    return availableCities

def find_path(P, end): #retorna o caminho
    path = []
    aux = end
    color = P[aux][1]
    
    while aux != -1:
        path.append((aux+1, color))
        
        aux = P[aux][0]
        prevColor = color
        color = P[aux][1]

        if(prevColor != color and aux != -1 ):  #repete a estação e muda a cor caso tenha baldeação
            path.append((aux+1, prevColor))
        
        
    return path[::-1]

def aStar(start, end):
    start = start.split(' ')
    start_color = start[-1]
    start = int(start[1]) - 1
    end = end.split(' ')
    end_color = end[-1]
    end = int(end[1]) - 1

    G = [99999] * 14
    F = [99999] * 14
    P = [(-1, None)] * 14

    P[start]= (-1, start_color)
    G[start] = 0
    F[start] = 0
    heap = []
    heap_insert(heap, (F[start], start, start_color))

    for i in range(14):
        (f, u, color) = heap.pop(0)
        if (u == end):
            if color == end_color or (f+4) < heap[0][0]: # ou vc já chegou na estação com a cor certa, ou o tempo pra baldear ainda é curto o suficiente pra essa ser a melhor opção
                
                path = find_path(P, end)

                if color != end_color:
                    path.append((end+1, end_color))     #adiciona mais uma baldeação no caminho
                    G[end] += 4
                    print("yes")
                
                print("G: ", G[end])
                print(path)

                return(P, G)
            else:
                heap_update(heap, (f+4, u, end_color))
                continue

        e = getAvailableCities(u)
        for v in e:
            g = get_g("E" + str(u + 1), "E" + str(v + 1))
            transhipment = 4 if color not in line_colors[v] else 0

            if G[u] + g + transhipment < G[v]:
                v_color = define_color(v, u, color)

                P[v] = (u, v_color)
                G[v] = G[u] + g + transhipment
                F[v] = G[v] + get_h("E" + str(v + 1), "E" + str(end+1))
             
                heap_update(heap, (F[v], v, v_color))

makearray()
aStar("estação 9 na linha yellow", "estação 5 na linha yellow")
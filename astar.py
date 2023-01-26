
class Graph:

    def __init__(self, lista_adjacencia):
        self.lista_adjacencia = lista_adjacencia
    
    def get_vizinhos(self, v):
        return self.lista_adjacencia[v]
    
    def h(self, n):
        H = {
            'A': 1,
            'B': 1,
            'C': 1,
            'D': 1
        }

        return H[n]
    
    def a_star(self, start, stop):

        open_list = set([start])
        closed_list = set([])

        g = {}

        g[start] = 0

        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            for v in open_list:
                if n == None or g[v] + self.h(v) < g[n] + self.h(n):
                    n = v
            
            if n == None:
                print("Nao existe caminho!")
                return None

            if n == stop:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            for (m, peso) in self.get_vizinhos(n):
                
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + peso
                
                else:
                    if g[m] > g[n] + peso:
                        gm = g[n] + peso
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)


            open_list.remove(n)
            closed_list.add(n)
        
        print("Nao existe caminho!")
        return None

adjacency_list = {
    'A': [('B', 1), ('C', 3), ('D', 7)],
    'B': [('D', 5)],
    'C': [('D', 12)]
}
graph1 = Graph(adjacency_list)
graph1.a_star('A', 'D')
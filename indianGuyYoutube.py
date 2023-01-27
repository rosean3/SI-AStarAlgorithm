
"""
	Perform A* Traversal and find the optimal path to reach goal
"""

print("A* Implementation in Python:\n")



def f(g, h, n):
	return g[n] + h[n]

#remove front, add to visited
def update(to_remove, to_add, m):
	to_remove.remove(m)
	to_add.append(m)


def a_star_algo(cost, heuristic, start, goals):
	path = [] #optimal path
	pathSet = []

	## closed list
	closed_list = [] # ex: S, A, ...

	## open list
	open_list = [start]

	path_len = {}
	path_len[start] = 0

	#for back-tracking:
	parent_node = {}
	parent_node[start]=start

	while len(open_list) > 0:
		#get node with least f
		node = None
		for n in open_list:
			if node == None or f(path_len,  heuristic, n) < f(path_len, heuristic, node):
				node = n 
		
		if node == None: #path does not exist
			break

		if node in goals: #[6, 7, 10]
			f_n = f(path_len, heuristic, node)
			reconstruct = []

			aux = node
			while parent_node[aux] != aux: # [(S, 9, S), (A, 6, S)]
				reconstruct.append(aux) #[ A, S]
				aux = parent_node[aux]
			
			reconstruct.append(start)
			reconstruct.reverse()

			pathSet.append((reconstruct, f_n))

			
			update(open_list, closed_list, node)
			continue
		

		#explore the current node
		path_cost = cost[node] #[0, 0, 5, 9, -1, 6, -1, -1, -1, -1, -1]
			
		for adj_node in range(0, len(path_cost)): 
			weight = path_cost[adj_node]

			if weight > 0:
				if adj_node not in open_list and adj_node not in closed_list:
					open_list.append(adj_node)
					parent_node[adj_node] = node
					path_len[adj_node] = path_len[node] + weight

				else: 
					if path_len[adj_node] > path_len[node] + weight:
						path_len[adj_node] = path_len[node] + weight
						parent_node[adj_node] = node

						if adj_node in closed_list:
							update(closed_list, open_list, adj_node)

		update(open_list, closed_list, node)

	if len(pathSet) > 0:
		pathSet = sorted(pathSet, key=lambda x: x[1]) #[([1,5,7], 8), ([1,2,3], 10)]
		path = pathSet[0][0] 
		
	return path


#driver code
'''
#Sample inputs 1: 

give_cost = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 5, 9, -1, 6, -1, -1, -1, -1, -1],
			[0, -1, 0, 3, -1, -1, 9, -1, -1, -1, -1],
			[0, -1, 2, 0, 1, -1, -1, -1, -1, -1, -1],
			[0, 6, -1, -1, 0, -1, -1, 5, 7, -1, -1],
			[0, -1, -1, -1, 2, 0, -1, -1, -1, 2, -1],
			[0, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1],
			[0, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1],
			[0, -1, -1, -1, -1, 2, -1, -1, 0, -1, 8],
			[0, -1, -1, -1, -1, -1, -1, -1, -1, 0, 7],
			[0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0]]

start=1
give_goals = [6, 7, 10]
heuristic = [0, 5, 7, 3, 4, 6, 0, 0, 6, 5, 0]
'''
#Sample Inputs 2

give_cost = [
[0,1,2.1],
[1,0,1],
[3.1,1,0]
]
start=0
give_goals=[2,3]

heuristic = [1,2.1,0]

getPath = a_star_algo(give_cost, heuristic, start, give_goals)

print(getPath)
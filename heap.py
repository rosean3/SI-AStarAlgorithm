class Heap_node:
    
     def __init__(self, distance = 99999, station = None, color = None):
         self.distance = distance
         self.station = station
         self.color = color

class Heap:
    
    def __init__(self, size):
        self.heap = [Heap_node()] * size
        self.heap_capacity = size
        self.heap_size = 0
        self.heap_presence = [-1] * size

    def heap_add(self, d, s, c):

        if self.heap_presence[s] == -1:
            self.heap[self.heap_size] = Heap_node(d, s, c)
            self.heap_presence[s] = self.heap_size
            self.heap_size += 1
            self.bubble_up(self.heap_size - 1)
        else:
            if d < self.heap[self.heap_presence[s]].distance:
                self.heap[self.heap_presence[s]] = Heap_node(d, s, c)
                self.bubble_up(self.heap_presence[s])

    def heap_extract(self):
        
        if self.heap_size > 0:
            node = self.heap[0]
            self.heap_size -= 1
            self.heap_swap(0, self.heap_size)
            self.heap_presence[self.heap[self.heap_size].station] = -1
            self.heap[self.heap_size] = Heap_node()
            self.bubble_down(0)
            return (node.distance, node.station, node.color)
        
    
    def bubble_up(self, i):
        if i != 0 and self.heap[i].distance < self.heap[self.parent(i)].distance:
            self.heap_swap(i, self.parent(i))
            return self.bubble_up(self.parent(i))
        

    def bubble_down(self, i):
        m = i
        l = self.child_left(i)
        r = self.child_right(i)

        if l < self.heap_size and self.heap[m].distance > self.heap[l].distance:
            m = l

        if r < self.heap_size and self.heap[m].distance > self.heap[r].distance:
            m = r

        if i != m:
            self.heap_swap(i, m)
            return self.bubble_down(m)

    def heap_swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

        self.heap_presence[self.heap[i].station], self.heap_presence[self.heap[j].station] = self.heap_presence[self.heap[j].station], self.heap_presence[self.heap[i].station]
        

    def parent(self, idx):
        return (idx - 1) // 2

    def child_left(self, idx):
        return 2 * idx + 1
    
    def child_right(self, idx):
        return 2 * idx + 2
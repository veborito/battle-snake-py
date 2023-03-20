from queue import PriorityQueue
import math
import time

matrice = [
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', '#', '#', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', 'O', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#', '#', 'V'],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '$', ' ', ' '],
[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '$', '$', ' '],
[' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ']
]

class Node:
    def __init__(self, row, col, state):
        self.row = row
        self.col = col # j'ai besoin qu'il soit deja correctement modifié
        self.neighbors = []
        self.state = state
        
    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.state == 'X'
    
    def is_open(self):
        return self.state == '1'
    
    def is_barrier(self):
        return self.state == '$' or self.state == 'B' or self.state == 'V' or self.state == '#'
    
    def is_start(self):
        return self.state == 'B'
    
    def is_end(self):
        return self.state == 'O'
    
    def make_closed(self):
        self.state = 'X'
    
    def make_open(self):
        self.state = '1'
    
    def make_path(self):
        self.state = '+'
    
    def make_start(self):
        self.state = 'B'
    
    def make_end(self):
        self.state = 'O'
    
    def update_neighbors(self, graph):
        self.neighbors = []
        if self.row < len(graph) - 1 and not graph[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(graph[self.row + 1][self.col])

        if self.row > 0 and not graph[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(graph[self.row - 1][self.col])

        if self.col < len(graph[0]) - 1 and not graph[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(graph[self.row][self.col + 1])

        if self.col > 0 and not graph[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(graph[self.row][self.col - 1])
    
    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    
    return abs(x1 - x2) + abs(y1 - y2)

def make_graph(matrice):
    graph = []
    for i in range(len(matrice)):
        graph.append([])
        for j in range(len(matrice[0])):
            node = Node(i, j, matrice[i][j])
            graph[i].append(node)
    return graph

def path(came_from, current):
    coord_list = [current.get_pos()]
    while current in came_from:
        current = came_from[current]
        coord_list.append(current.get_pos())
        current.make_path()
    return coord_list

def a_star(graph, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, 0, start))
    came_from = {} # wich node came from where 
    g_score = {node: float("inf") for row in graph for node in row} # number of step beetwen the start and the node
    g_score[start] = 0
    f_score = {node: float("inf") for row in graph for node in row} # manhattan distant or L distance for node to the end 
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start} # check what's inside priority queue
    while not open_set.empty():
        current = open_set.get()[2] # current node
        open_set_hash.remove(current)
        
        if current == end:  
            end.make_end()
            return came_from
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        if current != start:
            current.make_closed()
        
    return False

def start_node(graph):
    for row in graph:
        for node in row:
            if node.is_start():
                return node
    return False

def end_node(graph):
    for row in graph:
        for node in row:
            if node.is_end():
                return node
    return False   

if __name__ == "__main__":
	graph = make_graph(matrice)
	start = start_node(graph)
	end = end_node(graph)
	for row in graph:
		for node in row:
			node.update_neighbors(graph)

	a_star_res = a_star(graph, start, end)
	path_list = path(a_star_res, end)
	start.make_start()
	n_matrice = [[ node.state for node in row] for row in graph]
	for row in n_matrice:
		print (row)
	print(path_list)
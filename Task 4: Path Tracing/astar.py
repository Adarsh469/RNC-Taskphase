import numpy as np
import math
import cv2 as cv
import heapq
import datetime

image = cv.imread("test_map.png", cv.IMREAD_GRAYSCALE)
_, grid = cv.threshold(image, 128, 255, cv.THRESH_BINARY)

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = float('inf')
        self.h = 0
        self.f = float('inf')

    def compare_parent(self, p: 'Node', goal_pos):   #checks if the path we get from the node p gives better cost than the initital best gcost
        tentative_g = p.g + 1
        if tentative_g < self.g:      #update path if new path found is better than previous path needs few upgrades
            self.parent = p            #if new path found change the parent and update other values
            self.g = tentative_g
            self.h = math.sqrt((self.position[0] - goal_pos[0]) ** 2 + 
                               (self.position[1] - goal_pos[1]) ** 2)
            self.f = self.g + self.h

    def __lt__(self, other):
        return self.f < other.f      #compares the nodes in the priority queue based on fcost

class AStar:
    def __init__(self, grid, start_node, end_node):
        self.grid = grid
        self.start = Node(start_node)
        self.goal = Node(end_node)
        self.start.g = 0
        self.start.h = self.distance(self.start.position, self.goal.position)
        self.start.f = self.start.g + self.start.h

        self.open = []       #priority queue
        self.open_dict = {}     #used for easy access of priority queue stores only the coordinates of the nodes
        self.closed = set()     
        self.all_nodes = {}     #stores all nodes made till now to avoid duplication

        self.all_nodes[self.start.position] = self.start     #start node is pushed into heap  
        heapq.heappush(self.open, self.start)
        self.open_dict[self.start.position] = self.start

    def distance(self, a, b):
        return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)   #used euclidian distance for diagonal movement

    def get_neighbors(self, curr_node):
        neighbours = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]    #check all 8 directions
        for dx, dy in directions:
            x = curr_node.position[0] + dx
            y = curr_node.position[1] + dy
            if (0 <= x < self.grid.shape[0] and 
                0 <= y < self.grid.shape[1] and 
                self.grid[x, y] == 255 and 
                (x, y) not in self.closed):      #if its within the grid boundries and not in closed
                
                if (x, y) not in self.all_nodes:          #make new node if not in all nodes
                    self.all_nodes[(x, y)] = Node((x, y))
                neighbours.append(self.all_nodes[(x, y)])     #add node as one of the ni
        return neighbours

    def run(self, image_bgr):
        while self.open:
            current_node = heapq.heappop(self.open)        #heappop gives node with lowest f cost
            if current_node.position not in self.open_dict:       #remove the current node fomr the open list as it is checked now so add it to the closed list
                continue
            del self.open_dict[current_node.position]

            if current_node.position == self.goal.position:
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent 
                return path[::-1]

            self.closed.add(current_node.position)
            if self.grid[current_node.position] == 255:
                cv.circle(image_bgr, (current_node.position[1], current_node.position[0]), 1, (255, 0, 0), -1)

            for neighbor in self.get_neighbors(current_node):
                if neighbor.position in self.closed:
                    continue
                old_g = neighbor.g
                neighbor.compare_parent(current_node, self.goal.position)
                if (neighbor.position not in self.open_dict or neighbor.g < old_g):
                    heapq.heappush(self.open, neighbor)
                    self.open_dict[neighbor.position] = neighbor
                    if self.grid[neighbor.position] == 255:
                        cv.circle(image_bgr, (neighbor.position[1], neighbor.position[0]), 1, (0, 255, 0), -1)
        return None

# Set up the start/goal and run
height, width = image.shape
start = (10, 10)
goal = (height - 10, width - 10)
image_bgr = cv.cvtColor(image, cv.COLOR_GRAY2BGR)

astar = AStar(grid, start, goal)
path = astar.run(image_bgr)

if path:
    for pos in path:
        if grid[pos] == 255:
            cv.circle(image_bgr, (pos[1], pos[0]), 1, (0, 0, 255), -1)
    print("Path found")
else:
    print("No path found")

# Save and show result
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_resized = cv.resize(image_bgr, (1000, 1000), interpolation=cv.INTER_NEAREST)
cv.imwrite(f"output_map_{timestamp}.png", output_resized)

cv.namedWindow("Path", cv.WINDOW_NORMAL)
cv.resizeWindow("Path", 1000, 1000)
cv.imshow("Path", output_resized)
cv.waitKey(0)
cv.destroyAllWindows()

import numpy as np
import math
import cv2 as cv
import heapq
import datetime

image = cv.imread("test_map.png", cv.IMREAD_GRAYSCALE)
_, grid = cv.threshold(image, 128, 255, cv.THRESH_BINARY)

class Node:
    def __init__(self, position, parent):
        self.position = position
        self.parent = parent
        self.g = float('inf')
    
    def __lt__(self, other):
        return self.g<other.g 

class Dijkstra:
    def __init__(self, grid, start_node,end_node = None):
        self.grid = grid
        self.start = Node(start_node, None)
        self.start.g = 0
        self.goal = Node(end_node, None) if end_node else None
        self.open = []  #heap priority queue which stores the nodes yet to be visited
        self.open_dict = {} #used to check if node is in open list faster
        self.closed = set()
        self.paths = {}

        heapq.heappush(self.open, self.start)  #used to push the node with least gcost to the top of the heap
        self.open_dict[self.start.position] = self.start #stores the nodes with the key being its position for faster access
        
    def get_neighbours(self, curr_node):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            x = curr_node.position[0] + dx
            y = curr_node.position[1] + dy
            if (0 <= x < self.grid.shape[0] and 0 <= y < self.grid.shape[1] and self.grid[x, y] == 255 and (x, y) not in self.closed):
                neighbors.append(Node((x,y), curr_node))
        return neighbors
    
    def run(self, image_bgr):
        while self.open:
            curr_node = heapq.heappop(self.open)
            #safety check cuz multiple same coordinates can sneak into heap while finding gcost
            if(curr_node.position not in self.open_dict):
                continue
            del self.open_dict[curr_node.position] #position visited now so remove from to be processed and add to closed if already removed then continue

            self.closed.add(curr_node.position) #marks node as already visited
            self.paths[curr_node.position]=curr_node  #store the shortest path to the node we marked as visited

            if self.grid[curr_node.position] == 255:
                cv.circle(image_bgr, (curr_node.position[1], curr_node.position[0]), 1, (255, 0, 0), -1) #mark visisted node blue in output BGR
            
            #stop only if goal is provided and return the path to goal
            if self.goal and curr_node.position == self.goal.position: 
                path = []
                while curr_node:
                    path.append(curr_node.position)
                    curr_node = curr_node.parent
                return path[::-1]
            
            for neighbor in self.get_neighbours(curr_node):
                if neighbor.position in self.closed:
                    continue
                temp_g = curr_node.g + 1

                #if new path is found upfate the parent node and change the gcost and add in the open list
                if (neighbor.position not in self.open_dict or temp_g<self.open_dict[neighbor.position].g):
                    neighbor.g = temp_g
                    neighbor.parent = curr_node
                    heapq.heappush(self.open, neighbor)
                    self.open_dict[neighbor.position] = neighbor
                    if self.grid[neighbor.position] == 255:
                        cv.circle(image_bgr, (neighbor.position[1], neighbor.position[0]), 1, (0, 255, 0), -1) #draw the neighbour as green
        
        if self.goal:
            return None
        else:
            return self.paths
    
height, width = image.shape
start = (10, 10)
goal = (height - 10, width - 10)  

image_bgr = cv.cvtColor(image, cv.COLOR_GRAY2BGR)

dijkstra = Dijkstra(grid, start, goal)
path_or_dict = dijkstra.run(image_bgr)

if isinstance(path_or_dict, list):
    # Goal-based
    for pos in path_or_dict:
        if grid[pos] == 255:
            cv.circle(image_bgr, (pos[1], pos[0]), 1, (0, 0, 255), -1)
    print("Path to goal found")
elif isinstance(path_or_dict, dict):
    # No goal – show all reachable nodes
    print(f"{len(path_or_dict)} reachable nodes found from start.")
    for pos in path_or_dict:
        if grid[pos] == 255:
            cv.circle(image_bgr, (pos[1], pos[0]), 1, (0, 255, 255), -1)
else:
    print("No path found")

# Save and show output
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
output_resized = cv.resize(image_bgr, (1000, 1000), interpolation=cv.INTER_NEAREST)
cv.imwrite(f"output_map_{timestamp}.png", output_resized)

cv.namedWindow("Path", cv.WINDOW_NORMAL)
cv.resizeWindow("Path", 1000, 1000)
cv.imshow("Path", output_resized)
cv.waitKey(0)
cv.destroyAllWindows()

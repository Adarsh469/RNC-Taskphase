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

    def compare_parent(self, p: 'Node', goal_pos, movement_cost):
        tentative_g = p.g + movement_cost
        if tentative_g < self.g:
            self.parent = p
            self.g = tentative_g
            self.h = math.hypot(self.position[0] - goal_pos[0],
                                self.position[1] - goal_pos[1])
            self.f = self.g + self.h

    def __lt__(self, other):
        return self.f < other.f

class AStar:
    def __init__(self, grid, start_node, end_node):
        self.grid = grid
        self.start = Node(start_node)
        self.goal = Node(end_node)
        self.start.g = 0
        self.start.h = self.distance(self.start.position, self.goal.position)
        self.start.f = self.start.g + self.start.h

        self.open = []
        self.open_dict = {}
        self.closed = set()
        self.all_nodes = {}

        self.all_nodes[self.start.position] = self.start
        heapq.heappush(self.open, self.start)
        self.open_dict[self.start.position] = self.start

    def distance(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def is_walkable(self, x, y):
        return (0 <= x < self.grid.shape[0] and
                0 <= y < self.grid.shape[1] and
                self.grid[x, y] == 255)

    def get_neighbors(self, curr_node):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            x = curr_node.position[0] + dx
            y = curr_node.position[1] + dy

            # Prevent moving through corners
            if abs(dx) + abs(dy) == 2:
                if not (self.is_walkable(curr_node.position[0] + dx, curr_node.position[1]) and
                        self.is_walkable(curr_node.position[0], curr_node.position[1] + dy)):
                    continue

            if self.is_walkable(x, y) and (x, y) not in self.closed:
                if (x, y) not in self.all_nodes:
                    self.all_nodes[(x, y)] = Node((x, y))
                neighbors.append((self.all_nodes[(x, y)], math.hypot(dx, dy)))
        return neighbors

    def run(self, image_bgr):
        while self.open:
            current_node = heapq.heappop(self.open)
            if current_node.position not in self.open_dict:
                continue
            del self.open_dict[current_node.position]

            self.closed.add(current_node.position)

            # Mark closed node in BLUE (only if walkable)
            if self.grid[current_node.position] == 255:
                cv.circle(image_bgr, (current_node.position[1], current_node.position[0]), 1, (255, 0, 0), -1)

            if current_node.position == self.goal.position:
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]

            for neighbor_node, movement_cost in self.get_neighbors(current_node):
                if neighbor_node.position in self.closed:
                    continue
                old_g = neighbor_node.g
                neighbor_node.compare_parent(current_node, self.goal.position, movement_cost)
                if (neighbor_node.position not in self.open_dict or neighbor_node.g < old_g):
                    heapq.heappush(self.open, neighbor_node)
                    self.open_dict[neighbor_node.position] = neighbor_node

                    # Mark neighbor node in GREEN (only if walkable)
                    if self.grid[neighbor_node.position] == 255:
                        cv.circle(image_bgr, (neighbor_node.position[1], neighbor_node.position[0]), 1, (0, 255, 0), -1)
        return None

# Start/Goal and map setup
height, width = image.shape
start = (10, 10)
goal = (height - 10, width - 10)
image_bgr = cv.cvtColor(image, cv.COLOR_GRAY2BGR)

astar = AStar(grid, start, goal)
path = astar.run(image_bgr)

# Draw final path in RED
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

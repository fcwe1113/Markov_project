import heapq
import time

import Maze


class heuristic_markov:

    def __init__(self, maze: Maze.Maze):

        # variables
        self.execution_time = 0
        self.count = 0
        self.maze = maze
        self.start = (maze.startx, maze.starty)
        self.end = (maze.endx, maze.endy)
        self.parent_map = {} # dont do this is allowing revisiting nodes
        self.pathing = [self.start]

    def run(self):
        start_time = time.time_ns()
        self.count += 1
        queue = [(self.heuristic(self.start[0], self.start[1]), self.start)]
        self.parent_map[self.start] = None
        self.visited = []

        while queue:
            # get the closest node as current node
            current_dist, current_node = heapq.heappop(queue)
            self.visited.append(current_node)

            # yield data to the gui
            if current_node == self.end:
                yield current_node, f"goal reached after {self.count} iterations", time.time_ns() - start_time + self.execution_time
            else:
                yield current_node, f"current node: {current_node}   current distance to goal: {current_dist}", self.execution_time

            neighbors = self.maze.get_traversable_array(current_node[0], current_node[1])
            for y in range(len(neighbors)):
                if neighbors[y]:
                    if y == 0: # up
                        next_node = (current_node[0], current_node[1] - 1)
                    elif y == 1: # down
                        next_node = (current_node[0], current_node[1] + 1)
                    elif y == 2: # left
                        next_node = (current_node[0] - 1, current_node[1])
                    else: # right
                        next_node = (current_node[0] + 1, current_node[1])

                    if not next_node in self.visited or next_node == self.end:
                        if next_node not in self.parent_map:
                            self.parent_map[next_node] = current_node

                        if not neighbors in self.visited and not (self.heuristic(next_node[0], next_node[1]), next_node) in queue:
                            heapq.heappush(queue, (self.heuristic(next_node[0], next_node[1]), next_node))

        self.execution_time = time.time_ns() - start_time # todo double check this functionality

        # yield for GUI if no path found
        yield None, "Path not found", 0

    def heuristic(self, x, y):
        return abs(x - self.end[0]) + abs(y - self.end[1])

    def reconstruct_path(self):
        # This is called after the search finds the end uses the parent_map to work backwards from the end to the start
        path = []
        # Start from the end node
        current = self.end

        # If the end never added to the map no path found
        if self.end not in self.parent_map:
            return None

        # Loop backwards until start node, parent is None
        while current is not None:
            path.append(current)
            current = self.parent_map[current]

        # Reverse the path to be from start to end and return
        return path[::-1]
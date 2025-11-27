import heapq
import random
import time

import Maze


# add noise
    # apply randomness to each weight decision to eliminate deterministic behaviour
    # like a random number to add to each weight for the bot to be able to make bad decisions
# make the maze larger
# make a experience matrix for each maze bloc
    # as a kind of "learning" showing which bloc gave a more positive experience for reaching the goal
# current weight formula: given_weight + random_value(different for each option) + experience_value(if any)

# make it so every node visited but not used in final path get a weight penalty

class heuristic_markov:

    def __init__(self, maze: Maze.Maze, learning_offset = 5):

        # variables
        self.count = 0
        self.execution_time = 0
        self.maze = maze
        self.start = (maze.startx, maze.starty)
        self.end = (maze.endx, maze.endy)
        self.parent_map = {} # dont do this is allowing revisiting nodes
        self.pathing = [self.start]
        self.lowest_step = None
        self.max_random = 20 # for now keep it under 10
        self.queue = [(self.heuristic(self.start[0], self.start[1]), self.start)]
        self.visited = []
        self.experience = [[0 for x in range(self.maze.get_maze_x())] for y in range(maze.get_maze_y())]
        self.to_be_reset = False
        self.learning_offset = learning_offset

    def run(self):
        start_time = time.time_ns()
        self.parent_map[self.start] = None
        self.visited = []
        rng = random.Random()

        while self.queue:
            # get the closest node as current node
            current_dist, current_node = heapq.heappop(self.queue)
            self.count += 1
            self.visited.append(current_node)

            # get policies
            policies = []
            neighbors = self.maze.get_traversable_array(current_node[0], current_node[1])
            for y in range(len(neighbors)):
                dir = ""
                if neighbors[y]:
                    if y == 0:  # up
                        next_node = (current_node[0], current_node[1] - 1)
                        dir = "up"
                    elif y == 1:  # down
                        next_node = (current_node[0], current_node[1] + 1)
                        dir = "down"
                    elif y == 2:  # left
                        next_node = (current_node[0] - 1, current_node[1])
                        dir = "left"
                    else:  # right
                        next_node = (current_node[0] + 1, current_node[1])
                        dir = "right"

                    if not next_node in self.visited or next_node == self.end:
                        if next_node not in self.parent_map:
                            self.parent_map[next_node] = current_node

                        if not neighbors in self.visited and not (self.heuristic(next_node[0], next_node[1]), next_node) in self.queue:
                            random_float = rng.uniform(0, self.max_random)
                            # add more shit here when necessary
                            heapq.heappush(policies, (self.heuristic(next_node[0], next_node[1]) + random_float, [next_node, dir, self.heuristic(next_node[0], next_node[1]), self.experience[next_node[1]][next_node[0]], random_float]))

            # policies to string
            output = "Available policies (lowest weight will be picked):\n"
            if not policies:
                output += "No policies available\n"
            else:
                for i in range(len(policies)):
                    (_, policy) = policies[i]
                    output += f"node: {str(policy[0])}\tdirection: {policy[1]}\tdistance: {policy[2]} + random noise: {round(policy[4], 2)} + experience: {policy[3]} = sum: {round(policy[2] + policy[3] + policy[4], 2)}\n"

            # yield data to the gui
            if current_node == self.end:
                self.learn()
                yield current_node, f"goal reached after {self.count} iterations", time.time_ns() - start_time + self.execution_time, self.experience
                self.reset()
                policies = []
            else:
                yield current_node, f"current node: {current_node}   current distance to goal: {current_dist}\n{output}", self.execution_time, self.experience

            while policies:
                (weight, policy) = heapq.heappop(policies)
                skip = False
                for tup in self.queue:
                    if tup[1] == policy[0]:
                        skip = True
                        break

                if not skip:
                    heapq.heappush(self.queue, (weight, policy[0]))


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

    def reset(self):
        self.execution_time = 0
        self.count = 0
        self.parent_map = {self.start: None}  # dont do this is allowing revisiting nodes
        self.pathing = [self.start]
        self.visited = []
        self.queue = [(self.heuristic(self.start[0], self.start[1]), self.start)]
        self.to_be_reset = False

    def learn(self):
        pathing = self.reconstruct_path()
        if not self.lowest_step:
            self.lowest_step = len(pathing)
        else:
            if len(pathing) <= self.lowest_step:
                self.lowest_step = len(pathing)
                for tup in pathing:
                    self.experience[tup[1]][tup[0]] -= 1 # if the path is as good as the best path yet or better, reduce the experience value
            else:
                for tup in pathing:
                    self.experience[tup[1]][tup[0]] += self.learning_offset // 2 # half the experience value gained because at least the cell led to a valid path

        for tup in self.visited:
            if tup not in pathing:
                self.experience[tup[1]][tup[0]] += self.learning_offset
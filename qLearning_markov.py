import heapq
import random
import time

from Maze import Maze


# todo then run the search with the q learning matrix and compare with astar

class qlearning_markov:

    count: int = 0
    execution_time: int = 0
    lowest_step: int = None
    to_be_reset: bool = False
    parent_map: dict = {}
    visited: list = []
    learning: bool = False
    run_num: int = 1

    def __init__(self, maze: Maze, iterations: int = 500):

        rng = random.Random()

        # variables
        self.maze = maze
        self.start = (maze.startx, maze.starty)
        self.end = (maze.endx, maze.endy)
        self.astar_pathing = [self.start]
        self.queue = [(self.heuristic(self.start[0], self.start[1]), self.start)]
        self.experience = [[1 for x in range(self.maze.get_maze_x())] for y in range(maze.get_maze_y())]
        self.learn_start = (rng.randint(0, self.maze.get_maze_x() - 1), rng.randint(0, self.maze.get_maze_y() - 1))
        self.iterations = iterations

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
        self.parent_map = {}  # dont do this is allowing revisiting nodes
        self.parent_map[self.start] = None
        self.astar_pathing = [self.start]
        self.visited = []
        self.queue = [(self.heuristic(self.start[0], self.start[1]), self.start)]
        self.to_be_reset = False

    def get_policies(self, current_node):
        policies = []
        neighbors = self.maze.get_traversable_array(current_node[0], current_node[1])
        rng = random.Random()

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
                        # random_float = rng.uniform(0, self.max_random)
                        # enable rng if needed later
                        # add more shit here when necessary
                        heapq.heappush(policies, (self.heuristic(next_node[0], next_node[1]) + self.experience[next_node[1]][next_node[0]], [next_node, dir, self.heuristic(next_node[0], next_node[1]), self.experience[next_node[1]][next_node[0]]]))

        return policies

    def get_max_q_val(self, coord):
        output = 0
        for i in range(4):
            if i == 0 and coord[0] != 0 and self.maze.traversable(coord[0], coord[1], coord[0], coord[1] - 1):
                output = output if self.experience[coord[1] - 1][coord[0]] <= output else self.experience[coord[1] - 1][coord[0]]
            elif i == 1 and coord[0] != self.maze.get_maze_y() - 1 and self.maze.traversable(coord[0], coord[1], coord[0], coord[1] + 1):
                output = output if self.experience[coord[1] - 1][coord[0]] <= output else self.experience[coord[1] + 1][coord[0]]
            elif i == 2 and coord[1] != 0 and self.maze.traversable(coord[0], coord[1], coord[0] - 1, coord[1]):
                output = output if self.experience[coord[1]][coord[0] - 1] <= output else self.experience[coord[1]][coord[0] - 1]
            elif i == 3 and coord[1] != self.maze.get_maze_x() - 1 and self.maze.traversable(coord[0], coord[1], coord[0] + 1, coord[1]):
                output = output if self.experience[coord[1]][coord[0] + 1] <= output else self.experience[coord[1]][coord[0] + 1]

        return output

    def run(self):
        start_time = time.time_ns()
        self.visited = []
        self.parent_map = {}
        self.parent_map[self.start] = None

        while self.queue: # todo put learning in while loop

            if self.learning:
                rng = random.Random()
                for _ in range(self.iterations):
                    # reset the visited array
                    self.visited = []

                    # proc the recursion bfs learning
                    self.learn(self.learn_start)

                    # yield data to the gui
                    yield self.start, f"Learning...\ncurrently on iteration {self.run_num}", 0, self.experience

                    # randomize next start location for learning
                    self.learn_start = (rng.randint(0, self.maze.get_maze_x() - 1), rng.randint(0, self.maze.get_maze_y() - 1))

                    # housekeeping
                    self.run_num += 1

                self.queue = [(0, self.start)]
                self.learning = False
                self.visited = []

            # get the closest node as current node
            current_dist, current_node = heapq.heappop(self.queue)
            self.count += 1
            self.visited.append(current_node)

            # get policies
            policies = self.get_policies(current_node)

            # policies to string
            output = "Available policies (lowest weight will be picked):\n"
            if not policies:
                output += "No policies available\n"
            else:
                for i in range(len(policies)):
                    (_, policy) = policies[i]
                    if self.run_num == 1:
                        output += f"node: {str(policy[0])}\tdirection: {policy[1]}\tdistance: {policy[2]} + experience: {policy[3]} = sum: {round(policy[2] + policy[3], 2)}\n"
                    else:
                        output += f"node: {str(policy[0])}\tdirection: {policy[1]}\texperience: {policy[3]}\n"

            # yield data to the gui
            if current_node == self.end:
                if self.run_num == 1:
                    yield current_node, f"goal reached after {self.count} iterations", time.time_ns() - start_time + self.execution_time, self.experience
                    self.astar_pathing = self.reconstruct_path()
                    self.learning = True if self.run_num == 1 else self.learning
                    self.reset()
                    policies = []
                else:
                    yield current_node, f"goal reached after {self.count} iterations", time.time_ns() - start_time + self.execution_time, self.experience
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
                    if self.run_num == 1:
                        heapq.heappush(self.queue, (weight, policy[0]))
                    else:
                        if policy[0] == self.end: # ensure end node is reached first
                            policy[3] += 1000
                        heapq.heappush(self.queue, (-policy[3], policy[0]))


        self.execution_time = time.time_ns() - start_time # todo double check this functionality

        # yield for GUI if no path found
        yield None, "Path not found", 0, 0



    def learn(self, coord):

        # currently the reward is set to be 1 / distance to goal * 100

        alpha = 0.0002
        discount = 1.5
        current_val = self.experience[coord[1]][coord[0]]
        reward = (1 / self.heuristic(coord[0], coord[1]) if self.heuristic(coord[0], coord[1]) != 0 else 0.1) * 50

        self.experience[coord[1]][coord[0]] += alpha * (reward * (discount  * self.get_max_q_val(coord)) - current_val)
        self.visited.append(coord)
        # print(f"coord trained: {str(coord)} old value:{current_val} new value:{self.experience[coord[1]][coord[0]]}")

        # recurse, note it cannot reach isolated nodes
        for i in range(4):
            if i == 0 and coord[1] != 0 and (coord[0], coord[1] - 1) not in self.visited and self.maze.traversable(coord[0], coord[1] - 1, coord[0], coord[1]):
                self.learn((coord[0], coord[1] - 1))
            elif i == 1 and coord[1] != self.maze.get_maze_y() - 1 and (coord[0], coord[1] + 1) not in self.visited and self.maze.traversable(coord[0], coord[1] + 1, coord[0], coord[1]):
                self.learn((coord[0], coord[1] + 1))
            elif i == 2 and coord[0] != 0 and (coord[0] - 1, coord[1]) not in self.visited and self.maze.traversable(coord[0] - 1, coord[1], coord[0], coord[1]):
                self.learn((coord[0] - 1, coord[1]))
            elif i == 3 and coord[0] != self.maze.get_maze_x() - 1 and (coord[0] + 1, coord[1]) not in self.visited and self.maze.traversable(coord[0] + 1, coord[1], coord[0], coord[1]):
                self.learn((coord[0] + 1, coord[1]))
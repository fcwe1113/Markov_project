# constants
import warnings

import Node

class Maze:

    Maze: list[list[Node.Node]] = []
    startx: int
    starty: int
    endx: int
    endy: int

    def __init__(self, maze: list[list[list[bool]]], startx: int, starty: int, endx: int, endy: int):

        if startx == endx and starty == endy:
            raise ValueError("Start and End nodes cannot be the same")

        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy

        for i in range(len(maze)):
            self.Maze.append([])
            for j in range(len(maze[i])):
                self.Maze[i].append(Node.Node(i, j, maze[i][j][0], maze[i][j][1], maze[i][j][2], maze[i][j][3]))

        # raise a warning if start and/or end node is placed in isolated coord
        # no i am not integrating a search algorithm just to check can the 2 reach each other thats the point of the project lmao
        if self.Maze[starty][startx].is_isolated():
            warnings.warn("Start node is isolated")
        if self.Maze[endy][endx].is_isolated():
            warnings.warn("End node is isolated")

    def get_maze_x(self):
        return len(self.Maze)
    def get_maze_y(self):
        return len(self.Maze[0])
    def traversable(self, x1: int, y1: int, x2: int, y2: int): # x1 y1 being source and x2 y2 being dest, THIS IS A ONE WAY CHECKER
        if abs(x1 - x2 + y1 - y2) == 1: # check if they are 1 apart, if not return false
            if abs(x1 - x2) == 1: # check if they are 1 apart on the x axis, if not then its y axis
                if x1 > x2:
                    return self.Maze[y1][x1].get_left()
                else:
                    return self.Maze[y1][x1].get_right()
            else:
                if y1 > y2:
                    return self.Maze[y1][x1].get_up()
                else:
                    return self.Maze[y1][x1].get_down()
        else:
            return False

    def print_node(self, x, y):
        print(self.Maze[y][x])

    def is_start(self, x, y):
        return x == self.startx and y == self.starty

    def is_end(self, x, y):
        return x == self.endx and y == self.endy

    def __str__(self):
        # the tostring function of the maze
        # basically prints the maze out in shitty ascii chars
        # note the maze can theoretically support one way paths so i added them in and used arrows to display them
        # and an open space means u can go both ways
        output = "-----------------------------------------\n"

        def check_space(x, y) -> str:
            if self.is_start(x, y):
                return "s "
            elif self.is_end(x, y):
                return "e "
            else:
                return "  "

        for row in range(len(self.Maze)):
            output += "| " + check_space(0, row)
            for col in range(len(self.Maze[row])):
                # check for block to the right, skip if on right most block
                if col < len(self.Maze[row]) - 1: # left right
                    right = self.traversable(col, row, col + 1, row)
                    left = self.traversable(col + 1, row, col, row)
                    if right and left:
                        output += "  "
                    elif right and not left:
                        output += "→ "
                    elif not right and left:
                        output += "← "
                    else:
                        output += "| "

                    output += check_space(col + 1, row)
                else:
                    output += "|\n"

            for col in range(len(self.Maze[row])):
                # check for block below, skip if on bottom row
                if row < len(self.Maze) - 1:
                    output += "-"
                    down = self.traversable(col, row, col, row + 1)
                    up = self.traversable(col, row + 1, col, row)
                    if down and up:
                        output += "   "
                    elif down and not up:
                        output += " ↓ "
                    elif not down and up:
                        output += " ↑ "
                    else:
                        output += "---"
                else:
                    output += "----"
            output += "-\n"
        return output + "Start: s\tEnd: e\tOne way paths: arrows\n"
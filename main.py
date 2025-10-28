import Maze

# constants

# the maze define, each group of 4 bools represent traversable directions of up down left right, the 4 bools are always in that order
# can be extended or reduced if needed, the maze class is capable of taking in size changes, provided the maze is in rectangular form
# if someone has a better way of initializing this without just shoving it into a separate file please tell me this is a fking eyesore
MAZE = [[[False, False, False, True], [False, True, False, True], [False, False, True, True], [False, False, True, True], [False, False, True, True], [False, True, True, False], [False, True, False, True], [False, False, True, True], [False, False, True, True], [False, True, True, False]],
        [[True, True, False, False], [False, False, True, True], [False, True, True, False], [False, True, False, True], [False, True, True, False], [True, False, False, True], [True, False, True, False], [False, False, False, False], [False, False, False, True], [True, True, True, False]],
        [[True, True, False, True], [False, False, True, True], [True, False, True, False], [True, True, False, False], [True, True, False, True], [False, False, True, True], [False, True, True, True], [False, True, True, True], [False, True, True, False], [True, True, False, False]],
        [[True, False, False, True], [False, True, True, False], [False, True, False, True], [True, False, True, False], [True, True, False, True], [False, False, True, False], [True, False, False, True], [True, True, True, False], [True, True, False, False], [True, True, False, False]],
        [[False, True, False, False], [True, True, False, False], [True, True, False, False], [False, False, False, True], [True, False, True, False], [False, True, False, True], [False, True, True, False], [True, True, False, False], [True, True, False, False], [True, True, False, False]],
        [[True, False, False, True], [True, False, True, False], [True, True, False, False], [False, False, False, True], [False, False, True, True], [True, False, True, False], [True, True, False, False], [True, True, False, False], [True, False, False, True], [True, False, True, False]],
        [[False, True, False, True], [False, True, True, False], [True, False, False, True], [False, False, True, False], [False, True, False, True], [False, True, True, False], [True, True, False, False], [True, True, False, False], [False, True, False, True], [False, False, True, False]],
        [[True, True, False, False], [True, False, False, True], [False, True, True, True], [False, False, True, True], [True, False, True, False], [True, False, False, True], [True, False, True, False], [True, False, False, True], [True, False, True, True], [False, True, True, False]],
        [[True, False, False, True], [False, True, True, False], [True, True, False, False], [False, True, False, True], [False, False, True, True], [False, False, True, True], [False, False, True, True], [False, True, True, False], [False, True, False, False], [True, True, False, False]],
        [[False, False, False, True], [True, False, True, False], [True, False, False, True], [True, False, True, True], [False, False, True, False], [False, False, False, True], [False, False, True, True], [True, False, True, False], [True, False, False, True], [True, False, True, False]]]


if __name__ == '__main__':
    environment = Maze.Maze(MAZE, 0, 0, 7, 1)
    print(environment)


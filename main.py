import tkinter as tk

import Maze
import mazeGUI

# constants

# the maze define, each group of 4 bools represent traversable directions of up down left right, the 4 bools are always in that order
# can be extended or reduced if needed, the maze class is capable of taking in size changes, provided the maze is in rectangular form
# if someone has a better way of initializing this without just shoving it into a separate file please tell me this is a fking eyesore
MAZE = [[[False, True, False, True], [False, False, False, True], [False, False, True, True], [False, False, True, True], [False, False, True, True], [False, True, True, False], [False, True, False, True], [False, False, True, True], [False, False, True, True], [False, True, True, False], [False, True, False, True], [False, True, True, True], [False, True, True, True], [False, True, True, False]],
        [[True, True, False, False], [True, False, True, True], [False, False, True, True], [False, True, True, False], [False, False, False, False], [True, False, False, True], [True, False, True, False], [False, True, False, False], [False, True, True, True], [True, False, True, False], [True, True, False, True], [True, True, True, True], [True, True, True, True], [True, True, True, False]],
        [[True, True, False, False], [False, True, False, True], [False, False, True, True], [True, False, True, False], [False, True, False, True], [False, True, True, True], [False, True, True, True], [False, True, True, True], [True, True, True, False], [False, True, False, False], [True, True, False, True], [True, True, True, True], [True, False, True, True], [True, True, True, False]],
        [[True, True, False, False], [True, True, False, False], [False, True, False, True], [False, True, True, True], [True, True, True, True], [True, True, True, True], [True, True, True, True], [False, True, True, True], [True, True, True, False], [True, True, False, False], [True, True, False, True], [True, True, True, False], [False, False, False, True], [True, True, True, False]],
        [[True, True, False, False], [True, True, False, False], [True, True, False, True], [True, True, True, True], [True, True, True, True], [True, True, True, False], [True, True, True, False], [False, True, True, True], [True, True, True, False], [True, True, False, False], [True, True, False, True], [True, True, True, True], [False, True, True, True], [True, True, True, False]],
        [[True, True, False, False], [True, True, False, False], [True, True, False, False], [True, True, False, False], [True, True, False, False], [False, True, False, False], [True, True, False, False], [True, True, False, False], [True, True, False, False], [True, True, False, False], [True, True, False, True], [True, True, True, True], [True, True, True, True], [True, True, True, False]],
        [[True, True, False, False], [True, True, False, False], [True, False, False, True], [True, True, True, True], [True, False, True, True], [True, False, True, True], [True, False, True, True], [True, False, True, True], [True, False, True, True], [True, False, True, False], [True, True, False, True], [True, True, True, True], [True, True, True, True], [True, True, True, False]],
        [[True, True, False, False], [True, True, False, True], [False, True, True, False], [True, False, False, True], [False, False, True, True], [False, False, True, True], [False, False, True, True], [False, False, True, True], [False, False, True, True], [False, True, True, False], [True, True, False, True], [True, True, True, True], [True, True, True, True], [True, True, True, False]],
        [[True, True, False, False], [True, False, False, True], [True, True, True, False], [False, True, False, True], [False, False, True, True], [False, False, True, True], [False, False, True, True], [False, True, True, False], [False, True, False, False], [True, True, False, False], [True, True, False, True], [True, True, True, True], [True, True, True, True], [True, True, True, False]],
        [[True, False, False, True], [False, False, True, True], [True, False, True, False], [True, False, False, True], [False, False, True, False], [False, False, False, True], [False, False, True, True], [True, False, True, True], [True, False, True, True], [True, False, True, True], [True, False, True, True], [True, False, True, True], [True, False, True, True], [True, False, True, False]],
        [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]],
        [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]],
        [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]],
        [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]],
        [[False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False], [False, False, False, False]]]


# add noise
    # apply randomness to each weight decision to eliminate deterministic behaviour
    # like a random number to add to each weight for the bot to be able to make bad decisions
# make the maze larger
# make a experience matrix for each maze bloc
    # as a kind of "learning" showing which bloc gave a more positive experience for reaching the goal
# current weight formula: given_weight + random_value(different for each option) + experience_value(if any)

if __name__ == '__main__':
    gui = tk.Tk()
    start_pos = (0, 0)
    end_pos = (12, 3)

    app = mazeGUI.mazeGUI(gui, MAZE, start_pos, end_pos, animation_delay=500)

    gui.mainloop()
    # environment = Maze.Maze(MAZE, 0, 0, 9, 9)
    # print(environment)
    # print(environment.print_dist())
    # print(environment.markov_traverse_heuristic(display_decision=True))
    # print(environment.markov_traverse_distance_matrix(display_decision=True))
    #
    # print(310 % 10 ** 1)
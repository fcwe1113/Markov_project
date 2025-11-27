import tkinter as tk
from tkinter import StringVar

import Maze
import heuristic_markov


class mazeGUI:

    # class constants
    CELL_SIZE = 40
    WALL_WIDTH = 3

    def __init__(self, root, layout, start, end, animation_delay=30):
        # main tkinter window
        self.root = root

        # create the maze obj
        self.layout = Maze.Maze(layout, start[0], start[1], end[0], end[1])

        # store the start and end nodes
        self.start = start
        self.end = end

        # store the last visited node
        self.last_node = self.start

        # string var for bottom info text
        self.canvas_legend = "Green: Start   Red: Goal   Blue: Visiting   Cyan: Visited\nRed: Visiting repeated   Orange: Visited repeated"
        self.info_text_display = StringVar(value=self.canvas_legend)

        # store the animation delay, or the delay between search steps
        self.animation_delay = animation_delay

        # string vars to store the text output
        self.execution_time = 0 # in nanoseconds

        # make visited array of the GUI to keep track of visited squares
        self.visited = []
        self.last_node_repeated = False

        # store variables for map gen variables
        # for obvious reasons dont set them too high unless you hate yourself
        self.wall_percentage = tk.IntVar(value=10) # probability (in %) for walls to appear in a block border
        self.oneway_percentage = tk.IntVar(value=10) # probability (in %) for oneways to appear in a block border

        # markov process to use
        self.search_instance = None
        # search generator for step by step execution
        self.search_generator = None
        # flag to signify search has started
        self.search_started = False
        # flag to enable pausing the program
        self.paused = False
        # NOTE: no need to reset the 2 flags below as the speed controls override them anyways
        # flag to show fast forward
        self.fast_forward = False
        # flag to show max speed
        self.max_speed = False

        # GUI setup
        # set window title
        self.root.title("Markov process visualizer")

        # create frame widgets to hold the control buttons
        # NOTE: they kind of function like rows hence their name
        self.row_one = tk.Frame(self.root)
        self.row_two = tk.Frame(self.root)
        # pack the frames(rows) with some vertical padding
        self.row_one.pack(pady=10)
        self.row_two.pack(pady=10)

        # LINE 1
        # label for dropdown menu
        self.markovs_label = tk.Label(self.row_one, text="Algorithm:")
        self.markovs_label.pack(side="left", padx=5)

        # dropdown to select algorithm
        # variable to hold the dropdown content
        self.markov_var = tk.StringVar(value="Heuristic")

        # list to hold the dropdown options
        options = ["Heuristic", "Markov2", "Markov3", "Markov4", "Markov5"]

        # the actual dropdown object
        self.markov_menu = tk.OptionMenu(self.row_one, self.markov_var, options[0], *options)
        self.markov_menu.pack(side="left", padx=5)

        # pause button
        self.pause_button = tk.Button(self.row_one, text="⏸", command=self.pause_func, width=2)
        self.pause_button.pack(side="left", padx=5)

        # play button
        self.play_button = tk.Button(self.row_one, text="▶", command=self.start_resume_func, width=2)
        self.play_button.pack(side="left", padx=(0, 5))

        # fast forward button
        self.fast_forward_button = tk.Button(self.row_one, text="⏩", command=self.fast_forward_func, width=2)
        self.fast_forward_button.pack(side="left", padx=(0, 5))

        # max speed button
        self.max_speed_button = tk.Button(self.row_one, text="⏭", command=self.max_speed_func, width=2)
        self.max_speed_button.pack(side="left", padx=(0, 5))

        # reset button
        self.reset_button = tk.Button(self.row_one, text="Reset", command=self.reset, width=5)
        self.reset_button.pack(side="left", padx=5)

        # randomize environment button
        self.randomize_button = tk.Button(self.row_one, text="Randomize Environment", command=self.randomize_maze)
        self.randomize_button.pack(side="left", padx=5)
        # LINE 1 end

        # LINE 2
        # wall slider label
        self.wall_slider_label = tk.Label(self.row_two, text="Wall percentage:")
        self.wall_slider_label.pack(side="left", padx=5)

        # wall slider
        # text to show what the current value of the sliders are
        # have to be declared before the sliders themselves as the sliders reference these 2 during their declarations, sorry :3
        self.wall_slider_display = tk.Label(self.row_two, text=f"{self.wall_percentage.get()}%", width=4)
        self.oneway_slider_display = tk.Label(self.row_two, text=f"{self.oneway_percentage.get()}%", width=4)

        # The sliders themselves, one for adjusting how many walls and the other for adjusting how many one-ways
        self.wall_slider = tk.Scale(self.row_two, orient="horizontal", from_=0, to=100 - self.oneway_percentage.get())
        self.wall_slider.set(self.wall_percentage.get())
        self.oneway_slider = tk.Scale(self.row_two, orient="horizontal", from_=0, to=100 - self.wall_percentage.get(), command=self.update_sliders)
        self.oneway_slider.set(self.oneway_percentage.get())
        self.wall_slider.config(command=self.update_sliders)  # tacking this onto wall slider at this point to prevent circular referencing

        self.wall_slider.pack(side="left", padx=5)  # item 2 is slider 1

        self.wall_slider_display.pack(side="left", padx=5)  # item 3 is display for slider 1

        # Text to show what second slider is
        self.oneway_slider_label = tk.Label(self.row_two, text="One-way percentage:")
        self.oneway_slider_label.pack(side="left", padx=5)  # item 4 is slider 2 description

        self.oneway_slider.pack(side="left", padx=5)  # item 5 is slider 2

        self.oneway_slider_display.pack(side="left", padx=5)  # item 6 is slider 2 display

        # canvas setup
        # convert the maze dimensions into grid units
        self.map_height = self.layout.get_maze_y()
        self.map_width = self.layout.get_maze_x()

        # create the canvas widget
        self.canvas = tk.Canvas(self.root, width=self.map_width * self.CELL_SIZE, height=self.map_height * self.CELL_SIZE, bg="white", relief="solid", borderwidth=1, highlightthickness=1)
        self.canvas.pack(pady=10, padx=10)

        self.textbox = tk.Label(root, textvariable=self.info_text_display)
        self.textbox.pack(pady=5)

        # draw the initial environment
        self.draw_initial_map()

    def get_canvas_coords(self, x, y):
        return x * self.CELL_SIZE, y * self.CELL_SIZE, (x + 1) * self.CELL_SIZE, (y + 1) * self.CELL_SIZE

    def draw_arrow(self, x1, y1, x2, y2, colour="black"):  # only able to draw horizontal and vertical arrows
        ARROW_TIP_OFFSET = 7
        self.canvas.create_line(x1, y1, x2, y2, width=self.WALL_WIDTH / 2, fill=colour)

        if y1 == y2:
            if x1 < x2:
                self.canvas.create_line(x2, y2, x2 - ARROW_TIP_OFFSET, y2 + ARROW_TIP_OFFSET, width=self.WALL_WIDTH / 2, fill=colour)
                self.canvas.create_line(x2, y2, x2 - ARROW_TIP_OFFSET, y2 - ARROW_TIP_OFFSET, width=self.WALL_WIDTH / 2, fill=colour)
            elif x1 > x2:
                self.canvas.create_line(x2, y2, x2 + ARROW_TIP_OFFSET, y2 + ARROW_TIP_OFFSET, width=self.WALL_WIDTH / 2, fill=colour)
                self.canvas.create_line(x2, y2, x2 + ARROW_TIP_OFFSET, y2 - ARROW_TIP_OFFSET, width=self.WALL_WIDTH / 2, fill=colour)
        elif x1 == x2:
            if y1 < y2:
                self.canvas.create_line(x2, y2, x2 - ARROW_TIP_OFFSET, y2 - ARROW_TIP_OFFSET, width=self.WALL_WIDTH / 2, fill=colour)
                self.canvas.create_line(x2, y2, x2 + ARROW_TIP_OFFSET, y2 - ARROW_TIP_OFFSET, width=self.WALL_WIDTH / 2, fill=colour)
            elif y1 > y2:
                self.canvas.create_line(x2, y2, x2 - ARROW_TIP_OFFSET, y2 + ARROW_TIP_OFFSET, width=self.WALL_WIDTH / 2, fill=colour)
                self.canvas.create_line(x2, y2, x2 + ARROW_TIP_OFFSET, y2 + ARROW_TIP_OFFSET, width=self.WALL_WIDTH / 2, fill=colour)
        else:
            raise ValueError("diagonal arrows are not supported")

    def draw_cell_content(self, x, y, text=None, colour=None):
        x0, y0, x1, y1 = self.get_canvas_coords(x, y)

        if colour:
            padding = self.WALL_WIDTH + 2
            self.canvas.create_rectangle(x0 + padding, y0 + padding, x1 - padding, y1 - padding, fill=colour, outline="", tags="cell_content")
        if text:
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=text, font=("Arial", 16), fill="black", tags="cell_content")

    def draw_initial_map(self):
        arrow_offset = 0.3

        # clear the canvas
        self.canvas.delete("all")

        # loop through every cell in the grid
        for y in range(self.map_height):
            for x in range(self.map_width):
                # get pixel coords
                x0, y0, x1, y1 = self.get_canvas_coords(x, y)

                # get traversable array
                traversable = self.layout.get_traversable_array(x, y)

                # draw walls and oneways
                if not traversable[0]: # up
                    if y != 0 and self.layout.traversable(x, y - 1, x, y):  # draw down arrows
                        self.draw_arrow(x1 - self.CELL_SIZE / 2, y1 - self.CELL_SIZE * 1.5 + self.CELL_SIZE * arrow_offset, x1 - self.CELL_SIZE / 2, y1 - self.CELL_SIZE / 2 - self.CELL_SIZE * arrow_offset)
                    else:
                        self.canvas.create_line(x0, y0, x1, y0, fill='black', width=self.WALL_WIDTH)
                # Draw down wall
                if not traversable[1]: # down
                    if y != self.map_height - 1 and self.layout.traversable(x, y + 1, x, y):  # draw up arrows
                        self.draw_arrow(x1 - self.CELL_SIZE / 2, y1 + self.CELL_SIZE / 2 - self.CELL_SIZE * arrow_offset, x1 - self.CELL_SIZE / 2, y1 - self.CELL_SIZE / 2 + self.CELL_SIZE * arrow_offset)
                    else:
                        self.canvas.create_line(x0, y1, x1, y1, fill='black', width=self.WALL_WIDTH)
                # Draw left wall
                if not traversable[2]: # left
                    if x != 0 and self.layout.traversable(x - 1, y, x, y):  # draw right arrow
                        self.draw_arrow(x1 - self.CELL_SIZE * 1.5 + self.CELL_SIZE * arrow_offset, y1 - self.CELL_SIZE / 2, x1 - self.CELL_SIZE + self.CELL_SIZE * arrow_offset, y1 - self.CELL_SIZE / 2)
                    else:
                        self.canvas.create_line(x0, y0, x0, y1, fill='black', width=self.WALL_WIDTH)
                # Draw right wall
                if not traversable[3]: # right
                    if x != self.map_width - 1 and self.layout.traversable(x + 1, y, x, y):  # draw left arrow
                        self.draw_arrow(x1 + self.CELL_SIZE / 2 - self.CELL_SIZE * arrow_offset, y1 - self.CELL_SIZE / 2, x1 - self.CELL_SIZE / 2 + self.CELL_SIZE * arrow_offset, y1 - self.CELL_SIZE / 2)
                    else:
                        self.canvas.create_line(x1, y0, x1, y1, fill='black', width=self.WALL_WIDTH)

        self.draw_cell_content(self.start[0], self.start[1], "S", "green")
        self.draw_cell_content(self.end[0], self.end[1], "E", "red")

    # the function the sliders call whenever they are moved
    def update_sliders(self, event):

        # updates the percentage variable with the slider
        self.wall_percentage = int(self.wall_slider.get())
        self.oneway_percentage = int(self.oneway_slider.get())

        # update slider 1 and its display
        self.wall_slider_display.config(text=f"{self.wall_percentage}%")
        self.wall_slider.config(to=100 - self.oneway_percentage)

        # update slider 2 and its display
        self.oneway_slider_display.config(text=f"{self.oneway_percentage}%")
        self.oneway_slider.config(to=100 - self.wall_percentage)

    def pause_func(self):
        if self.search_started:
            self.paused = True

    def fast_forward_func(self):
        if not self.search_started:
            self.start_resume_func()
        if self.paused:
            self.paused = False
        self.fast_forward = True
        self.max_speed = False

    def max_speed_func(self):
        if not self.search_started:
            self.start_resume_func()
        if self.paused:
            self.paused = False
        self.fast_forward = False
        self.max_speed = True

    # randomizes maze with the randomize function within the maze class
    # also does some housekeeping to ensure the GUI updates correctly
    def randomize_maze(self):
        self.layout.randomize(self.wall_percentage, self.oneway_percentage)
        self.start = (self.layout.startx, self.layout.starty)
        self.end = (self.layout.endx, self.layout.endy)
        self.reset()
        self.draw_initial_map()
        # print(self.maze)

    def reset(self):
        self.search_started = False

        # shut down the generator if its running
        if self.search_generator:
            try: self.search_generator.close()
            except GeneratorExit: pass

        # clear search state variables
        self.search_instance = None
        self.search_generator = None

        # reset state variables
        self.last_node = self.start
        self.paused = False
        self.info_text_display.set(self.canvas_legend)
        self.visited = []
        self.last_node_repeated = False
        self.execution_time = 0

        # reenable the gui
        self.markov_menu.config(state="normal")

        # redraw the environment
        self.draw_initial_map()

    def start_resume_func(self):
        self.fast_forward = False
        self.max_speed = False
        if self.search_started:
            self.paused = False
        elif not self.search_started:
            # reset the board and start the animation loop
            self.reset()
            self.search_started = True
            # disable the menu dropdown while the search is running
            self.markov_menu.config(state="disabled")

            # get the markov algorithm from the dropdown
            markov_choice = self.markov_var.get()

            if "Heuristic" in markov_choice: # replace with an actual algorithm name
                self.search_instance = heuristic_markov.heuristic_markov(self.layout) # placeholder
            else:
                print(f"Algorithm {markov_choice} not implemented")
                self.reset()
                return

            # get generator function from algorithm object
            self.search_generator = self.search_instance.run()

            # call animation loop function for the first time
            self.run_search_step()

    def run_search_step(self):
        # stop the animation is search is stopped
        if not self.search_started:
            return

        if self.paused:
            self.root.after(1, self.run_search_step)
        else:
            try:
                # get the next node from the search generator
                current_node, text, execution_time = next(self.search_generator)
                if text != "":
                    self.info_text_display.set(f"{self.canvas_legend}\n{text}")
                else:
                    self.info_text_display.set(self.canvas_legend)

                if current_node == None:
                    self.search_started = False
                    return
                else:
                    self.execution_time += execution_time

                (x, y) = current_node

                if self.last_node != self.start and self.last_node != self.end:
                    if self.last_node_repeated:
                        self.draw_cell_content(self.last_node[0], self.last_node[1], colour="orange")
                        self.last_node_repeated = False
                    else:
                        self.draw_cell_content(self.last_node[0], self.last_node[1], colour="cyan")

                if current_node != self.start and self.last_node != self.end:
                    if current_node in self.visited:
                        self.draw_cell_content(x, y, colour="red")
                        self.last_node_repeated = True
                    else:
                        self.draw_cell_content(x, y, colour="blue")
                        self.visited.append(current_node) if current_node not in self.visited else None
                self.last_node = current_node

                # check if reached goal
                if current_node == self.end:
                    self.search_started = False
                    self.draw_final_path()
                    self.markov_menu.config(state="normal")
                    return

                #schedule the next animation loop
                if self.max_speed:
                    self.root.after(1, self.run_search_step)
                elif self.fast_forward:
                    self.root.after(self.animation_delay // 2, self.run_search_step)
                else:
                    self.root.after(self.animation_delay, self.run_search_step)

            except StopIteration:
                self.search_started = False
                self.markov_menu.config(state="normal")
            except Exception as e:
                self.info_text_display.set(f"{self.canvas_legend}\nAn error occurred:{e}")
                self.search_started = False
                self.markov_menu.config(state="normal")

    def draw_final_path(self):

        self.info_text_display.set(f"{self.canvas_legend}\nexecution time: {self.execution_time}")
        path = self.search_instance.reconstruct_path()

        if not path:
            print("path reconstruction failed")
            return

        for i in range(len(path) - 1):
            x_start, y_start = path[i]
            x_end, y_end = path[i + 1]

            # get the central pixel coord of the start cell
            x0, y0, x1, y1 = self.get_canvas_coords(x_start, y_start)
            start_center_x, start_center_y = (x0 + x1) / 2, (y0 + y1) / 2

            # get the central pixel coord of the end cell
            x0, y0, x1, y1 = self.get_canvas_coords(x_end, y_end)
            end_center_x, end_center_y = (x0 + x1) / 2, (y0 + y1) / 2

            # draw the line connecting the centres
            self.canvas.create_line(start_center_x, start_center_y, end_center_x, end_center_y, fill="magenta", width=3)

            # redraw start and end on top so the path line doesnt cover them
            self.draw_cell_content(self.start[0], self.start[1], "S", "green")
            self.draw_cell_content(self.end[0], self.end[1], "E", "red")
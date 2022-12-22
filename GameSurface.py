import math
import os

import pygame
from pygame import Surface
from Game import Game

LIVES_IMAGE = pygame.image.load(os.path.join("images", "life.png"))

TEXT_COLOR = (0, 0, 0)

MAX_STEPS_TO_UPDATE_DOWN = 25
MAX_STEPS_TO_UPDATE_RIGHT = 25

HIGHLIGHTED_COLOR = (224, 236, 255)
LINE_THICKNESS = 2


class GameSurface:
    def __init__(self, x, y, width, height, game_settings: dict, background_color):
        # the coordinates relative to the whole screen,useful at the mouse position
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.background_color = background_color

        # TODO: Allocate height and width based on the dimensions of the game
        self.level_height = 50
        self.level_width = 100

        self.info_height = 50
        self.info_width = self.width

        self.board_width = width
        self.board_height = height - self.level_height - self.info_height

        self.game = Game(game_settings)

        self.surface = pygame.Surface((width, height))

        self.no_lines = game_settings["no_lines"]
        self.no_columns = game_settings["no_columns"]

        self.cell_width = self.board_width / self.no_columns
        self.cell_height = self.board_height / self.no_lines

        # TODO:If there are empty pixels,it doesn't center
        #  properly using them...it even puts spaces between cells...Why?

        # center the start of the board,such that pixels not covered will be evenly placed on each side
        self.board_x = (self.board_width % self.no_columns) / 2
        self.board_y = self.level_height + (self.board_height % self.no_lines) / 2

        # the coords of each cell
        # the fixed points at which we would draw the cells
        self.initial_cell_coords = []
        for line in range(self.no_lines):
            line_coords = []
            for column in range(self.no_columns):
                line_coords.append((self.board_x + column * self.cell_width, self.board_y + line * self.cell_height))
            self.initial_cell_coords.append(line_coords)

        # the current cell coords,used to allow a more dynamic update of the table
        self.cell_coords = [[self.initial_cell_coords[line][column] for column in range(self.no_columns)] for line in
                            range(self.no_lines)]

        # values for the moving animation
        # if the board is still updating(the cells values are still moving on the board)
        self.updating_down, self.updating_right = False, False

        # boards after the first deletion,after applying the DOWN rule(where we move each cell downwards as far as possible)
        # and after the RIGHT rule(move the columns to the right as far as possible)
        self.after_action_board, self.after_down_board, self.after_right_board = None, None, None
        # the distance for each cell/columns to move for a step and the limit/as far as it can go in that direction
        self.down_update_distance, self.right_update_distance, self.down_update_limit, self.right_update_limit = None, None, None, None

        # used for the animation where it shows all the possible deleted cells
        self.highlighted_cells = [[False for column in range(self.no_columns)] for line in range(self.no_lines)]

        # the images for each cell
        self.hieroglyphs = []
        for index in range(6):
            hieroglyph = pygame.image.load(os.path.join("images", "hieroglyph" + str(index) + ".PNG"))
            hieroglyph = pygame.transform.scale(hieroglyph, (self.cell_width, self.cell_height))
            self.hieroglyphs.append(hieroglyph)

        # the font which we will use
        self.font = pygame.font.SysFont("Roboto", 30)

        # the heart image
        self.lives_image = pygame.transform.scale(LIVES_IMAGE, (30, self.info_height))

        self.draw()

    def draw_level(self):
        level_text = self.font.render("LEVEL : " + str(self.game.level), True, TEXT_COLOR)
        text_rect = level_text.get_rect()
        text_rect.center = (self.level_width / 2, self.level_height / 2)

        self.surface.blit(level_text, text_rect)

        # separator
        start_position = self.initial_cell_coords[0][0]
        end_position = (self.initial_cell_coords[0][self.no_columns - 1][0] + self.cell_width, \
                        self.initial_cell_coords[0][self.no_columns - 1][1])
        pygame.draw.line(self.surface, (0, 0, 0), start_position, end_position)

    def draw_board(self):
        # draw the board
        if self.updating_down:
            board = self.after_action_board
        elif self.updating_right:
            board = self.after_down_board
        else:
            board = self.game.board

        for line in range(self.no_lines):
            for column in range(self.no_columns):
                x, y = self.cell_coords[line][column]
                value = board[line][column]
                if value != -1:
                    self.surface.blit(self.hieroglyphs[value], (x, y))

                    # if we aren't moving the cells and this cell is currently highlighted,do so
                    if not self.updating_down and not self.updating_right and self.highlighted_cells[line][column]:
                        pygame.draw.rect(self.surface, HIGHLIGHTED_COLOR, [x, y, self.cell_width, self.cell_height],
                                         LINE_THICKNESS)

    def draw_info(self):

        # draw separator
        y_coord = self.initial_cell_coords[self.no_lines - 1][0][1] + self.cell_height
        pygame.draw.line(self.surface, (0, 0, 0),
                         (self.initial_cell_coords[self.no_lines - 1][0][0], y_coord),
                         (self.initial_cell_coords[self.no_lines - 1][self.no_columns - 1][0] + self.cell_width,
                          y_coord))

        # draw info
        x = 0
        y = self.level_height + self.board_height

        # draw heart and lives left
        self.surface.blit(self.lives_image, (x + 20, y))

        lives_text = self.font.render("X" + str(self.game.no_lives_left), True, TEXT_COLOR)
        self.surface.blit(lives_text, (x + 60, y + 20))

        # draw score
        score_text = self.font.render("SCORE : " + str(self.game.score), True, TEXT_COLOR)
        self.surface.blit(score_text, (x + self.info_width - 150, y + 20))

    def draw(self):
        self.surface.fill(self.background_color)

        self.draw_level()
        self.draw_board()
        self.draw_info()

    def update_coords(self):
        """
        Used to update the coordinates of the cells to create the movement of the cells according to the game rules
        Updates the updating_down and updating_right accordingly
        On each call,moves one step the cells of the board
        :return:
        """

        if self.updating_down:
            updated = False
            for line in range(self.no_lines):
                for column in range(self.no_columns):
                    x_coord = self.cell_coords[line][column][0]
                    y_coord = self.cell_coords[line][column][1]

                    y_limit = self.down_update_limit[line][column][1]
                    # if it can still go down
                    if y_coord < y_limit:
                        y_coord = min(y_coord + self.down_update_distance[line][column], y_limit)
                        self.cell_coords[line][column] = (x_coord, y_coord)
                        updated = True

            if not updated:
                self.updating_down = False

                # TODO:Better way to copy the values?
                for line in range(self.no_lines):
                    for column in range(self.no_columns):
                        self.cell_coords[line][column] = self.initial_cell_coords[line][column]

        elif self.updating_right:
            updated = False
            for line in range(self.no_lines):
                for column in range(self.no_columns):
                    x_coord = self.cell_coords[line][column][0]
                    y_coord = self.cell_coords[line][column][1]

                    x_limit = self.right_update_limit[column][0]
                    # if it can still go right
                    if x_coord < x_limit:
                        x_coord = min(x_coord + self.right_update_distance[column], x_limit)
                        self.cell_coords[line][column] = (x_coord, y_coord)
                        updated = True
            if not updated:
                self.updating_right = False

                # TODO:Better way to copy the values?
                for line in range(self.no_lines):
                    for column in range(self.no_columns):
                        self.cell_coords[line][column] = self.initial_cell_coords[line][column]
        self.draw()

    def compute_parameters(self):
        """
        Compute the necessary information to perform the update of the cells
        :return:
        """
        # update variables and values used to move from top to down
        no_deleted_below = [[0 for column in range(self.no_columns)] for line in range(self.no_lines)]

        # for line in self.initial_cell_coords:
        #     print(line)

        for line in range(self.no_lines - 2, -1, -1):
            for column in range(self.no_columns):
                no_deleted_below[line][column] = (self.after_action_board[line + 1][column] == -1) + \
                                                 no_deleted_below[line + 1][column]
        # print("No values below:")
        # for line in no_deleted_below:
        #     print(line)

        self.down_update_distance = [[0 for column in range(self.no_columns)] for line in range(self.no_lines)]

        self.down_update_limit = [[(0, 0) for column in range(self.no_columns)] for line in range(self.no_lines)]

        for line in range(self.no_lines - 1, -1, -1):
            for column in range(self.no_columns):
                no_values_deleted = no_deleted_below[line][column]
                no_values_left = self.no_lines - line - 1 - no_values_deleted

                y_distance = no_values_deleted * self.cell_height
                step_length = int(math.ceil(1.0 * y_distance / MAX_STEPS_TO_UPDATE_DOWN))

                self.down_update_distance[line][column] = step_length
                self.down_update_limit[line][column] = (self.initial_cell_coords[line][column][0],
                                                        self.initial_cell_coords[self.no_lines - 1 - no_values_left][
                                                            column][1])

        # print("Down updates distance below:")
        # for line in self.down_update_distance:
        #     print(line)
        #
        # print("Update limit:")
        # for line in self.update_limit:
        #     print(line)

        # update variables and values to move from left to right
        no_deleted_right = [0 for column in range(self.no_columns)]

        for column in range(self.no_columns - 2, -1, -1):
            no_deleted_right[column] = (self.after_down_board[self.no_lines - 1][column + 1] == -1) + no_deleted_right[
                column + 1]

        self.right_update_distance = [0 for column in range(self.no_lines)]

        self.right_update_limit = [(0, 0) for column in range(self.no_columns)]

        for column in range(self.no_columns):
            no_values_deleted = no_deleted_right[column]
            no_values_left = self.no_columns - column - 1 - no_values_deleted

            y_distance = no_values_deleted * self.cell_width
            step_length = int(math.ceil(1.0 * y_distance / MAX_STEPS_TO_UPDATE_RIGHT))

            self.right_update_distance[column] = step_length
            self.right_update_limit[column] = (self.initial_cell_coords[0][self.no_columns - 1 - no_values_left][0], -1)

    def reset(self):
        self.highlighted_cells = [[False for column in range(self.no_columns)] for line in range(self.no_lines)]
        self.updating_down = self.updating_right = False

        # TODO:Shorter way to copy values to the other matrix without 2 for loops
        #  Did it this way to avoid the using the reference
        for line in range(self.no_lines):
            for column in range(self.no_columns):
                self.cell_coords[line][column] = (
                    self.initial_cell_coords[line][column][0], self.initial_cell_coords[line][column][1])

        self.game.reset_game()
        self.draw()

    def compute_board_position(self, mouse_position):
        mouse_x = mouse_position[0] - self.x
        mouse_y = mouse_position[1] - self.y

        chosen_line = chosen_column = -1
        for line in range(self.no_lines):
            for column in range(self.no_columns):
                if self.initial_cell_coords[line][column][0] <= mouse_x < (
                        self.initial_cell_coords[line][column][0] + self.cell_width) and \
                        self.initial_cell_coords[line][column][1] <= mouse_y < (
                        self.initial_cell_coords[line][column][1] + self.cell_height):
                    chosen_line = line
                    chosen_column = column

        return chosen_line, chosen_column

    def highlight_possible_deleted_cells(self, mouse_position):
        chosen_line, chosen_column = self.compute_board_position(mouse_position)

        no_visited_cells, self.highlighted_cells = self.game.get_deletion_result(chosen_line, chosen_column)

        self.draw()

        self.highlighted_cells = [[False for column in range(self.no_columns)] for line in range(self.no_lines)]

    def act(self, mouse_position):
        chosen_line, chosen_column = self.compute_board_position(mouse_position)

        changed, self.after_action_board, self.after_down_board, self.after_right_board = self.game.act(chosen_line,
                                                                                                        chosen_column)
        if changed:
            # start the moving of the cells accordingly
            self.updating_down, self.updating_right = True, True
            self.compute_parameters()
            self.draw()

    def game_over(self):
        return self.game.game_over()

    def get_score(self):
        return self.game.score

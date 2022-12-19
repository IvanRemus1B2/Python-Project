import random

from queue import Queue

MAX_LEVEL = 5
BLOCK_VALUE = 1

# the neighbors for a given cell in the board
NO_NEIGHBOURS = 4
LINE_VALUES = (-1, 0, 1, 0)
COLUMN_VALUES = (0, 1, 0, -1)


class Game:
    def __init__(self, game_settings):

        if "no_lines" not in game_settings:
            raise Exception("Number of lines for the board game not specified")
        elif "no_columns" not in game_settings:
            raise Exception("Number of columns for the board game not specified")
        elif "no_lives" not in game_settings:
            raise Exception("Number of lives for the player in the game not specified")

        no_lines = game_settings["no_lines"]
        no_columns = game_settings["no_columns"]
        no_lives = game_settings["no_lives"]

        self.no_lines = no_lines
        self.no_columns = no_columns

        self.level = 1
        self.score = 0
        self.no_lives = no_lives

        self.no_lives_left = no_lives
        self.no_cells_left = no_lines * no_columns

        self.board = Game.generate_board(no_lines, no_columns, self.level + 1)

    @staticmethod
    def generate_board(no_lines, no_columns, no_different_pieces):
        """
        Construct the board with the following values:
        -1 : empty
        0 : the piece of type 0
        1 : the piece of type 1
        ...
        and has these values from [0,no_different_pieces)
        :param no_lines: number of lines for the board
        :param no_columns: number of columns for the board
        :param no_different_pieces: the number of different pieces on the board
        :return: the generated board
        """

        board = [[random.randint(0, no_different_pieces - 1) for column in range(no_columns)] for line in
                 range(no_lines)]

        return board

    def game_over(self):
        return self.level == MAX_LEVEL or self.no_lives_left <= 0

    def act(self, line, column):
        if self.outside_board(line, column) or self.board[line][column] == -1:
            return False

        # visit the neighbors of each cell using a queue
        queue = Queue(self.no_lines * self.no_columns)
        queue.put((line, column))

        # delete the cell that are of the same type as the clicked cell
        visited = [[False for column in range(self.no_columns)] for line in range(self.no_lines)]

        no_visited_cells = 0
        cell_type = self.board[line][column]

        while not queue.empty():
            current_line, current_column = queue.get()
            if not visited[current_line][current_column]:

                visited[current_line][current_column] = True
                self.board[current_line][current_column] = -1

                no_visited_cells += 1

                for index in range(NO_NEIGHBOURS):
                    new_line = current_line + LINE_VALUES[index]
                    new_column = current_column + COLUMN_VALUES[index]

                    if not self.outside_board(new_line, new_column) and self.board[new_line][new_column] == cell_type:
                        queue.put((new_line, new_column))

        # update board after we removed at least one block

        # update board from top to bottom

        for column in range(self.no_columns):
            values = [-1 for line in range(self.no_lines)]
            index = 0
            for line in range(self.no_lines - 1, -1, -1):
                # get the new values in order
                value = self.board[line][column]
                if value != -1:
                    values[index] = value
                    index += 1

            # update column
            for index in range(self.no_lines):
                self.board[self.no_lines - index - 1][column] = values[index]

        # update board from left to right

        last_line = self.no_lines - 1
        column = self.no_columns - 1
        while column > 0:
            # we have a column that is empty in front of the column that isn't empty,swap their values
            if column < self.no_columns and self.board[last_line][column - 1] != -1 \
                    and self.board[last_line][column] == -1:
                for line in range(self.no_lines):
                    self.board[line][column - 1], self.board[line][column] = self.board[line][column], self.board[line][
                        column - 1]
                column += 1
            else:
                column -= 1

        # update game info

        self.score += no_visited_cells * self.level * BLOCK_VALUE

        if no_visited_cells == 1:
            self.no_lives_left -= 1

        self.no_cells_left -= no_visited_cells

        if self.no_lives_left > 0 and self.no_cells_left == 0:
            self.no_cells_left = self.no_lines * self.no_columns
            self.level += 1
            self.board = Game.generate_board(self.no_lines, self.no_columns, self.level + 1)

        return True

    def outside_board(self, line, column):
        return line < 0 or line >= self.no_lines or column < 0 or column >= self.no_columns

    def reset_game(self):
        self.no_cells_left = self.no_lines * self.no_columns
        self.level = 1
        self.score = 0
        self.no_lives_left = self.no_lives

        self.board = Game.generate_board(self.no_lines, self.no_columns, self.level + 1)

    def print(self):
        print("No lines: ", self.no_lines)
        print("No columns: ", self.no_columns)
        print("No of total lives: ", self.no_lives)
        print("No of lives left: ", self.no_lives_left)
        print("Score: ", self.score)

        print("Board:")
        for line in range(self.no_lines):
            print(self.board[line])

        print("Game over? ", self.game_over())


if __name__ == "__main__":
    game = Game(6, 6, 3)
    game.print()

    while True:
        x = int(input("line = "))
        y = int(input("column = "))
        game.act(x, y)
        game.print()

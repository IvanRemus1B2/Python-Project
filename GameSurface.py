import os

import pygame
from pygame import Surface
from Game import Game

LIVES_IMAGE = pygame.image.load(os.path.join("images", "life.png"))

TEXT_COLOR = (0, 0, 0)


class GameSurface:
    def __init__(self, width, height, game_settings: dict, background_color):
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
        self.cell_coords = []
        for line in range(self.no_lines):
            line_coords = []
            for column in range(self.no_columns):
                line_coords.append((self.board_x + column * self.cell_width, self.board_y + line * self.cell_height))
            self.cell_coords.append(line_coords)

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

    def draw_level(self):
        level_text = self.font.render("LEVEL : " + str(self.game.level), True, TEXT_COLOR)
        text_rect = level_text.get_rect()
        text_rect.center = (self.level_width / 2, self.level_height / 2)

        self.surface.blit(level_text, text_rect)

    def draw_board(self):
        # draw the board
        board = self.game.board
        for line in range(self.no_lines):
            for column in range(self.no_columns):
                x, y = self.cell_coords[line][column]
                value = board[line][column]
                if value != -1:
                    self.surface.blit(self.hieroglyphs[value], (x, y))

    def draw_info(self):
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

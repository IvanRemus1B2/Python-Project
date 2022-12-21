import pygame

from pygame.locals import *

import os

import Game
from Button import Button
from GameSurface import GameSurface
from InformativeMessageSurface import InformativeMessageSurface

GAME_NAME = "Stones of the Pharaoh"

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

GAME_WIDTH = 400
GAME_HEIGHT = 600

INFORMATIVE_MESSAGE_WIDTH = 300
INFORMATIVE_MESSAGE_HEIGHT = 300

INFORMATIVE_MESSAGE_X = (SCREEN_WIDTH - INFORMATIVE_MESSAGE_WIDTH) // 2
INFORMATIVE_MESSAGE_Y = (SCREEN_HEIGHT - INFORMATIVE_MESSAGE_HEIGHT) // 2

GAME_X = (SCREEN_WIDTH - GAME_WIDTH) / 2
GAME_Y = 100

WHITE = (255, 255, 255)
YELLOW = (211, 222, 7)
AQUA = (255, 87, 51)
BLACK = (0, 0, 0)
TANGERINE = (255, 204, 0)
ORANGE = (255, 128, 0)

FPS = 60


def start_game():
    pygame.init()

    # draw surfaces
    menu_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # game background image
    background_image = pygame.image.load(os.path.join("images", "bg_menu.jpg"))
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    menu_surface.blit(background_image, (0, 0))

    # game window surface which will have the buttons and the game interaction
    game_window_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_window_surface.fill(AQUA)

    # game surface,to include the board,score,lives left and level
    game_settings = {"no_lines": 10, "no_columns": 10, "no_lives": 3}
    game = GameSurface(GAME_X, GAME_Y, GAME_WIDTH, GAME_HEIGHT, game_settings, TANGERINE)

    # game_over object to get the surface required
    game_over_surface = InformativeMessageSurface(INFORMATIVE_MESSAGE_WIDTH, INFORMATIVE_MESSAGE_HEIGHT, ORANGE)

    current_surface = 1

    play_button = Button(SCREEN_WIDTH / 2 - 100 / 2, SCREEN_HEIGHT - 50 - 50 / 2, 100, 50, ORANGE, "Play", 30, WHITE)
    back_button = Button(SCREEN_WIDTH - 100, 25, 75, 50, ORANGE, "Back", 30, WHITE)

    play_button.draw(menu_surface)
    back_button.draw(game_window_surface)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # game name
    pygame.display.set_caption(GAME_NAME)

    # game icon
    icon = pygame.image.load(os.path.join("images", "icons8-pharaoh-32.png"))
    pygame.display.set_icon(icon)

    # clock of the game
    clock = pygame.time.Clock()

    # Run the game
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                if current_surface == 1:
                    # at the menu
                    pressed_play_button = play_button.pressed(mouse_position)
                    if pressed_play_button:
                        game.reset()
                        game_window_surface.blit(game.surface, (GAME_X, GAME_Y))
                        current_surface = 3 - current_surface
                elif current_surface == 2:
                    # at the game
                    pressed_back_button = back_button.pressed(mouse_position)
                    if pressed_back_button:
                        current_surface = 3 - current_surface
                    elif not game.updating_down and not game.updating_right:
                        # if the game cells are still moving,don't update anything
                        # no buttons pressed,check for a click on the cells of the board
                        game.act(mouse_position)
                        game_window_surface.blit(game.surface, (GAME_X, GAME_Y))
                        if game.game_over():
                            current_surface = 3

                            # update the game over surface
                            game_over_surface.reset()
                            game_over_surface.write_text("GAME OVER", 50, WHITE)
                            game_over_surface.write_text("Final score : " + str(game.get_score()), 30, WHITE)

                            # encouraging message
                            text = "Keep it up!"
                            level = game.game.level
                            if level >= Game.MAX_LEVEL:
                                text = "Good job!You got them all!"
                            game_over_surface.write_text(text, 30, WHITE)

                elif current_surface == 3:
                    current_surface = 1
            else:
                if current_surface == 2:
                    # if the mouse position hovers over any cell,highlight the cells
                    mouse_position = pygame.mouse.get_pos()

                    game.highlight_possible_deleted_cells(mouse_position)
                    game_window_surface.blit(game.surface, (GAME_X, GAME_Y))

        if current_surface == 1:
            screen.blit(menu_surface, (0, 0))
        elif current_surface == 2:
            # if the game still have moving cells,continue updating it
            if game.updating_down or game.updating_right:
                game.update_coords()
                game_window_surface.blit(game.surface, (GAME_X, GAME_Y))
            screen.blit(game_window_surface, (0, 0))
        elif current_surface == 3:
            screen.blit(game_window_surface, (0, 0))
            screen.blit(game_over_surface.surface, (INFORMATIVE_MESSAGE_X, INFORMATIVE_MESSAGE_Y))
        else:
            raise Exception("Unknown surface when trying to update")

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    start_game()

import pygame

from pygame.locals import *

import os

from Button import Button

GAME_NAME = "Stones of the Pharaoh"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

WHITE = (255, 255, 255)
YELLOW = (211, 222, 7)
AQUA = (255, 87, 51)
BLACK = (0, 0, 0)

FPS = 60


def start_game():
    pygame.init()

    surface1 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface1.fill(YELLOW)

    surface2 = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface2.fill(AQUA)

    current_surface = 1

    play_button = Button(SCREEN_WIDTH / 2 - 100 / 2, SCREEN_HEIGHT - 50 - 50 / 2, 100, 50, WHITE, "Play", 30, YELLOW)
    back_button = Button(SCREEN_WIDTH - 100, 25, 75, 50, BLACK, "Back", 30, YELLOW)

    play_button.draw(surface1)
    back_button.draw(surface2)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # game name
    pygame.display.set_caption(GAME_NAME)

    # game icon
    icon = pygame.image.load(os.path.join("images", "icons8-pharaoh-32.png"))
    pygame.display.set_icon(icon)

    # TODO:How to add background image?
    # game background image
    # background_image = pygame.image.load(os.path.join("images", "pyramids.png"))
    # background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # screen.blit(background_image, (0, 0))

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
                left, middle, right = pygame.mouse.get_pressed()
                mouse_position = pygame.mouse.get_pos()

                if play_button.pressed(mouse_position) or back_button.pressed(mouse_position):
                    current_surface = 3 - current_surface

                # print(mouse_position)
                # if left and play_button.mouse_hovers_over(mouse_position):
                #     print("Button play was pressed")

        if current_surface == 1:
            screen.blit(surface1, (0, 0))
        elif current_surface == 2:
            screen.blit(surface2, (0, 0))
        else:
            raise Exception("Unknown surface")

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    start_game()

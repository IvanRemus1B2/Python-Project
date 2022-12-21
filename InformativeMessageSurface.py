import pygame

INITIAL_X_POSITION = 40
INITIAL_Y_POSITION = 30
SPACE_BETWEEN = 40


class InformativeMessageSurface:
    def __init__(self, width, height, background_color):
        self.width = width
        self.height = height

        self.background_color = background_color

        self.surface = pygame.Surface((width, height))
        self.surface.fill(background_color)

        self.free_x_position = INITIAL_X_POSITION
        self.free_y_position = INITIAL_Y_POSITION

    def write_text(self, text, font_size, text_color):
        font = pygame.font.SysFont("Roboto", font_size)
        text_drawing = font.render(text, True, text_color)
        self.surface.blit(text_drawing, (self.free_x_position, self.free_y_position))

        sizes = text_drawing.get_size()

        self.free_y_position += sizes[1] + SPACE_BETWEEN

    def reset(self):
        self.surface.fill(self.background_color)
        self.free_x_position = INITIAL_X_POSITION
        self.free_y_position = INITIAL_Y_POSITION

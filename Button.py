import pygame


class Button:
    def __init__(self, x, y, width, height, background_color, button_text, text_size, text_color, draw_border=False,
                 border_color=(0, 0, 0), border_thickness=1):

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_surface.fill(background_color)

        font = pygame.font.SysFont("Arial", text_size)
        self.button_text = font.render(button_text, True, text_color)

        self.button_rect = self.button_text.get_rect()
        self.button_rect.center = (width / 2, height / 2)

        self.button_surface.blit(self.button_text, self.button_rect)

        # border settings
        self.draw_border = draw_border
        self.border_color = border_color
        self.border_thickness = border_thickness

    def draw(self, screen):
        screen.blit(self.button_surface, (self.x, self.y))
        if self.draw_border:
            pygame.draw.rect(screen, self.border_color, [self.x, self.y, self.width, self.height],
                             self.border_thickness)

    def pressed(self, position):
        return self.x <= position[0] <= (self.x + self.width) and self.y <= position[1] <= (self.y + self.height)

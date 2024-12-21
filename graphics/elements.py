import pygame

from graphics.common import GRAY, BLACK, FONT


class InputField:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.text = ''
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = BLACK if self.active else GRAY

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN:
                self.text += event.unicode

    def draw(self, surface):
        rect_width = 2
        pygame.draw.rect(surface, self.color, self.rect, rect_width)

        text_surface = FONT.render(self.text, True, BLACK)
        text_padding = 5
        surface.blit(text_surface, (self.rect.x + text_padding, self.rect.y + text_padding))


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def handle_event(self, event):
        # To be implemented
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect)

        text_surface = FONT.render(self.text, True, BLACK)
        text_padding = 5
        surface.blit(text_surface, (self.rect.x + text_padding, self.rect.y + text_padding))

import pygame

from graphics.common import GRAY, BLACK, FONT, dance_button_image, SCREEN_WIDTH, DANCE_BUTTON_WIDTH, MAROON


class InputField:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = GRAY
        self.text = ""
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
        surface.blit(
            text_surface, (self.rect.x + text_padding, self.rect.y + text_padding)
        )


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
        surface.blit(
            text_surface, (self.rect.x + text_padding, self.rect.y + text_padding)
        )


class DanceButton:
    def __init__(self):
        padding = 15
        height = dance_button_image.get_height()
        self.rect = pygame.Rect(SCREEN_WIDTH - padding - DANCE_BUTTON_WIDTH, padding, DANCE_BUTTON_WIDTH, height)

    def draw(self, surface, is_dancing):

        if is_dancing:
            pygame.draw.rect(surface, MAROON, self.rect, border_radius=8)

            text_surface = FONT.render("Stop", True, BLACK)
            text_padding = 15
            surface.blit(
                text_surface, (self.rect.x + text_padding, self.rect.y + text_padding)
            )
        else:
            surface.blit(
                dance_button_image, (self.rect.x, self.rect.y)
            )

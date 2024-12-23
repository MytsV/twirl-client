import pygame

from graphics.common import (
    BLACK,
    MAIN_FONT,
    dance_button_image,
    SCREEN_WIDTH,
    DANCE_BUTTON_WIDTH,
    MAROON,
    LAVENDER,
    BLUE,
    TEXT_COLOR,
    HINT_COLOR,
    MANTLE,
    DETAILS_FONT,
)

BORDER_RADIUS = 5


class InputField:
    def __init__(self, x, y, width, height, hint):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = TEXT_COLOR
        self.hint = hint
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = BLUE if self.active else TEXT_COLOR

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key != pygame.K_RETURN:
                self.text += event.unicode

    def draw(self, surface):
        pygame.draw.rect(
            surface, self.color, self.rect, width=2, border_radius=BORDER_RADIUS
        )

        if self.text:
            text_surface = MAIN_FONT.render(self.text, True, TEXT_COLOR)
        else:
            text_surface = MAIN_FONT.render(self.hint, True, HINT_COLOR)

        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 14))


class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def handle_event(self, event):
        # To be implemented
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, LAVENDER, self.rect, border_radius=BORDER_RADIUS)

        text_surface = MAIN_FONT.render(self.text, True, MANTLE)
        surface.blit(text_surface, (self.rect.x + 10, self.rect.y + 14))


class DanceButton:
    def __init__(self):
        padding = 15
        height = dance_button_image.get_height()
        self.rect = pygame.Rect(
            SCREEN_WIDTH - padding - DANCE_BUTTON_WIDTH,
            padding,
            DANCE_BUTTON_WIDTH,
            height,
        )

    def draw(self, surface, is_dancing):

        if is_dancing:
            pygame.draw.rect(surface, MAROON, self.rect, border_radius=8)

            text_surface = MAIN_FONT.render("Stop", True, BLACK)
            text_padding = 15
            surface.blit(
                text_surface, (self.rect.x + text_padding, self.rect.y + text_padding)
            )
        else:
            surface.blit(dance_button_image, (self.rect.x, self.rect.y))


def draw_song_name(surface, name):
    text_surface = DETAILS_FONT.render(f"♪ {name} ♪", True, TEXT_COLOR)
    text_width = text_surface.get_width()
    surface.blit(text_surface, ((SCREEN_WIDTH - text_width) // 2, 670))


def draw_location_name(surface, name):
    text_surface = DETAILS_FONT.render(f"{name}", True, TEXT_COLOR)
    text_width = text_surface.get_width()
    surface.blit(text_surface, ((SCREEN_WIDTH - text_width) // 2, 25))

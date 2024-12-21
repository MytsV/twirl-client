import pygame

from graphics.common import WHITE, RED, GRAY
from graphics.elements import InputField, Button
from network.auth import login
from network.udp import initialize_client


class Screen:
    def __init__(self):
        # To be implemented
        pass

    def handle_event(self, event):
        # To be implemented
        pass

    def update(self):
        # To be implemented
        pass

    def draw(self, surface):
        # To be implemented
        pass


class LoginScreen(Screen):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.username_field = InputField(100, 100, 200, 40)
        self.password_field = InputField(100, 150, 200, 40)
        self.login_button = Button(100, 200, 200, 40, "Login")
        self.error = None

    def handle_event(self, event):
        self.username_field.handle_event(event)
        self.password_field.handle_event(event)

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and self.login_button.rect.collidepoint(event.pos)
        ):
            username = self.username_field.text
            password = self.password_field.text
            try:
                response, error = login(username, password)
                self.error = error
                if response:
                    self.screen_manager.set_credentials(response)
                    self.screen_manager.set_screen(DanceFloorScreen(self.screen_manager))
            except:
                print("Fatal error on sign in.")

    def draw(self, surface):
        surface.fill(WHITE)
        self.username_field.draw(surface)
        self.password_field.draw(surface)
        self.login_button.draw(surface)

        if self.error:
            error_font = pygame.font.Font(None, 20)
            error_surface = error_font.render(self.error, True, RED)
            surface.blit(error_surface, (100, 250))


class DanceFloorScreen(Screen):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        initialize_client(self.screen_manager.user_id, self.screen_manager.token)

    def draw(self, surface):
        surface.fill(GRAY)


# TODO: display the login screen if there are no credentials
class ScreenManager:
    def __init__(self):
        self.current_screen = None
        self.user_id = None
        self.token = None

    def set_screen(self, screen):
        self.current_screen = screen

    def handle_event(self, event):
        if self.current_screen:
            self.current_screen.handle_event(event)

    def update(self):
        if self.current_screen:
            self.current_screen.update()

    def draw(self, surface):
        if self.current_screen:
            self.current_screen.draw(surface)

    def set_credentials(self, response):
        self.user_id = response["userId"]
        self.token = response["token"]

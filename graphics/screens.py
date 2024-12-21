import pygame

from graphics.common import WHITE, RED
from graphics.elements import InputField, Button
from network.auth import login


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

        if event.type == pygame.MOUSEBUTTONDOWN and self.login_button.rect.collidepoint(event.pos):
            username = self.username_field.text
            password = self.password_field.text
            try:
                response, error = login(username, password)
                self.error = error
                print(response)
            except:
                print('Fatal error on sign in.')
            # response = self.login_to_server(username, password)
            # if response.get("success"):
            #     print("Login Successful!")
            #     self.screen_manager.set_screen(HomeScreen(self.screen_manager))
            # else:
            #     print("Login Failed!")

    def draw(self, surface):
        surface.fill(WHITE)
        self.username_field.draw(surface)
        self.password_field.draw(surface)
        self.login_button.draw(surface)

        if self.error:
            error_font = pygame.font.Font(None, 20)
            error_surface = error_font.render(self.error, True, RED)
            surface.blit(error_surface, (100, 250))


class ScreenManager:
    def __init__(self):
        self.current_screen = None

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

import pygame

from graphics.common import WHITE, RED, GRAY, BLACK
from graphics.elements import InputField, Button
from models import PlayerState, GameState
from network.auth import login
from network.udp import initialize_client, issue_move

from typing import List


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


PLAYER_RADIUS = 15
INTERPOLATION_SPEED = 0.15


def coordinates_to_local(position):
    x = int(position[0] + PLAYER_RADIUS * 2)
    y = int(position[1] + PLAYER_RADIUS * 2)
    return x, y


def coordinates_to_remote(position):
    x = int(position[0] - PLAYER_RADIUS)
    y = int(position[1] - PLAYER_RADIUS)
    return x, y


class Player():
    def __init__(self, state: PlayerState):
        self.user_id = state.user_id
        self.is_main = state.is_main
        self.shadow = (state.longitude, state.latitude)
        self.position = (state.longitude, state.latitude)

    def update_state(self, state: PlayerState):
        self.shadow = (state.longitude, state.latitude)

    def _interpolate_position(self):
        shadow_x, shadow_y = self.shadow
        current_x, current_y = self.position

        delta_x = shadow_x - current_x
        delta_y = shadow_y - current_y

        move_x = current_x + delta_x * INTERPOLATION_SPEED
        move_y = current_y + delta_y * INTERPOLATION_SPEED

        self.position = (int(move_x), int(move_y))

    def draw(self, surface):
        self._interpolate_position()
        x, y = coordinates_to_local(self.position)
        color = RED if self.is_main else BLACK
        pygame.draw.circle(surface, color, (x, y), PLAYER_RADIUS)


class DanceFloorScreen(Screen):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.player_elements: List[Player] = []
        self.game_state: GameState | None = None
        initialize_client(self.screen_manager.user_id, self.screen_manager.token, self.update_state)

    def update_state(self, game_state):
        self.game_state = game_state
        self.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = coordinates_to_remote(pygame.mouse.get_pos())
            issue_move(self.screen_manager.user_id, self.screen_manager.token, x, y)

    def _find_player_element(self, user_id):
        for player in self.player_elements:
            if player.user_id == user_id:
                return player
        return None

    def _update_player(self, state: PlayerState):
        player_element = self._find_player_element(state.user_id)
        if player_element:
            player_element.update_state(state)
            return player_element
        else:
            return Player(state)

    def draw(self, surface):
        surface.fill(GRAY)

        if self.game_state:
            new_player_elements = []
            for player in self.game_state.players:
                player_element = self._update_player(player)
                new_player_elements.append(player_element)
            self.player_elements = new_player_elements

            for player_element in self.player_elements:
                player_element.draw(surface)

        pygame.display.flip()


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

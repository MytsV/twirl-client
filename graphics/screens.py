import os
import time

import pygame

from graphics.common import WHITE, RED, BLACK, MANTLE, LAVENDER, YELLOW, BLUE, MAROON
from graphics.elements import InputField, Button
from models import PlayerState, GameState, SongState
from network.auth import login
from network.udp import initialize_client, issue_move, change_status

from typing import List

from enum import Enum


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
                    self.screen_manager.set_screen(
                        DanceFloorScreen(self.screen_manager)
                    )
            except:
                print("Fatal error on sign in.")

    def draw(self, surface):
        surface.fill(LAVENDER)
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


class Player:
    def __init__(self, state: PlayerState):
        self.state = state
        self.user_id = state.user_id
        self.position = (state.longitude, state.latitude)

    def update_state(self, state: PlayerState):
        self.state = state

    def _interpolate_position(self):
        shadow_x, shadow_y = (self.state.longitude, self.state.latitude)
        current_x, current_y = self.position

        delta_x = shadow_x - current_x
        delta_y = shadow_y - current_y

        move_x = current_x + delta_x * INTERPOLATION_SPEED
        move_y = current_y + delta_y * INTERPOLATION_SPEED

        self.position = (int(move_x), int(move_y))

    def draw(self, surface):
        self._interpolate_position()
        x, y = coordinates_to_local(self.position)
        color = RED if self.state.is_main else BLACK
        pygame.draw.circle(surface, color, (x, y), PLAYER_RADIUS)

        username_font = pygame.font.Font(None, 20)
        username_text = username_font.render(self.state.username, True, color)
        text_width, text_height = username_text.get_size()

        text_x = x - text_width // 2
        text_y = y - PLAYER_RADIUS - text_height - 5

        surface.blit(username_text, (text_x, text_y))


def play_song(song: SongState, start=0):
    song_path = f"assets/songs/{song.id}.mp3"

    if os.path.exists(song_path):
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(start=start)
    else:
        print(f"Song {song.id} not found!")


class ArrowCircle:
    def __init__(self, x, y, direction_code, radius=40):
        self.x = x
        self.y = y
        self.radius = radius
        self.direction_code = direction_code
        self.pressed = False
        self.arrow_symbols = ["←", "↑", "→", "↓"]
        self.font = pygame.font.Font(pygame.font.match_font("arial"), 40)

    def get_arrow_symbol(self):
        inverted = self.direction_code < 0
        index = abs(self.direction_code)
        symbol = self.arrow_symbols[index]
        if inverted:
            symbol = symbol.lower()
        return symbol

    def draw(self, surface):
        unpressed_color = BLUE if self.direction_code >= 0 else MAROON
        circle_color = YELLOW if self.pressed else unpressed_color
        pygame.draw.circle(surface, circle_color, (self.x, self.y), self.radius)

        symbol = self.get_arrow_symbol()
        text = self.font.render(symbol, True, BLACK)
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)


class ArrowDisplay:
    def __init__(
        self,
        screen_width,
        screen_height,
        arrow_combination,
        circle_radius=40,
        spacing=20,
    ):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.arrow_combination = list(map(int, arrow_combination))
        self.circle_radius = circle_radius
        self.spacing = spacing
        self.arrows = []

        self.last_pressed = -1

        self.inverted_mapping = {-0: 2, -1: 3, -2: 0, -3: 1}

        self.key_mapping = {
            pygame.K_LEFT: 0,
            pygame.K_UP: 1,
            pygame.K_RIGHT: 2,
            pygame.K_DOWN: 3,
        }

        self.calculate_positions()

    def calculate_positions(self):
        total_width = (
            len(self.arrow_combination) * (self.circle_radius * 2 + self.spacing)
            - self.spacing
        )
        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height // 2

        for i, direction_code in enumerate(self.arrow_combination):
            x = start_x + i * (self.circle_radius * 2 + self.spacing)
            self.arrows.append(ArrowCircle(x, y, direction_code, self.circle_radius))

    def draw(self, surface):
        for idx in range(len(self.arrows)):
            arrow = self.arrows[idx]
            arrow.pressed = idx <= self.last_pressed
            arrow.draw(surface)

    def handle_keydown(self, key):
        pressed_direction = self.key_mapping.get(key)
        if pressed_direction is None:
            return

        next_index = self.last_pressed + 1

        if next_index < len(self.arrow_combination):
            expected_direction = self.arrow_combination[next_index]
            if expected_direction < 0:
                expected_direction = self.inverted_mapping[expected_direction]

            if pressed_direction == expected_direction:
                self.last_pressed = next_index
            else:
                self.last_pressed = -1


COUNTS_PER_PASS = 8


class Mark(Enum):
    PERFECT = "perfect"
    GOOD = "good"
    BAD = "bad"
    MISS = "miss"


class PlayerStatus(Enum):
    DANCING = "dancing"
    IDLE = "idle"


class BPMBar:
    def __init__(
        self, bar_x: int, bar_y: int, bar_width: int, bpm: int, on_pass, on_start
    ):
        self.bar_x = bar_x
        self.bar_y = bar_y
        self.bar_width = bar_width

        self.ball_radius = 10
        self.ball_position = 0
        self.ball_direction = 1

        self.bpm = bpm
        self.count_duration = (COUNTS_PER_PASS * 60) / bpm
        self.last_song_time = time.time()
        self.on_pass = on_pass
        self.on_start = on_start

        self.mark_boundaries = {
            Mark.PERFECT: (0.73, 0.77),
            Mark.GOOD: (0.71, 0.79),
            Mark.BAD: (0.68, 0.82),
        }

    def update(self):
        elapsed_time = time.time() - self.last_song_time
        progress = (elapsed_time % self.count_duration) / self.count_duration
        self.ball_position = progress
        if self.ball_position >= 0.95:
            self.on_pass()
        if self.ball_position <= 0.05:
            self.on_start()

    def draw(self, surface):
        ball_x = self.bar_x + self.ball_position * self.bar_width
        ball_y = self.bar_y

        pygame.draw.rect(
            surface, WHITE, (self.bar_x, self.bar_y - 10, self.bar_width, 20)
        )

        interval_start_x = (
            self.bar_x + self.mark_boundaries[Mark.BAD][0] * self.bar_width
        )
        interval_end_x = self.bar_x + self.mark_boundaries[Mark.BAD][1] * self.bar_width
        pygame.draw.rect(
            surface,
            LAVENDER,
            (interval_start_x, self.bar_y - 10, interval_end_x - interval_start_x, 20),
        )

        pygame.draw.circle(surface, RED, (int(ball_x), int(ball_y)), self.ball_radius)

    def sync_with_song(self, playback_position: float):
        elapsed_in_count = playback_position % self.count_duration
        self.last_song_time = time.time() - elapsed_in_count

    def set_bpm(self, bpm: int):
        self.bpm = bpm
        self.count_duration = (COUNTS_PER_PASS * 60) / bpm

    def calculate_mark(self):
        for mark, (start, end) in self.mark_boundaries.items():
            if start <= self.ball_position <= end:
                return mark

        return Mark.MISS


class MarkDisplay:
    def __init__(self):
        self.displayed_mark = None
        self.mark_display_start_time = None
        self.duration = 1

    def show_mark(self, mark):
        self.displayed_mark = mark
        self.mark_display_start_time = time.time()

    def is_displaying(self):
        return (
            self.displayed_mark is not None
            and (time.time() - self.mark_display_start_time) <= self.duration
        )

    def clear(self):
        self.displayed_mark = None

    def draw(self, surface):
        if self.is_displaying():
            self._draw_mark(surface, self.displayed_mark)
        else:
            self.clear()

    def _draw_mark(self, surface, mark):
        font = pygame.font.Font(None, 50)
        mark_text = font.render(str(mark), True, RED)
        surface.blit(mark_text, (400, 300))


class DanceFloorScreen(Screen):
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.player_elements: List[Player] = []
        self.game_state: GameState | None = None
        self.bpm_bar: BPMBar | None = None
        self.arrow_display = None
        self.mark_display = MarkDisplay()

        self.status_button = Button(550, 60, 200, 40, "Status")

        initialize_client(
            self.screen_manager.user_id, self.screen_manager.token, self.update_state
        )

    def _on_pass(self):
        if self.arrow_display:
            self.arrow_display = None
            self.mark_display.show_mark(Mark.MISS)

    def _on_start(self):
        if self.game_state.arrow_combination and not self.arrow_display:
            self.arrow_display = ArrowDisplay(
                800, 800, self.game_state.arrow_combination
            )

    def _update_song(self, song):
        current_time = time.time()
        elapsed_time = current_time - song.start_timestamp / 1000
        play_song(song, elapsed_time)

        self.bpm_bar = BPMBar(400, 500, 200, song.bpm, self._on_pass, self._on_start)

        playback_position = max(0, elapsed_time - song.onset)
        self.bpm_bar.sync_with_song(playback_position)

    def update_state(self, game_state):
        if game_state and game_state.song:
            if (
                not self.game_state
                or not self.game_state.song
                or game_state.song.id != self.game_state.song.id
            ):
                self._update_song(game_state.song)

        self.game_state = game_state
        self.update()

    def _handle_space_down(self):
        mark = self.bpm_bar.calculate_mark()

        is_combination_complete = (
            self.arrow_display.last_pressed
            == len(self.arrow_display.arrow_combination) - 1
        )
        self.arrow_display = None

        if not is_combination_complete:
            mark = Mark.MISS

        self.mark_display.show_mark(mark)

    def _get_is_dancing(self):
        if not self.game_state:
            return False
        for player in self.game_state.players:
            if player.is_main:
                return player.status == PlayerStatus.DANCING.value
        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.status_button.rect.collidepoint(event.pos):
                is_dancing = self._get_is_dancing()
                new_status = PlayerStatus.IDLE if is_dancing else PlayerStatus.DANCING
                change_status(self.screen_manager.user_id, self.screen_manager.token, new_status.value)
            else:
                x, y = coordinates_to_remote(pygame.mouse.get_pos())
                issue_move(self.screen_manager.user_id, self.screen_manager.token, x, y)
        elif event.type == pygame.KEYDOWN and self.arrow_display:
            pressed_key = event.key
            if pressed_key == pygame.K_SPACE:
                self._handle_space_down()
            else:
                self.arrow_display.handle_keydown(pressed_key)

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
        surface.fill(MANTLE)

        is_dancing = self._get_is_dancing()

        if self.game_state:
            new_player_elements = []
            for player in self.game_state.players:
                player_element = self._update_player(player)
                new_player_elements.append(player_element)
            self.player_elements = new_player_elements

            for player_element in self.player_elements:
                player_element.draw(surface)

            self.status_button.draw(surface)

        if is_dancing:
            if self.bpm_bar:
                self.bpm_bar.update()
                self.bpm_bar.draw(surface)

            if self.arrow_display:
                self.arrow_display.draw(surface)

            self.mark_display.draw(surface)

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

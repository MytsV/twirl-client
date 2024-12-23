import pygame

# From catppuccin theme
MAUVE = (203, 166, 247)
MAROON = (235, 160, 172)
YELLOW = (249, 226, 175)
GREEN = (166, 227, 161)
TEAL = (148, 226, 213)
BLUE = (137, 180, 250)
LAVENDER = (180, 190, 254)
MANTLE = (24, 24, 37)

BAR_COLOR = (73, 77, 100)

TEXT_COLOR = (198, 208, 245)
HINT_COLOR = (131, 139, 167)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)


def scale_by_height(image: pygame.Surface, new_height: int) -> pygame.Surface:
    original_width = image.get_width()
    original_height = image.get_height()

    new_width = int(original_width * (new_height / original_height))

    scaled_image = pygame.transform.scale(image, (new_width, new_height))

    return scaled_image


def scale_by_width(image: pygame.Surface, new_width: int) -> pygame.Surface:
    original_width = image.get_width()
    original_height = image.get_height()

    new_height = int(original_height * (new_width / original_width))

    scaled_image = pygame.transform.scale(image, (new_width, new_height))

    return scaled_image


pygame.init()

MAIN_FONT = pygame.font.Font(None, 32)
DETAILS_FONT = pygame.font.Font(pygame.font.match_font("arial"), 20)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

blob_image_unprocessed = pygame.image.load('./assets/images/blob.png')
PLAYER_HEIGHT = 125
blob_image = scale_by_height(blob_image_unprocessed, PLAYER_HEIGHT)
blob_image_pressed = scale_by_height(blob_image_unprocessed, PLAYER_HEIGHT + 10)

sad_face_image = pygame.image.load('./assets/images/sad_face.png')
sad_face_image = scale_by_width(sad_face_image, blob_image.get_width() - 30)

neutral_face_image = pygame.image.load('./assets/images/neutral_face.png')
neutral_face_image = scale_by_width(neutral_face_image, blob_image.get_width() - 30)

happy_face_image = pygame.image.load('./assets/images/happy_face.png')
happy_face_image = scale_by_height(happy_face_image, 50)

DANCE_BUTTON_WIDTH = 250
dance_button_image = pygame.image.load('./assets/images/dance_button.png')
dance_button_image = scale_by_width(dance_button_image, DANCE_BUTTON_WIDTH)

LOGO_WIDTH = 600
logo_image = pygame.image.load('./assets/images/logo.png')
logo_image = scale_by_width(logo_image, LOGO_WIDTH)

mark_overlay_image = pygame.image.load('./assets/images/mark_overlay.png')

move_icon_image = pygame.image.load('./assets/images/move_icon.png')
move_icon_image = scale_by_width(move_icon_image, 30)
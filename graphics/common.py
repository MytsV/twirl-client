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
FONT = pygame.font.Font(None, 32)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

blob_image = pygame.image.load('./assets/images/blob.png')
PLAYER_HEIGHT = 125
blob_image = scale_by_height(blob_image, PLAYER_HEIGHT)

happy_face_image = pygame.image.load('./assets/images/neutral_face.png')
happy_face_image = scale_by_width(happy_face_image, blob_image.get_width() - 30)

DANCE_BUTTON_WIDTH = 250
dance_button_image = pygame.image.load('./assets/images/dance_button.png')
dance_button_image = scale_by_width(dance_button_image, DANCE_BUTTON_WIDTH)

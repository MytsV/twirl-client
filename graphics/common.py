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

pygame.init()
FONT = pygame.font.Font(None, 32)

blob_image = pygame.image.load('./assets/images/blob.png')
PLAYER_HEIGHT = 150
blob_image = pygame.transform.scale(blob_image, (100, PLAYER_HEIGHT))

happy_face_image = pygame.image.load('./assets/images/neutral_face.png')
happy_face_image = pygame.transform.scale(happy_face_image, (75, 30))

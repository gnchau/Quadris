import pygame


class visuals:
    """
    Stores variables for the visual view class
    """
    pygame.font.init()
    font_path = './assets/OpenSans-Light.ttf'
    font_path_b = './assets/OpenSans-Bold.ttf'

    font_light = pygame.font.Font(font_path, 20)
    font_bold = pygame.font.Font(font_path_b, 20)

    black = (10, 10, 10)
    white = (255, 255, 255)
    grey_1 = (26, 26, 26)
    grey_2 = (35, 35, 35)
    grey_3 = (55, 55, 55)

    # Tetrimino colors
    cyan = (69, 206, 204)  # I
    blue = (64, 111, 249)  # J
    orange = (253, 189, 53)  # L
    yellow = (246, 227, 90)  # O
    green = (98, 190, 68)  # S
    pink = (242, 64, 235)  # T
    red = (225, 13, 27)  # Z

    COLOR_MAP = {
        1: (69, 206, 204),
        2: (246, 227, 90),
        3: (242, 64, 235),
        4: (98, 190, 68),
        5: (225, 13, 27),
        6: (64, 111, 249),
        7: (253, 189, 53)
    }

    OFFSET_MAP = {
        1: (-0.5, -0.5),
        2: (-0.5, 0),
        3: (0, -1),
        4: (0, -1),
        5: (0, -1),
        6: (0, -1),
        7: (0, -1),
    }
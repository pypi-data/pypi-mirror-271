"""constants.py: Constants for the application."""


class Constants:
    """
    Constants for the application.

    Notes
    -----
    This class contains constants used throughout the application.
    By storing constants in a single location, it is easier to
    manage and update them. Constants should be defined as class
    attributes and should be named in uppercase with underscores
    separating words.
    """

    # Logging constants
    LOGGING_LEVEL_DEFAULT = "INFO"
    LOGGING_FORMAT = "%(message)s"
    LOGGING_DATE_FORMAT = "[%X]"
    LOGGING_TRACEBACKS = True

    # Colors
    EMPTY_COLOUR = (51, 51, 51)
    BACKGROUND_COLOUR = (51, 51, 51)
    FONT_COLOUR = (214, 214, 214)
    CORRECT_COLOUR = (93, 162, 113)
    POSITION_COLOUR = (242, 129, 35)
    WRONG_COLOUR = (128, 128, 128)

    # Pygame settings
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
    CELL_WIDTH_DIVISOR = 10  # division of screen width for cell width
    CELL_HEIGHT_DIVISOR = 10  # division of screen height for cell height
    FONT_DIVISOR = 1  # division of screen width for font size
    GRID_X_ACROSS = 2
    GRID_Y_DOWN = 1
    KEY_WIDTH_DIVISOR = 30  # division of screen width for key width
    KEY_HEIGHT_DIVISOR = 30  # division of screen height for key height
    KEYBOARD_Y_DOWN = 25
    POPUP_FONT_SIZE = 30
    FPS = 60

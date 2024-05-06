"""graphical_menu.py: Contains the graphical menu for the games."""

import sys

import pygame

from ..config.constants import Constants
from ..logs.setup_logging import setup_logging

interface_logger = setup_logging()

# TODO: Refactor this code to use a class-based approach


def draw_text(
    text: str,
    font: pygame.font.Font,
    color: tuple,
    surface: pygame.Surface,
    x: int,
    y: int,
) -> None:
    """
    Draw text on the screen.

    Parameters
    ----------
    text : str
        The text to display.
    font : pygame.font.Font
        The font to use.
    color : tuple
        The color of the text.
    surface : pygame.Surface
        The Pygame surface.
    x : int
        The x-coordinate of the text.
    y : int
        The y-coordinate of the text.

    Examples
    --------
    >>> draw_text("Hello, World!", font, (255, 255, 255), screen, 50, 50)

    Notes
    -----
    This function draws text on the screen using Pygame.
    """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def gui_leaderboard(screen: pygame.Surface, font: pygame.font.Font, games: dict) -> None:
    """
    Display the leaderboard in a graphical interface.

    Parameters
    ----------
    screen : pygame.Surface
        The Pygame surface.
    font : pygame.font.Font
        The font to use.
    games : dict
        A dictionary of games.

    Examples
    --------
    >>> gui_leaderboard(screen, font, games)

    Notes
    -----
    This function displays the leaderboard in a graphical interface using Pygame.
    """
    running = True
    while running:
        screen.fill(Constants.BACKGROUND_COLOUR)
        draw_text(
            "Leaderboards:", font, Constants.FONT_COLOUR, screen, 20, 20
        )  # TODO: Fix magic numbers throughout the code

        y = 60
        for game in games.values():
            if game:
                try:
                    score_text = f"{game.__name__()}: {game.score}"
                except AttributeError:
                    score_text = f"{game.__name__()}: Unavailable"
            else:
                score_text = "Unavailable"  # TODO: Fix magic strings throughout the code
            draw_text(score_text, font, Constants.FONT_COLOUR, screen, 50, y)
            y += 40

        # Draw Back to Menu button
        back_text = "Back to Menu"
        back_button_y = y + 20  # Positioning the button just below the last score
        draw_text(back_text, font, Constants.FONT_COLOUR, screen, 50, back_button_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # Check if Back to Menu button is clicked
                if 50 <= x <= 350 and back_button_y <= y <= back_button_y + 30:
                    running = False  # Exit leaderboard loop to return to main menu

        pygame.display.update()


def main_menu(games: dict) -> None:
    """
    Display the main menu in a graphical interface.

    Parameters
    ----------
    games : dict
        A dictionary of games.

    Examples
    --------
    >>> main_menu(games)

    Notes
    -----
    This function displays the main menu in a graphical interface using Pygame.
    """
    pygame.init()

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Game Menu")

    font = pygame.font.Font(None, 36)

    running = True
    while running:
        screen.fill(Constants.BACKGROUND_COLOUR)
        draw_text("Choose a game to play:", font, Constants.FONT_COLOUR, screen, 20, 20)

        # Display games as buttons
        button_y = 60
        buttons = []
        for i, game in enumerate(games.keys(), start=1):
            text = f"{i}. {game}" if games[game] else f"{i}. {game} (not available)"
            draw_text(
                text,
                font,
                Constants.FONT_COLOUR if games[game] else Constants.WRONG_COLOUR,
                screen,
                50,
                button_y,
            )
            buttons.append((text, 50, button_y, game))
            button_y += 40

        # Add leaderboard button
        leaderboard_text = "View Leaderboard"
        draw_text(leaderboard_text, font, Constants.FONT_COLOUR, screen, 50, button_y)
        buttons.append((leaderboard_text, 50, button_y, "leaderboard"))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for text, bx, by, game in buttons:
                    if bx <= x <= bx + 300 and by <= y <= by + 30:
                        if game == "leaderboard":
                            gui_leaderboard(screen, font, games)
                        elif games[game]:
                            games[game].play()
                            running = False
                            main_menu(games)

        pygame.display.update()

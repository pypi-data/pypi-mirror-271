"""wordle.py: A game of Wordle, inheriting from the Game class."""

import random

import pygame

from ...config.constants import Constants
from ...config.dialogue_en import DialogueEn
from ...logs.setup_logging import setup_logging
from ..game_infrastructure import Game

wordle_logger = setup_logging()

# TODO: Refactor Wordle to be more readable and maintainable.
# TODO: Implement a second list for possible words.
# TODO: Create parent classes for the Cell and Grid classes.


class Cell:
    """
    A cell in the grid.

    Attributes
    ----------
    letter : str
        The letter in the cell.
    x : int
        The x-coordinate of the cell.
    y : int
        The y-coordinate of the cell.
    width_divisor : int
        The width divisor of the cell.
    height_divisor : int
        The height divisor of the cell.
    font_divisor : int
        The font divisor of the cell.
    colour : tuple[int, int, int]
        The colour of the cell.
    screen : pygame.Surface
        The Pygame screen.
    width : int
        The width of the cell.
    height : int
        The height of the cell.
    font : pygame.font.Font
        The font of the cell.
    needs_redraw : bool
        Whether the cell needs to be redrawn.

    Methods
    -------
    draw() -> pygame.Rect | None:
        Draw the cell.
    update(letter: str, colour: tuple[int, int, int]) -> None:
        Update the cell.

    Examples
    --------
    >>> cell = Cell(screen, letter="a", x=0, y=0)

    Notes
    -----
    This class initialises a cell in the grid.
    """

    def __init__(
        self,
        screen: pygame.Surface,
        letter: str = "",
        x: int = 0,
        y: int = 0,
        divisors: tuple[int, int, int] = (
            Constants.CELL_WIDTH_DIVISOR,
            Constants.CELL_HEIGHT_DIVISOR,
            Constants.FONT_DIVISOR,
        ),
        colour: tuple[int, int, int] = Constants.EMPTY_COLOUR,
    ) -> None:
        """
        Initialise the cell.

        Parameters
        ----------
        screen : pygame.Surface
            The Pygame screen.
        letter : str, optional
            The letter in the cell, by default "".
        x : int, optional
            The x-coordinate of the cell, by default 0.
        y : int, optional
            The y-coordinate of the cell, by default 0.
        divisors : tuple[int, int, int], optional
            divisors: tuple[int, int, int] = (
                Constants.CELL_WIDTH_DIVISOR,
                Constants.CELL_HEIGHT_DIVISOR,
                Constants.FONT_DIVISOR,
            )
        colour : tuple[int, int, int], optional
            The colour of the cell, by default Constants.EMPTY_COLOUR.

        Examples
        --------
        >>> cell = Cell(screen, letter="a", x=0, y=0)

        Notes
        -----
        This class initialises a cell in the grid.
        """
        self.letter = letter
        self.x = x
        self.y = y
        self.width_divisor, self.height_divisor, self.font_divisor = divisors
        self.colour = colour
        self.screen = screen
        self.width = self.screen.get_width() // self.width_divisor
        self.height = self.screen.get_height() // self.height_divisor
        self.font = pygame.font.Font(None, self.height // self.font_divisor)
        self.needs_redraw = True

    def draw(self) -> pygame.Rect | None:
        """
        Draw the cell.

        Returns
        -------
        pygame.Rect | None
            The rectangle of the cell.

        Examples
        --------
        >>> cell.draw()

        Notes
        -----
        This method draws the cell.
        """
        if self.needs_redraw:
            pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height))
            text = self.font.render(self.letter.upper(), True, Constants.FONT_COLOUR)
            text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            self.screen.blit(text, text_rect)
            self.needs_redraw = False
            return pygame.Rect(self.x, self.y, self.width, self.height)

        return None

    def update(self, letter: str, colour: tuple[int, int, int]) -> None:
        """
        Update the cell.

        Parameters
        ----------
        letter : str
            The letter to update the cell with.
        colour : tuple[int, int, int]
            The colour to update the cell with.

        Examples
        --------
        >>> cell.update("a", (255, 255, 255))

        Notes
        -----
        This method updates the cell.
        """
        if self.letter != letter or self.colour != colour:
            self.letter = letter
            self.colour = colour
            self.needs_redraw = True


class Grid:
    """
    A grid of cells.

    Attributes
    ----------
    screen : pygame.Surface
        The Pygame screen.
    cells : list[list[Cell]]
        The list of cells.
    target_word : str
        The target word.
    attempts : int
        The number of attempts.
    current_attempt : int
        The current attempt.

    Methods
    -------
    update_cell(guess: str, letter_tracking: list[Cell]) -> list[Cell]:
        Update the cell.
    resize() -> None:
        Resize the grid.
    draw() -> None:
        Draw the grid.

    Examples
    --------
    >>> grid = Grid(screen, "hello", 6)

    Notes
    -----
    This class initialises the grid of cells.
    """

    def __init__(self, screen: pygame.Surface, target_word: str, attempts: int = 6) -> None:
        """
        Initialise the grid.

        Parameters
        ----------
        screen : pygame.Surface
            The Pygame screen.
        target_word : str
            The target word.
        attempts : int, optional
            The number of attempts, by default 6.

        Examples
        --------
        >>> grid = Grid(screen, "hello", 6)

        Notes
        -----
        This class initialises the grid of cells.
        """
        self.screen = screen
        self.cells = [
            [
                Cell(
                    self.screen,
                    x=Constants.GRID_X_ACROSS
                    * (self.screen.get_width() // Constants.CELL_WIDTH_DIVISOR)
                    + j
                    * (
                        (self.screen.get_width() // Constants.CELL_WIDTH_DIVISOR)
                        + self.screen.get_width() // (Constants.CELL_WIDTH_DIVISOR * 5)
                    ),
                    y=Constants.GRID_Y_DOWN
                    * (self.screen.get_height() // Constants.CELL_HEIGHT_DIVISOR)
                    + i
                    * (
                        (self.screen.get_height() // Constants.CELL_HEIGHT_DIVISOR)
                        + self.screen.get_height() // (Constants.CELL_HEIGHT_DIVISOR * 5)
                    ),
                )
                for j in range(len(target_word))
            ]
            for i in range(attempts)
        ]
        self.target_word = target_word
        self.attempts = attempts
        self.current_attempt = 0

    def update_cell(
        self, guess: str, letter_tracking: dict[str, tuple[int, int, int]]
    ) -> list[Cell]:
        """
        Update the cell.

        Parameters
        ----------
        guess : str
            The guess.
        letter_tracking : dict[str, tuple[int, int, int]]
            The letter tracking.

        Returns
        -------
        list[Cell]
            The updated letter tracking.

        Examples
        --------
        >>> grid.update_cell("hello", {"a": (255, 255, 255)})

        Notes
        -----
        This method updates the cell.
        """
        updated_cells = []
        for i, letter in enumerate(guess):
            cell = self.cells[self.current_attempt][i]
            correct = self.target_word[i] == letter
            if correct:
                new_colour = Constants.CORRECT_COLOUR
            elif letter in self.target_word:
                new_colour = (
                    Constants.POSITION_COLOUR
                    if guess.count(letter) <= self.target_word.count(letter)
                    else Constants.WRONG_COLOUR
                )
            else:
                new_colour = Constants.WRONG_COLOUR

            if cell.letter != letter or cell.colour != new_colour:
                cell.update(letter, new_colour)  # Ensure updates are performed
                updated_cells.append(cell)

        return updated_cells

    def resize(self) -> None:
        """
        Resize the grid.

        Examples
        --------
        >>> grid.resize()

        Notes
        -----
        This method resizes the grid.
        """
        base_x = Constants.GRID_X_ACROSS * (self.screen.get_width() // Constants.CELL_WIDTH_DIVISOR)
        base_y = Constants.GRID_Y_DOWN * (self.screen.get_height() // Constants.CELL_HEIGHT_DIVISOR)
        width_step = self.screen.get_width() // Constants.CELL_WIDTH_DIVISOR
        height_step = self.screen.get_height() // Constants.CELL_HEIGHT_DIVISOR
        width_spacing = width_step // 5
        height_spacing = height_step // 5

        for row in self.cells:
            for cell in row:
                cell.x = base_x + row.index(cell) * (width_step + width_spacing)
                cell.y = base_y + self.cells.index(row) * (height_step + height_spacing)
                cell.width = width_step
                cell.height = height_step
                cell.font = pygame.font.Font(None, cell.height // cell.font_divisor)
                cell.needs_redraw = True

    def draw(self) -> None:
        """
        Draw the grid.

        Examples
        --------
        >>> grid.draw()

        Notes
        -----
        This method draws the grid.
        """
        redraw_rects = [cell.draw() for row in self.cells for cell in row if cell.needs_redraw]
        if redraw_rects:
            pygame.display.update(redraw_rects)


class VirtualKeyboard:
    """
    A virtual keyboard.

    Attributes
    ----------
    screen : pygame.Surface
        The Pygame screen.
    keys : list[Cell]
        The list of keys.

    Methods
    -------
    update_key(letter_tracking: dict[str, tuple[int, int, int]]) -> None:
        Update the key colours.
    resize() -> None:
        Resize the virtual keyboard.
    draw() -> None:
        Draw the virtual keyboard.

    Examples
    --------
    >>> virtual_keyboard = VirtualKeyboard(screen)

    Notes
    -----
    This class initialises the virtual keyboard.
    """

    def __init__(self, screen: pygame.Surface) -> None:
        """
        Initialise the virtual keyboard.

        Parameters
        ----------
        screen : pygame.Surface
            The Pygame screen.

        Examples
        --------
        >>> virtual_keyboard = VirtualKeyboard(screen)

        Notes
        -----
        This class initialises the virtual keyboard.
        """
        self.screen = screen
        self.keys: list[Cell] = []
        rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]

        key_height = screen.get_height() // Constants.KEY_HEIGHT_DIVISOR
        initial_y = Constants.KEYBOARD_Y_DOWN * key_height

        for i, row in enumerate(rows):
            key_width = screen.get_width() // Constants.KEY_WIDTH_DIVISOR
            total_row_width = len(row) * key_width + (len(row) - 1) * (key_width // 5)
            initial_x = (screen.get_width() - total_row_width) // 2

            for j, letter in enumerate(row):
                key = Cell(
                    screen,
                    letter,
                    x=initial_x + j * (key_width + key_width // 5),
                    y=initial_y + i * (key_height + key_height // 5),
                    divisors=(
                        Constants.KEY_WIDTH_DIVISOR,
                        Constants.KEY_HEIGHT_DIVISOR,
                        Constants.FONT_DIVISOR,
                    ),
                    colour=Constants.EMPTY_COLOUR,
                )

                self.keys.append(key)

    def update_key(self, letter_tracking: dict[str, tuple]) -> None:
        """
        Update the key colours.

        Parameters
        ----------
        letter_tracking : dict[str, tuple[int, int, int]]
            The letter tracking.

        Examples
        --------
        >>> virtual_keyboard.update_key({"a": (255, 255, 255)})

        Notes
        -----
        This method updates the key colours.
        """
        for key in self.keys:
            key.colour = letter_tracking[key.letter]

    def resize(self) -> None:
        """
        Resize the virtual keyboard.

        Examples
        --------
        >>> virtual_keyboard.resize()

        Notes
        -----
        This method resizes the virtual keyboard.
        """
        key_height = self.screen.get_height() // Constants.KEY_HEIGHT_DIVISOR
        initial_y = Constants.KEYBOARD_Y_DOWN * key_height

        key_index = 0
        for i, row in enumerate(["qwertyuiop", "asdfghjkl", "zxcvbnm"]):
            key_width = self.screen.get_width() // Constants.KEY_WIDTH_DIVISOR
            total_row_width = len(row) * key_width + (len(row) - 1) * (key_width // 5)
            initial_x = (self.screen.get_width() - total_row_width) // 2

            for j in range(len(row)):
                key: Cell = self.keys[key_index]
                key.x = initial_x + j * (key_width + key_width // 5)
                key.y = initial_y + i * (key_height + key_height // 5)
                key.width = key_width
                key.height = key_height
                key.needs_redraw = True
                key_index += 1

    def draw(self) -> None:
        """
        Draw the virtual keyboard.

        Examples
        --------
        >>> virtual_keyboard.draw()

        Notes
        -----
        This method draws the virtual keyboard.
        """
        for key in self.keys:
            key.draw()
        pygame.display.update()


class Wordle(Game):
    """
    A game of Wordle.

    Attributes
    ----------
    word_list : list[str]
        The list of words to choose from.
    letter_tracking : dict[str, tuple[int, int, int]]
        The letter tracking.

    Methods
    -------
    _init_pygame() -> None:
        Initialise Pygame.
    _draw_text(
        message: str,
        size: int,
        color: tuple[int, int, int],
        center: tuple[int, int],
        duration: int = 2000,
    ) -> None:
        Draw text on the screen.
    _handle_keydown(event: pygame.event.Event, current_guess: list[str]) -> None:
        Handle the keydown event.
    play() -> None:
        Play the Wordle game.

    Examples
    --------
    >>> wordle = Wordle()

    Notes
    -----
    This class represents the Wordle game.
    """

    def __init__(self, word_list: list[str]) -> None:
        """
        Initialise the Wordle game.

        Parameters
        ----------
        word_list : list[str]
            The list of words to choose from.

        Examples
        --------
        >>> wordle = Wordle()

        Notes
        -----
        This class initialises the Wordle game.
        """
        super().__init__(
            DialogueEn.WORDLE_NAME,
            DialogueEn.WORDLE_DESCRIPTION,
            DialogueEn.WORDLE_INSTRUCTIONS,
        )

        self.word_list = word_list
        self.letter_tracking = {
            chr(i): Constants.EMPTY_COLOUR for i in range(ord("a"), ord("z") + 1)
        }

    def _init_pygame(self) -> None:
        """
        Initialise Pygame.

        Examples
        --------
        >>> _init_pygame()

        Notes
        -----
        This method initialises Pygame.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(
            Constants.SCREEN_SIZE, pygame.RESIZABLE | pygame.DOUBLEBUF
        )
        pygame.display.set_caption(self.__name__())
        self.screen.fill(Constants.BACKGROUND_COLOUR)
        pygame.display.update()

    def _draw_text(
        self,
        message: str,
        size: int,
        color: tuple[int, int, int],
        center: tuple[int, int],
        duration: int = 2000,
    ) -> None:
        """
        Draw text on the screen.

        Parameters
        ----------
        message : str
            The message to display.
        size : int
            The font size.
        color : tuple[int, int, int]
            The font colour.
        center : tuple[int, int]
            The center of the text.
        duration : int, optional
            The duration of the text, by default 2000.

        Examples
        --------
        >>> _draw_text("Hello, World!", 24, (255, 255, 255), (100, 100))

        Notes
        -----
        This method draws text on the screen. The text fades in, pauses, and fades out.
        """
        # TODO: Fix text boldening due to not clearing the rect before/after drawing the text.
        # TODO: Implement non-blocking text popup.
        font = pygame.font.Font(None, size)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=center)

        # Fade in parameters
        fade_in_duration = duration // 2
        fade_out_duration = duration // 2
        fade_in_alpha = 0
        fade_out_alpha = 0
        fade_rate = 255 / (fade_in_duration / 1000 * Constants.FPS)

        # Start the fade in effect
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < fade_in_duration:
            fade_in_alpha = min(fade_in_alpha + fade_rate, 255)
            text.set_alpha(fade_in_alpha)
            self.screen.blit(text, text_rect)
            pygame.display.update(text_rect)
            pygame.time.delay(1000 // Constants.FPS)

        # Pause for a moment
        pygame.time.delay(duration // 2)

        # Start the fade out effect with rectangle
        fade_out_start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - fade_out_start_time < fade_out_duration:
            fade_out_alpha = min(fade_out_alpha + fade_rate, 255)
            self.screen.blit(text, text_rect)
            # Cover the text with a rectangle of background color gradually becoming opaque
            overlay_rect = pygame.Surface(text.get_size())
            overlay_rect.fill(Constants.BACKGROUND_COLOUR)
            overlay_rect.set_alpha(fade_out_alpha)
            self.screen.blit(overlay_rect, text_rect)
            pygame.display.update(text_rect)
            pygame.time.delay(1000 // Constants.FPS)

        # Clear the final state
        pygame.display.update(text_rect)  # Update the screen to clear the faded text.

    def _handle_keydown(self, event: pygame.event.Event, current_guess: list[str]) -> None:
        """
        Handle the keydown event.

        Parameters
        ----------
        event : pygame.event.Event
            The Pygame event.
        current_guess : list[str]
            The current guess.

        Examples
        --------
        >>> _handle_keydown(event, current_guess)

        Notes
        -----
        This method handles the keydown event.
        """
        if event.key == pygame.K_RETURN and len(current_guess) == len(self.target_word):
            guess = "".join(current_guess)
            if guess in self.word_list:
                updated_cells = self.grid.update_cell(guess, self.letter_tracking)
                self.virtual_keyboard.update_key(self.letter_tracking)
                self.grid.current_attempt += 1
                current_guess.clear()
                if updated_cells:
                    self.grid.draw()
                if guess == self.target_word:
                    self._draw_text(
                        f"You Win! The word was: {self.target_word}",
                        Constants.POPUP_FONT_SIZE,
                        Constants.FONT_COLOUR,
                        (self.screen.get_width() // 2, self.screen.get_height() // 20),
                    )
                    self.running = False
                elif self.grid.current_attempt == self.grid.attempts:
                    self._draw_text(
                        f"Game Over! The word was: {self.target_word}",
                        Constants.POPUP_FONT_SIZE,
                        Constants.FONT_COLOUR,
                        (self.screen.get_width() // 2, self.screen.get_height() // 20),
                    )
                    self.running = False
            else:
                self._draw_text(
                    "Invalid word",
                    Constants.POPUP_FONT_SIZE,
                    Constants.FONT_COLOUR,
                    (self.screen.get_width() // 2, self.screen.get_height() // 20),
                )
        elif event.key == pygame.K_BACKSPACE and current_guess:
            cell = self.grid.cells[self.grid.current_attempt][len(current_guess) - 1]
            cell.update("", Constants.EMPTY_COLOUR)
            current_guess.pop()
        elif len(current_guess) < len(self.target_word) and event.unicode.isalpha():
            cell = self.grid.cells[self.grid.current_attempt][len(current_guess)]
            cell.update(event.unicode.lower(), Constants.EMPTY_COLOUR)
            current_guess.append(event.unicode.lower())

    def play(self) -> None:
        """
        Play the Wordle game.

        Examples
        --------
        >>> wordle.play()

        Notes
        -----
        This method plays the Wordle game.
        """
        self.target_word = random.choice(self.word_list)
        self._init_pygame()
        self.grid = Grid(self.screen, self.target_word)
        self.virtual_keyboard = VirtualKeyboard(self.screen)

        print(f"Psst.. The word is: {self.target_word}!")  # For testing purposes

        self.running = True
        current_guess: list[str] = []
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode(
                        event.dict["size"], pygame.RESIZABLE | pygame.DOUBLEBUF
                    )
                    self.screen.fill(Constants.BACKGROUND_COLOUR)
                    self.grid.resize()
                    self.virtual_keyboard.resize()
                    self.grid.draw()
                    self.virtual_keyboard.draw()
                elif event.type == pygame.KEYDOWN:
                    self._handle_keydown(event, current_guess)

            self.grid.draw()
            self.virtual_keyboard.draw()

        self.score = self.grid.current_attempt

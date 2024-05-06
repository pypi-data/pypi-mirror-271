"""game_infrastructure.py: Classes for the games to inherit from."""

from ..logs.setup_logging import setup_logging

game_infrastructure_logger = setup_logging()


class Game:
    """
    A class representing a game.

    Parameters
    ----------
    name : str
        The name of the game.
    description : str
        The description of the game.
    instructions : str
        The instructions for the game.

    Methods
    -------
    play()
        Play the game.

    Examples
    --------
    >>> game = Game("Game", "This is a game.", "Instructions for the game.")

    Notes
    -----
    This class initialises the game with a name, description, and instructions.
    """

    def __init__(self, name: str, description: str, instructions: str) -> None:
        """
        Initialise the game.

        Parameters
        ----------
        name : str
            The name of the game.
        description : str
            The description of the game.
        instructions : str
            The instructions for the game.

        Examples
        --------
        >>> game = Game("Game", "This is a game.", "Instructions for the game.")

        Notes
        -----
        This class initialises the game with a name, description, and instructions.
        """
        self.name = name
        self.description = description
        self.instructions = instructions
        self.score: int | None = None

    def __name__(self) -> str:
        """
        Return the name of the game.

        Returns
        -------
        str
            The name of the game.

        Examples
        --------
        >>> game.__name__()
        'Game'

        Notes
        -----
        This method returns the name of the game.
        """
        return self.name

    def __str__(self) -> str:
        """
        Return the name and description of the game.

        Returns
        -------
        str
            The name and description of the game.

        Examples
        --------
        >>> game.__str__()
        'Game: This is a game.'

        Notes
        -----
        This method returns the name and description of the game.
        """
        return f"{self.name}: {self.description}"

    def __repr__(self) -> str:
        """
        Return the name, description, and instructions of the game.

        Returns
        -------
        str
            The name, description, and instructions of the game.

        Examples
        --------
        >>> game.__repr__()
        'Game: This is a game.\n--------\n\nInstructions for the game.'

        Notes
        -----
        This method returns the name, description, and instructions of the game.
        """
        return f"{self.name}: {self.description}.\n--------\n\nInstructions: {self.instructions})"

    def play(self) -> None:
        """
        Play the game.

        Examples
        --------
        >>> game.play()

        Notes
        -----
        This method is used to play the game.
        """
        game_infrastructure_logger.info(f"Playing the {self.name} game.")
        print(f"{self.name}: {self.description}")
        print(f"Instructions: {self.instructions}")
        self.score = 0

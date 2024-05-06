"""strands.py: A game of Strands, inheriting from the Game class."""

from ...config.dialogue_en import DialogueEn
from ...logs.setup_logging import setup_logging
from ..game_infrastructure import Game

strands_logger = setup_logging()


class Strands(Game):
    """
    A game of Strands.

    Notes
    -----
    This class represents the Strands game.
    """

    def __init__(self) -> None:
        """
        Initialise the Strands game.

        Examples
        --------
        >>> strands = Strands(
        ...     "Strands",
        ...     "This is a game of Strands.",
        ...     "Instructions for the game."
        ... )

        Notes
        -----
        This class initialises the Strands game.
        """
        super().__init__(
            DialogueEn.STRANDS_NAME,
            DialogueEn.STRANDS_DESCRIPTION,
            DialogueEn.STRANDS_INSTRUCTIONS,
        )

        # TODO: Implement the Strands game.

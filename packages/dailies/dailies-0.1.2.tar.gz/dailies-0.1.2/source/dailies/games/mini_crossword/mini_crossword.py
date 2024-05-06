"""mini_crossword.py: A game of Mini Crossword, inheriting from the Game class."""

from ...config.dialogue_en import DialogueEn
from ...logs.setup_logging import setup_logging
from ..game_infrastructure import Game

mini_crossword_logger = setup_logging()


class MiniCrossword(Game):
    """
    A game of Mini Crossword.

    Notes
    -----
    This class represents the Mini Crossword game.
    """

    def __init__(self) -> None:
        """
        Initialise the Mini Crossword game.

        Examples
        --------
        >>> mini_crossword = MiniCrossword()

        Notes
        -----
        This method initialises the Mini Crossword game.
        """
        super().__init__(
            DialogueEn.MINI_CROSSWORD_NAME,
            DialogueEn.MINI_CROSSWORD_DESCRIPTION,
            DialogueEn.MINI_CROSSWORD_INSTRUCTIONS,
        )

        # TODO: Implement the Mini Crossword game.

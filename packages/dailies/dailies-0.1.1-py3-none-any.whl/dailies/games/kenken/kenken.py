"""kenken.py: A game of KenKen, inheriting from the Game class."""

from ...config.dialogue_en import DialogueEn
from ...logs.setup_logging import setup_logging
from ..game_infrastructure import Game

kenken_logger = setup_logging()


class KenKen(Game):
    """
    A game of KenKen.

    Notes
    -----
    This class represents the KenKen game.
    """

    def __init__(self) -> None:
        """
        Initialise the KenKen game.

        Examples
        --------
        >>> kenken = KenKen()

        Notes
        -----
        This method initialises the KenKen game.
        """
        super().__init__(
            DialogueEn.KENKEN_NAME,
            DialogueEn.KENKEN_DESCRIPTION,
            DialogueEn.KENKEN_INSTRUCTIONS,
        )

        # TODO: Implement the KenKen game.

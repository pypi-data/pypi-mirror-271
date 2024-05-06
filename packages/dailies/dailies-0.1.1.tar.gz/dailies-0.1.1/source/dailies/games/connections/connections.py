"""connections.py: A game of Connections, inheriting from the Game class."""

from ...config.dialogue_en import DialogueEn
from ...logs.setup_logging import setup_logging
from ..game_infrastructure import Game

connections_logger = setup_logging()


class Connections(Game):
    """
    A game of Connections.

    Notes
    -----
    This class represents the Connections game.
    """

    def __init__(self) -> None:
        """
        Initialises the Connections game.

        Examples
        --------
        >>> connections = Connections()

        Notes
        -----
        This method initialises the Connections game.
        """
        super().__init__(
            DialogueEn.CONNECTIONS_NAME,
            DialogueEn.CONNECTIONS_DESCRIPTION,
            DialogueEn.CONNECTIONS_INSTRUCTIONS,
        )

        # TODO: Implement the Connections game.

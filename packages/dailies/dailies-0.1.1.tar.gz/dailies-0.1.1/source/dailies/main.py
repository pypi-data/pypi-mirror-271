"""main.py: Called when the package is run as a script."""

from .config.paths import Paths
from .logs.setup_logging import setup_logging
from .games.connections.connections import Connections
from .games.kenken.kenken import KenKen
from .games.mini_crossword.mini_crossword import MiniCrossword
from .games.strands.strands import Strands
from .games.sudoku.sudoku import Sudoku
from .games.wordle.wordle import Wordle
from .interface.graphical_menu import main_menu
from .file_interaction.read import read_file

main_logger = setup_logging()


def main() -> None:
    """
    Main function for the application.

    Notes
    -----
    This function is the entry point for the application.
    """
    try:
        main_logger.info("Application started.")
        games = {
            "Wordle": Wordle(read_file(Paths.WORDS)) if read_file(Paths.WORDS) else None,
            "Sudoku": Sudoku(9, 0.6),
            "Connections": Connections(),
            "Mini Crossword": MiniCrossword(),
            "Strands": Strands(),
            "KenKen": KenKen(),
        }

        main_menu(games)
    except KeyboardInterrupt:
        print("\n")
        main_logger.info("Exiting application due to user interrupt...")


if __name__ == "__main__":
    main()

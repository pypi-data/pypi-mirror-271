"""sudoku.py: A game of Sudoku, inheriting from the Game class."""

import random

import numpy as np

from ...config.dialogue_en import DialogueEn
from ...logs.setup_logging import setup_logging
from ..game_infrastructure import Game

sudoku_logger = setup_logging()


class Sudoku(Game):  # TODO: Refactor the Sudoku class to be more readable and maintainable.
    """
    A game of Sudoku.

    Notes
    -----
    This class represents the Sudoku game.
    """

    def __init__(self, size: int, percent_to_remove: float) -> None:
        """
        Initialise the Sudoku game.

        Parameters
        ----------
        size : int
            The size of the Sudoku grid.
        percent_to_remove : float
            The percentage of cells to remove from the Sudoku grid.

        Examples
        --------
        >>> sudoku = Sudoku(9, 0.5)

        Notes
        -----
        This class initialises the Sudoku game with the given size
        and percentage of cells to remove.
        """
        super().__init__(
            DialogueEn.SUDOKU_NAME,
            DialogueEn.SUDOKU_DESCRIPTION,
            DialogueEn.SUDOKU_INSTRUCTIONS,
        )

        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.percent_to_remove = percent_to_remove

    def _valid_numbers(self, i: int, j: int) -> list[int]:
        """
        Finds the valid numbers for the given cell in the Sudoku grid.

        Parameters
        ----------
        i : int
            The row index of the cell.
        j : int
            The column index of the cell.

        Returns
        -------
        list[int]
            The valid numbers for the cell.

        Examples
        --------
        >>> sudoku._valid_numbers(0, 0)
        [1, 2, 3, 4, 5, 6, 7, 8, 9]

        Notes
        -----
        This method finds the valid numbers for the given cell in the Sudoku grid.
        """
        valid_numbers = set(range(1, self.size + 1))

        for k in range(self.size):
            valid_numbers.discard(self.grid[i][k])
            valid_numbers.discard(self.grid[k][j])

        i_start, j_start = 3 * (i // 3), 3 * (j // 3)
        for i in range(i_start, i_start + 3):
            for j in range(j_start, j_start + 3):
                valid_numbers.discard(self.grid[i][j])

        return list(valid_numbers)

    def _fill_grid(self) -> None:
        """
        Fills the Sudoku grid with random numbers.

        Examples
        --------
        >>> sudoku._fill_grid()

        Notes
        -----
        This method fills the Sudoku grid with random numbers.
        """
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j] = random.sample(self._valid_numbers(i, j), 1)[0]

    def _remove_numbers(self) -> None:
        """
        Removes numbers from the Sudoku grid.

        Examples
        --------
        >>> sudoku._remove_numbers()

        Notes
        -----
        This method removes numbers from the Sudoku grid.
        """
        for i in range(self.size):
            for j in range(self.size):
                if random.random() < self.percent_to_remove:
                    self.grid[i][j] = 0

    def solve(self, grid: np.ndarray) -> list[np.ndarray]:
        """
        Solves the Sudoku grid using backtracking.

        Parameters
        ----------
        grid : np.ndarray
            The Sudoku grid to solve.

        Returns
        -------
        list[np.ndarray]
            The list of solutions for the Sudoku grid.

        Examples
        --------
        >>> sudoku.solve(grid)

        Notes
        -----
        This method solves the Sudoku grid using backtracking.
        """

        def _find_empty() -> tuple | None:
            """
            Finds an empty cell in the Sudoku grid.

            Returns
            -------
            tuple | None
                The row and column indices of the empty cell, or None if no empty cell is found.

            Examples
            --------
            >>> _find_empty()
            (0, 0)

            Notes
            -----
            This method finds an empty cell in the Sudoku grid.
            """
            for i in range(self.size):
                for j in range(self.size):
                    if grid[i][j] == 0:
                        return i, j
            return None

        def _solve_sudoku(solutions: list[np.ndarray]) -> None:
            """
            Solves the Sudoku grid using backtracking.

            Parameters
            ----------
            solutions : list[np.ndarray]
                The list of solutions for the Sudoku grid.

            Examples
            --------
            >>> _solve_sudoku(solutions)

            Notes
            -----
            This method solves the Sudoku grid using backtracking.
            """
            if len(solutions) > 1:
                return  # Stop when multiple solutions are found

            empty = _find_empty()
            if not empty:
                solutions.append(grid.copy())
                return

            i, j = empty
            for n in self._valid_numbers(i, j):
                grid[i][j] = n
                _solve_sudoku(solutions)
                grid[i][j] = 0  # Backtrack

        solutions: list[np.ndarray] = []
        _solve_sudoku(solutions)
        return solutions

    def _is_unique(self) -> bool:
        """
        Checks if the Sudoku grid has a unique solution.

        Returns
        -------
        bool
            True if the Sudoku grid has a unique solution, False otherwise.

        Examples
        --------
        >>> sudoku._is_unique()
        True

        Notes
        -----
        This method checks if the Sudoku grid has a unique solution.
        """
        solutions: list = self.solve(self.grid)

        if len(solutions) == 1:
            return True
        else:
            return False

    def _generate(self) -> None:
        """
        Generates a Sudoku grid.

        Examples
        --------
        >>> sudoku._generate()

        Notes
        -----
        This method generates a Sudoku grid.
        """
        unique = False
        while unique is False:
            self._fill_grid()
            self._remove_numbers()
            unique = self._is_unique()

    # TODO: Implement the GUI for the Sudoku game.

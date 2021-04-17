from abc import ABC
from abc import abstractmethod


class UnsetGridError(Exception):
  pass


class InvalidGridShapeError(Exception):
  pass


class SolverInterface(ABC):
  _grid = []

  @abstractmethod
  def is_possible(self, row, col, value):
    pass

  @abstractmethod
  def solve(self, *args, **kwargs):
    pass

  @property
  def grid(self) -> list:
    if not self._grid:
      raise UnsetGridError("Gris is not defined")
    return self._grid

  @grid.setter
  def grid(self, grid: list) -> None:
    if not grid:
      raise InvalidGridShapeError("Grid must be a list")
    row_count = len(grid)
    if row_count == 9:
      col_count = len(grid[0])
      if col_count == 9:
        self._grid = grid
        return
    raise InvalidGridShapeError("Grid must be 9x9")

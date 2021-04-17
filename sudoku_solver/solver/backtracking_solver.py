from sudoku_solver.solver.solver_interface import SolverInterface


class BacktrackingSolver(SolverInterface):
  def is_possible(self, row: int, col: int, num: int) -> bool:
    if not self.grid:
      raise ValueError("Grid is not defined")
    # Check row and columns
    for i in range(9):
      if self.grid[row][i] == num:
        return False
      if self.grid[i][col] == num:
        return False
    # Check 3x3 group
    group_hor_pos = col // 3
    group_ver_pos = row // 3
    for i in range(3):
      check_row = i + group_ver_pos*3
      for j in range(3):
        check_col = j + group_hor_pos*3
        if self.grid[check_row][check_col] == num:
          return False
    return True
  
  def solve(self, update = lambda row, col, num: None):
    if not self.grid:
      raise ValueError("Grid is not defined")
    for row in range(9):
      for col in range(9):
        if self.grid[row][col] == 0:
          for num in range(1,10):
            if self.is_possible(row, col, num):
              update(row, col, num)
              self.grid[row][col] = num
              is_complete = self.solve(update)
              if is_complete:
                return True
              update(row, col, 0)
              self.grid[row][col] = 0
          # solution not found for current number
          # backtrace to previous call
          return False
    return True

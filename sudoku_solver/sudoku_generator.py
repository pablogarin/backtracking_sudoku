import random


def generate_sudoku(solver):
  grid = [[0 for _ in range(9)] for _ in range(9)]
  solver.grid = grid
  number_count = 0
  for row in range(9):
    for col in range(9):
      if insert_number(grid, row, col, solver.is_possible):
        number_count += 1
  return_grid = [[num for num in row] for row in grid]
  if number_count < 20:
    return generate_sudoku(solver)
  if solver.solve():
    return return_grid
  else:
    print("Discarding unsolvable sudoku")
    return generate_sudoku(solver)


def insert_number(grid, row, col, check_function):
  if should_insert_number():
    n = random.randint(1,9)
    if check_function(row, col, n):
      grid[row][col] = n
      return True
    else:
      return insert_number(grid, row, col, check_function)
  else:
    grid[row][col] = 0
    return False

def should_insert_number():
  return random.randint(0,100) > 60
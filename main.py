import sys
import numpy as np


grid = [
  [5,3,0,0,7,0,0,0,0],
  [6,0,0,1,9,5,0,0,0],
  [0,9,8,0,0,0,0,6,0],
  [8,0,0,0,6,0,0,0,3],
  [4,0,0,8,0,3,0,0,1],
  [7,0,0,0,2,0,0,0,6],
  [0,6,0,0,0,0,2,8,0],
  [0,0,0,4,1,9,0,0,5],
  [0,0,0,0,8,0,0,7,9]
]


def is_possible(row, col, num):
  global grid
  # Check row and columns
  for i in range(9):
    if grid[row][i] == num:
      return False
    if grid[i][col] == num:
      return False
  # Check 3x3 group
  group_hor_pos = col // 3
  group_ver_pos = row // 3
  for i in range(3):
    check_row = i + group_ver_pos*3
    for j in range(3):
      check_col = j + group_hor_pos*3
      if grid[check_row][check_col] == num:
        return False
  return True


def solve():
  global grid
  for row in range(9):
    for col in range(9):
      if grid[row][col] == 0:
        for num in range(1,10):
          if is_possible(row, col, num):
            grid[row][col] = num
            is_complete = solve()
            if is_complete:
              return True
            grid[row][col] = 0
        # solution not found
        return False
  return True


if __name__ == "__main__":
  solution = solve()
  if solution:
    print(np.matrix(grid))
    sys.exit(0)
  print("Unsolvable!")
  sys.exit(1)

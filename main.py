import sys
from sudoku_solver.solver.backtracking_solver import BacktrackingSolver
from sudoku_solver.sudoku_ui import SudokuUI
from sudoku_solver.sudoku_generator import generate_sudoku


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

def main():
  solver = BacktrackingSolver()
  ui = SudokuUI(solver)


if __name__ == "__main__":
  main()

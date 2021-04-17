import pygame
from sudoku_solver.solver.solver_interface import SolverInterface
from sudoku_solver.sudoku_generator import generate_sudoku


WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
PALE_GREEN = (180,255,180)
BLUE = (0,0,255)
LIGHT_BLUE = (180, 180, 255)
RED = (255,0,0)
YELLOW = (255,255,0)
PALE_YELLOW = (255, 255, 180)
GRAY = (180, 180, 180)
LIGHT_GRAY = (200, 200, 200)
PURPLE = (255, 90, 255)


NUMBER_MAP = {
  pygame.K_BACKSPACE: 0,
  pygame.K_1: 1,
  pygame.K_2: 2,
  pygame.K_3: 3,
  pygame.K_4: 4,
  pygame.K_5: 5,
  pygame.K_6: 6,
  pygame.K_7: 7,
  pygame.K_8: 8,
  pygame.K_9: 9,
}


class SudokuUI(object):
  def __init__(self, solver: SolverInterface, grid: list = None, size: int = 450):
    self.size = size
    self.solver = solver
    self.set_grid(grid)
    pygame.init()
    pygame.display.set_caption("Sudoku")
    self.screen = pygame.display.set_mode((self.size, self.size))
    self.editing = None
    self.update()
    self.count = 0
    self.fps = 60
    self.start_main_loop()
  
  def start_main_loop(self):
    self.is_running = True
    while self.is_running:
      self.check_events()

  def check_events(self):
    pressed_key = None
    pressed_mouse = None
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.is_running = False
      if event.type == pygame.KEYUP:
        pressed_key = event.key
      if event.type == pygame.MOUSEBUTTONDOWN:
        pressed_mouse = pygame.mouse.get_pressed()[0]
    if pressed_mouse:
      row, col = pygame.mouse.get_pos()
      self.select_cell(row, col)
    if pressed_key:
      if pressed_key == pygame.K_n:
        self.set_grid(None)
        self.update()
      elif self.editing:
        cell = self.get_cell_at(*self.editing)
        if pressed_key in NUMBER_MAP:
          num = NUMBER_MAP[pressed_key]
          self.update_cell(cell, num)
          self.editing = None
          self.update()
      else:
        if pressed_key == pygame.K_SPACE:
          self.solver.grid = self.get_grid()
          self.solver.solve(update=self.fill_cell)
          self.update()
          pressed_key = None
  
  def fill_cell(self, row, col, value):
    cell = self.get_cell(row, col)
    cell.value = value
    cell.color = WHITE
    if value > 0:
      cell.color = PALE_YELLOW
    self.count += 1
    if self.count % self.fps == 0:
      self.update()

  def set_grid(self, grid):
    if not grid:
      grid = generate_sudoku(self.solver)
    self.solver.grid = grid
    self.grid = []
    for row in range(9):
      curr_row = []
      for col in range(9):
        cell = Cell(row, col, grid[row][col])
        if cell.value != 0:
          cell.blocked = True
          cell.color = LIGHT_GRAY
        curr_row.append(cell)
      self.grid.append(curr_row)
  
  def select_cell(self, row, col):
    cell = self.get_cell_at(row, col)
    if cell.blocked:
      return
    if self.editing:
      old_cell = self.get_cell_at(*self.editing)
      old_cell.color = WHITE
    self.editing = (row, col)
    cell.color = PALE_GREEN
    self.update()
  
  def update_cell(self, cell, value):
    cell.value = value
    cell.color = WHITE
    if cell.value > 0 and not self.solver.is_possible(cell.row, cell.col, cell.value):
      cell.color = RED
    self.solver.grid = self.get_grid()

  def get_cell_at(self, x, y):
    cell_size = self.size // 9
    row = y//cell_size
    col = x//cell_size
    cell = self.get_cell(row, col)
    return cell
  
  def get_cell(self, row, col):
    return self.grid[row][col]

  def paint_cell(self, cell):
    y, x = cell.row, cell.col
    cell_size = self.size // 9
    rect = (x*cell_size, y*cell_size, cell_size, cell_size)
    pygame.draw.rect(self.screen, cell.color, rect)
    num = cell.value
    if num > 0:
      row, col = cell.row, cell.col
      self.draw_number(row, col, num)
  
  def update(self):
    self.screen.fill(WHITE)
    for row in range(9):
      for col in range(9):
        cell = self.grid[row][col]
        self.paint_cell(cell)
    self.draw_grid()
    pygame.display.update()
  
  def draw_grid(self):
    gap = self.size // 9
    for i in range(0, self.size):
      horizontal_init, horizontal_end = ((0, i*gap), (self.size, i* gap))
      vertical_init, vertical_end = ((i*gap, 0), (i* gap, self.size))
      pygame.draw.line(self.screen, GRAY, horizontal_init, horizontal_end)
      pygame.draw.line(self.screen, GRAY, vertical_init, vertical_end)
    gap = self.size // 3
    for i in range(0, self.size):
      horizontal_init, horizontal_end = ((0, i*gap), (self.size, i* gap))
      vertical_init, vertical_end = ((i*gap, 0), (i* gap, self.size))
      pygame.draw.line(self.screen, BLACK, horizontal_init, horizontal_end)
      pygame.draw.line(self.screen, BLACK, vertical_init, vertical_end)

  def draw_number(self, row: int, col: int, num: int):
    font = pygame.font.SysFont(None, 40)
    img = font.render(str(num), True, BLACK)
    num_size = img.get_rect()
    *_, width, height = num_size
    y = ((self.size // 9 ) * row) + ((self.size // 9)//2) - height/2
    x = ((self.size // 9 ) * col) + ((self.size // 9)//2) - width/2
    self.screen.blit(img, (x, y))
  
  def get_grid(self):
    simple_grid = []
    for row in range(9):
      row_list = []
      for col in range(9):
        cell = self.grid[row][col]
        row_list.append(cell.value)
      simple_grid.append(row_list)
    return simple_grid


class Cell(object):
  def __init__(self, row: int, col: int, value: int):
    self.row = row
    self.col = col
    self.value = value
    self.blocked = False
    self.color = WHITE

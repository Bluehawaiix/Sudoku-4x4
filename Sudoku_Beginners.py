import pygame
import sys
import time

SIZE = 4                 # the board is SIZE x SIZE cells
BOX = 2                  # sub-boxes are BOX x BOX (drawn with thick lines)
CELL = 80                # pixels per cell
BOTTOM_BAR = 80          # pixels reserved for the status bar
BOARD = SIZE * CELL      # the board is a 320 x 320 square
WIDTH, HEIGHT = BOARD, BOARD + BOTTOM_BAR

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 120, 240)          # given numbers (fixed)
GRAY = (80, 80, 80)            # numbers the player typed
SELECT_COLOR = (173, 216, 230) # highlight of the selected cell
GREEN = (34, 139, 34)          # "correct" message
RED = (220, 20, 60)            # "wrong" message

PUZZLE = [
    [1, 0, 3, 0],
    [0, 4, 0, 2],
    [2, 0, 4, 0],
    [0, 3, 0, 1],
]  # 0 means "empty cell"

NUMBER_KEYS = {
    pygame.K_1: 1, pygame.K_KP1: 1,
    pygame.K_2: 2, pygame.K_KP2: 2,
    pygame.K_3: 3, pygame.K_KP3: 3,
    pygame.K_4: 4, pygame.K_KP4: 4,
}
CLEAR_KEYS = (pygame.K_BACKSPACE, pygame.K_DELETE)
CONFIRM_KEYS = (pygame.K_RETURN, pygame.K_KP_ENTER)
ARROW_KEYS = {
    pygame.K_UP: (-1, 0),    # (row delta, column delta)
    pygame.K_DOWN: (1, 0),
    pygame.K_LEFT: (0, -1),
    pygame.K_RIGHT: (0, 1),
}

# window
pygame.init()  
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini 4x4 Sudoku")
big_font = pygame.font.SysFont("arial", 45)
small_font = pygame.font.SysFont("arial", 16)


grid = [row[:] for row in PUZZLE]                      # working copy of the puzzle
given = [[cell != 0 for cell in row] for row in PUZZLE] # True = fixed cell
selected = None                                        # (row, col) or None
message = "Press ENTER to check your solution"
message_color = BLACK


def cell_at(pos):
    """Pixel position -> (row, col), or None when clicked below the board."""
    x, y = pos
    return (y // CELL, x // CELL) if y < BOARD else None


def first_empty():
    """Coordinates of the first empty cell, or None when the board is full."""
    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c] == 0:
                return r, c
    return None


def unique(cells):
    """True when a row/column/box holds SIZE different numbers."""
    return len(set(cells)) == SIZE


def check_solution():
    """Compare the board with the rules; store the verdict in message."""
    global message, message_color

    rows = grid  # every row is already a list inside grid
    columns = [[grid[r][c] for r in range(SIZE)] for c in range(SIZE)]
    boxes = [[grid[r][c]
              for r in range(br, br + BOX)
              for c in range(bc, bc + BOX)]
             for br in range(0, SIZE, BOX)
             for bc in range(0, SIZE, BOX)]

    if any(cell == 0 for row in rows for cell in row):
        message, message_color = "Incomplete! Keep working.", RED
    elif not all(unique(r) for r in rows) or not all(unique(c) for c in columns):
        message, message_color = "Incorrect solution! Check it again.", RED
    else:
        message, message_color = "Perfect! You are genius!", GREEN


def handle_key(key):
    """Apply one key press to the game state."""
    
    if selected is not None and key in NUMBER_KEYS:
        grid[selected[0]][selected[1]] = NUMBER_KEYS[key]
    elif selected is not None and key in CLEAR_KEYS:
        grid[selected[0]][selected[1]] = 0
    elif key in CONFIRM_KEYS:
        check_solution()


def draw(elapsed):
    """Paint the window: highlight, numbers, grid lines and the status bar."""
    screen.fill(WHITE)

    if selected is not None:
        r, c = selected
        pygame.draw.rect(screen, SELECT_COLOR, (c * CELL, r * CELL, CELL, CELL))

    for r in range(SIZE):
        for c in range(SIZE):
            if grid[r][c]:
                colour = BLUE if given[r][c] else GRAY
                digit = big_font.render(str(grid[r][c]), True, colour)
                centre = (c * CELL + CELL // 2, r * CELL + CELL // 2)
                screen.blit(digit, digit.get_rect(center=centre))

    for i in range(SIZE + 1):  # box borders and the outer frame are thick
        thickness = 4 if i % BOX == 0 else 1
        pygame.draw.line(screen, BLACK, (0, i * CELL), (BOARD, i * CELL), thickness)
        pygame.draw.line(screen, BLACK, (i * CELL, 0), (i * CELL, BOARD), thickness)

    mins, secs = int(elapsed // 60), int(elapsed % 60)
    timer_text = small_font.render(f"Time: {mins:02d}:{secs:02d}", True, BLACK)
    status_text = small_font.render(message, True, message_color)
    screen.blit(status_text, (15, BOARD + 15))
    screen.blit(timer_text, (15, BOARD + 45))


def main():
    """Game loop: draw, then handle events, 30 times per second."""
    global selected
    clock = pygame.time.Clock()
    start = time.time()
    elapsed = 0.0
    running = True

    while running:
        if message_color != GREEN:  # freeze the clock after a win
            elapsed = time.time() - start

        draw(elapsed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cell = cell_at(event.pos)
                selected = cell if cell and not given[cell[0]][cell[1]] else None
            elif event.type == pygame.KEYDOWN:
                handle_key(event.key)

        pygame.display.update()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
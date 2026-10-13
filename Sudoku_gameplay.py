import pygame
import sys
import time

# Initialize Pygame and fonts
pygame.init()
pygame.font.init()

# Window Settings
WINDOW_SIZE = 540  # 9 cells * 60px
BOTTOM_BAR = 80
SCREEN = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + BOTTOM_BAR))
pygame.display.set_caption("Sudoku Game 9x9")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)
BLUE = (50, 120, 240)       # Original unchangeable numbers
DARK_GRAY = (80, 80, 80)    # User inputted numbers
SELECT_COLOR = (173, 216, 230) # Light blue highlight for selection
GREEN = (34, 139, 34)       # Success message
RED = (220, 20, 60)         # Error message

# Sample 9x9 Sudoku Board (0 represents empty cells)
GRID = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Track configuration masks
ORIGINAL_MASK = [[GRID[r][c] != 0 for c in range(9)] for r in range(9)]

FONT = pygame.font.SysFont("arial", 35)
UI_FONT = pygame.font.SysFont("arial", 20)

# Game State Variables
selected_cell = None  # Stores (row, col) tuple
start_time = time.time()
game_status_msg = "Press 'ENTER' to check your solution"
msg_color = BLACK

def draw_grid(elapsed_time):
    """Draws the board, selection block, numbers, and the bottom status dashboard."""
    SCREEN.fill(WHITE)
    cell_size = WINDOW_SIZE // 9
    
    # Highlight selected cell
    if selected_cell:
        r, c = selected_cell
        pygame.draw.rect(SCREEN, SELECT_COLOR, (c * cell_size, r * cell_size, cell_size, cell_size))

    # Draw numbers
    for r in range(9):
        for c in range(9):
            if GRID[r][c] != 0:
                color = BLUE if ORIGINAL_MASK[r][c] else DARK_GRAY
                text = FONT.render(str(GRID[r][c]), True, color)
                text_rect = text.get_rect(center=(c * cell_size + cell_size//2, r * cell_size + cell_size//2))
                SCREEN.blit(text, text_rect)

    # Draw structural grid lines
    for i in range(10):
        thickness = 4 if i % 3 == 0 else 1
        pygame.draw.line(SCREEN, BLACK, (0, i * cell_size), (WINDOW_SIZE, i * cell_size), thickness)
        pygame.draw.line(SCREEN, BLACK, (i * cell_size, 0), (i * cell_size, WINDOW_SIZE), thickness)
        
    # Render Bottom UI elements (Timer & Game Validation Status)
    mins = int(elapsed_time // 60)
    secs = int(elapsed_time % 60)
    timer_str = f"Time: {mins:02d}:{secs:02d}"
    
    timer_text = UI_FONT.render(timer_str, True, BLACK)
    status_text = UI_FONT.render(game_status_msg, True, msg_color)
    
    SCREEN.blit(status_text, (20, WINDOW_SIZE + 15))
    SCREEN.blit(timer_text, (20, WINDOW_SIZE + 45))

def get_cell_from_pos(pos):
    """Translates pixel mouse click coordinates into (row, col) matrix indexes."""
    x, y = pos
    if y < WINDOW_SIZE:
        cell_size = WINDOW_SIZE // 9
        return y // cell_size, x // cell_size
    return None

def check_solution():
    """Validates if the user's completed board grid is mathematically correct."""
    global game_status_msg, msg_color
    
    # 1. Look for incomplete spaces
    for r in range(9):
        for c in range(9):
            if GRID[r][c] == 0:
                game_status_msg = "Puzzle incomplete! Keep working."
                msg_color = RED
                return

    # 2. Validate all rows, columns, and 3x3 subgrids
    for i in range(9):
        row_set = set()
        col_set = set()
        box_set = set()
        
        # Check rows & columns uniqueness
        for j in range(9):
            row_set.add(GRID[i][j])
            col_set.add(GRID[j][i])
            
        # Check 3x3 boxes uniqueness
        box_x = (i % 3) * 3
        box_y = (i // 3) * 3
        for r in range(box_y, box_y + 3):
            for c in range(box_x, box_x + 3):
                box_set.add(GRID[r][c])
                
        if len(row_set) != 9 or len(col_set) != 9 or len(box_set) != 9:
            game_status_msg = "Incorrect solution! Check for duplicate items."
            msg_color = RED
            return

    game_status_msg = "Congratulations! You are genius!"
    msg_color = GREEN

def main():
    global selected_cell, game_status_msg, msg_color
    clock = pygame.time.Clock()
    running = True
    game_over = False

    while running:
        # Calculate time (stop ticking if user wins)
        if msg_color != GREEN:
            current_elapsed = time.time() - start_time
        
        draw_grid(current_elapsed)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                cell = get_cell_from_pos(pos)
                if cell:
                    r, c = cell
                    # Only allow selection if it isn't an original starting digit
                    if not ORIGINAL_MASK[r][c]:
                        selected_cell = cell
                    else:
                        selected_cell = None
                        
            elif event.type == pygame.KEYDOWN:
                if selected_cell:
                    r, c = selected_cell
                    
                    # Intercept number inputs (Keyboard numbers or Numpad numbers)
                    if event.key in [pygame.K_1, pygame.K_KP1]: GRID[r][c] = 1
                    elif event.key in [pygame.K_2, pygame.K_KP2]: GRID[r][c] = 2
                    elif event.key in [pygame.K_3, pygame.K_KP3]: GRID[r][c] = 3
                    elif event.key in [pygame.K_4, pygame.K_KP4]: GRID[r][c] = 4
                    elif event.key in [pygame.K_5, pygame.K_KP5]: GRID[r][c] = 5
                    elif event.key in [pygame.K_6, pygame.K_KP6]: GRID[r][c] = 6
                    elif event.key in [pygame.K_7, pygame.K_KP7]: GRID[r][c] = 7
                    elif event.key in [pygame.K_8, pygame.K_KP8]: GRID[r][c] = 8
                    elif event.key in [pygame.K_9, pygame.K_KP9]: GRID[r][c] = 9
                    # Clear cell with Backspace or Delete
                    elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]: GRID[r][c] = 0
                
                # Check validation manually when hitting Return/Enter key
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    check_solution()

        pygame.display.update()
        clock.tick(30)  # Keep the loop steady at 30 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
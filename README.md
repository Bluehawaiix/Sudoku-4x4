## Mini 4x4 Sudoku 
This project implements a mini interactive Sudoku game built with Python and Pygame library. Unlike traditional 9x9 Sudoku,
this version uses a 4x4 grid divided into 2x2 sub-boxes, making it simpler and faster to play.

The game provides:
A graphical interface with a Sudoku board.
Mouse and keyboard interaction for selecting and filling cells.
A timer to track play duration.
Validation logic to check whether the solution is correct.
Visual feedback with colors for fixed numbers, user input, and solution messages.

This project is intended as a learning exercise in Python game development, event handling, and GUI programming.

## Installation Instructions

### Installation
Prerequisites
- Python 3.8+
- Pygame library

Setup Instructions
1. Clone the repository
   "https://github.com/Bluehawaiix/Sudoku-4x4.git"
2. Install dependencise
   "pip install pygame"
3. Run the game
   "python Sudoku_Beginners.py"

## Usage Instructions

### Controls
- Mouse click -> Select a cell (only empty cells can be selected).
- Number keys(1-4) -> Fill the selected xell with that number.
- Backspace/Delete -> Clear the selected cell.
- Enter/Return -> Check the solution.

### Game Rules
- Fill in all empty cells with numbers 1-4.
- Each row and column must contain unique numbers.
- Press Enter to validate your solution:
  For the correct solution, it shows "Perfect! You are genius"
<img width="200" height="300" alt="Screenshot 2026-10-13 230934" src="https://github.com/user-attachments/assets/99b79d91-5eab-4a9e-8c8b-bf2ccbe1085c" />

  
  For the incorrect solution, it shows "Incorrect solution! Check it again."
  
<img width="200" height="300" alt="Screenshot 2026-10-13 230920" src="https://github.com/user-attachments/assets/a27b3ef9-c8fd-422a-944e-2414a77a1350" />

  
  For the incomplete solution, it shows "Incomplete! Keep working."
  
<img width="200" height="300" alt="Screenshot 2026-10-13 230849" src="https://github.com/user-attachments/assets/91374fee-5927-494a-a464-ab09a138965d" />


### Exit
- Close the window to exit the game.

## Example Run
When you launch the game:
- A 4×4 Sudoku board appears with some numbers pre-filled.
- You can interact with the board using mouse and keyboard.
- A timer runs at the bottom of the screen.
- Messages guide you as you play and check your solution.

<img width="200" height="300" alt="Screenshot 2026-10-13 230816" src="https://github.com/user-attachments/assets/39db8136-41a7-4576-9e32-c5087b46f595" />


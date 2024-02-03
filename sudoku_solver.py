def is_safe(board, row, col, num):
    # Check if the number is not present in the current row
    if num in board[row]:
        return False
    
    # Check if the number is not present in the current column
    for i in range(9):
        if board[i][col] == num:
            return False
    
    # Check if the number is not present in the current 3x3 grid
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    
    return True

def find_empty_location(board):
    # Find the next empty location in the board
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return -1, -1  # If no empty location is found

def solve_sudoku(board):
    row, col = find_empty_location(board)

    # If no empty location is found, the puzzle is solved
    if row == -1 and col == -1:
        return True

    # Try numbers from 1 to 9
    for num in range(1, 10):
        if is_safe(board, row, col, num):
            # Assign the number if it is safe
            board[row][col] = num

            # Recursively solve the rest of the puzzle
            if solve_sudoku(board):
                return True

            # Backtrack if the current assignment does not lead to a solution
            board[row][col] = 0

    # If no number can be assigned, return False to trigger backtracking
    return False

if __name__ == "__main__":
    # Sample Sudoku puzzle (0 represents empty cells)
    sudoku_board = [[0, 8, 0, 0, 4, 0, 1, 0, 6,],
                    [5, 0, 0, 0, 0, 0, 4, 0, 0,],
                    [0, 0, 0, 0, 0, 9, 0, 0, 0,],
                    [0, 0, 7, 0, 0, 0, 0, 3, 0,],
                    [0, 0, 0, 6, 0, 0, 5, 0, 0,],
                    [0, 2, 9, 0, 0, 0, 0, 0, 0,],
                    [0, 0, 0, 8, 0, 0, 0, 7, 0,],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0,],
                    [0, 0, 0, 0, 0, 0, 0, 9, 0]]

    if solve_sudoku(sudoku_board):
        print("Sudoku puzzle solved successfully:")
        for row in sudoku_board:
            print(row)
    else:
        print("No solution exists for the Sudoku puzzle.")

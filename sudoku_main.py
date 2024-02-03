import cv2
from ppadb.client import Client as AdbClient
import numpy as np
from time import sleep
import numpy as np
import pytesseract
import sudoku_solver
import sys
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def progress_bar(iteration, total, prefix='', suffix='', length=20, fill='#'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    sys.stdout.flush()

adb = AdbClient(host="127.0.0.1", port=5037)
devices = adb.devices()
if len(devices) == 0:
    print('No devices')
    quit()

device = devices[0]

# step 1 - take a screenshot
print('Taking a screenshot...')

device.shell('screencap -p /sdcard/screenshot.png')
device.pull('/sdcard/screenshot.png', 'screenshot.png')

# step 2 - preprocess the image
print('Preprocessing the image...')

captured_image = cv2.imread('screenshot.png')
gray_image = cv2.cvtColor(captured_image, cv2.COLOR_BGR2GRAY)

kernel = np.array([[0, -1, 0],
                   [-1, 4, -1],
                   [0, -1, 0]])

convoluted_image = cv2.filter2D(gray_image, -1, kernel)

# step 3 - find the sudoku grid
contours, _ = cv2.findContours(convoluted_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))

sudoku_grid_image = captured_image[y:y+h, x:x+w]

# step 4 - make the grid and fill the numbers with AI
print('Making the Sudoku grid...')

sudoku_grid = np.zeros((9, 9), dtype=int)

cell_width = sudoku_grid_image.shape[1] // 9
cell_height = sudoku_grid_image.shape[0] // 9

for i in range(9):
    for j in range(9):
        cell = sudoku_grid_image[i*cell_height:(i+1)*cell_height, j*cell_width:(j+1)*cell_width]
        cell = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
        _, cell = cv2.threshold(cell, 120, 255, cv2.THRESH_BINARY_INV)
        cell = cv2.GaussianBlur(cell, (5, 5), 0)
        cell = cv2.resize(cell, (28, 28))

        number = pytesseract.image_to_string(cell, config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')

        try:
            number = int(number)
        except ValueError:
            number = 0

        sudoku_grid[i, j] = number

        progress_bar(i*9+j+1, 81, prefix='Progress:', suffix='Complete', length=40)

print('\nSudoku grid extracted successfully:')
print(sudoku_grid)
######

# step 5 - solve the sudoku
print('Solving the Sudoku puzzle...')

sudoku_grid_solution = sudoku_grid.copy()
if sudoku_solver.solve_sudoku(sudoku_grid_solution):
    print("Sudoku puzzle solved successfully:")
    print(sudoku_grid_solution)
else:
    print("No solution exists for the Sudoku puzzle.")

# step 6 - send the solution to the device

################
grid_coords = [[90, 500], [90, 1400], [990, 500]]
number_coords = [[70, 2000], [1000, 2000]]
################

def tap(x, y):
    device.shell(f'input tap {x} {y}')

def set_case(i, j, number):
    # tap the case
    tap(grid_coords[0][0]+(grid_coords[2][0]-grid_coords[0][0])//8*j, 
        grid_coords[0][1]+(grid_coords[1][1]-grid_coords[0][1])//8*i)
    # tap the number
    tap(number_coords[0][0]+(number_coords[1][0]-number_coords[0][0])//8*(number-1), 
        number_coords[1][1]+(number_coords[1][1]-number_coords[0][1])//8*(number-1))

for i in range(9):
    for j in range(9):
        if sudoku_grid[i, j] == 0:
            set_case(i, j, sudoku_grid_solution[i, j])
        progress_bar(i*9+j+1, 81, prefix='Progress:', suffix='Complete', length=40)

print()
# step 7 clean up
print('Cleaning up...')
device.shell('rm /sdcard/screenshot.png')
os.remove('screenshot.png')
print('Done!')


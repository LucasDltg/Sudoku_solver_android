# Sudoku Solver for Android

This python script is meant to be used with Sudoku developed by Kidult Lovin available on google play store.

## Requirements
- OpenCV
- ppadb.client
- pytesseract

## Overview
- Establish a connection with an Android device.
- Capture a screenshot from the device and transfer it to the PC.
- Apply filters to the image and extract the grid from it.
- Numerize the grid.
- Solve the Sudoku puzzle using a simple backtracking algorithm.
- Fill the solved puzzle on the phone, correct any recognized text errors, and enhance it.
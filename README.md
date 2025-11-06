# 📐 Linear Equation System Solver (Gauss & Gauss-Jordan)

This project is a simple desktop application built with Python and `Tkinter`. It solves systems of linear equations using two primary methods: **Gauss Elimination** and **Gauss-Jordan Elimination**.

The application is capable of solving systems of any (m x n) size and displays all solution steps in detail, making it a useful educational tool.

## ✨ Features

* **Graphical User Interface (GUI)**: A simple and easy-to-use interface built entirely with `Tkinter`.
* **m x n Support**: Can solve any system of `m` equations and `n` variables (currently limited to 10x10 in the GUI).
* **Method Selection**: The user can choose between:
    * **Gauss Elimination** (which reduces the matrix to Row Echelon Form and then uses back substitution).
    * **Gauss-Jordan** (which reduces the matrix to Reduced Row Echelon Form).
* **Step-by-Step Display**: A text box shows all step-by-step operations (row swaps, scaling, and row operations).
* **Solution Type Detection**: The application automatically identifies all three solution cases:
    1.  **Unique Solution**
    2.  **Infinite Solutions**
    3.  **No Solution (Inconsistent System)**
* **Pivoting**: The code uses a partial pivoting strategy to enhance numerical stability. It first searches for a '1' to use as a pivot. If none is found, it uses the element with the largest absolute value in the pivot column.

## 📋 Requirements

* Python 3.x
* `Tkinter` (This library is typically included with standard Python installations).

## 🚀 How to Run

1.  Ensure you have Python 3 installed on your system.
2.  Save the code in a file named `Solve.py`.
3.  Run the file from your Terminal or Command Prompt:
    ```bash
    python Solve.py
    ```
    or
    ```bash
    python3 Solve.py
    ```

## 📝 How to Use

1.  When you run the program, a main window will appear.
2.  **Select Solver Method**: Choose either "Gauss Elimination" or "Gauss-Jordan".
3.  **Enter Dimensions**:
    * Enter the number of equations (rows) in the `m` field.
    * Enter the number of variables (columns) in the `n` field.
4.  Click the **"Create Input Grid"** button.
5.  The main window will hide, and a new window will appear for matrix input, dynamically sized to your `m` and `n` values.
6.  Enter all coefficients for the variables (x1, x2, ...) and the constant values (b) in their respective fields.
7.  Click the **"Solve System"** button.
8.  All solution steps and the final result will be displayed in the text box at the bottom of the window.

## 🔧 Code Overview

The code is primarily divided into two parts:

### 1. Algorithm Functions

* `solve_system(matrix_entries, m, n, steps_text, method)`:
    * The main function that takes input from the GUI.
    * Executes the chosen elimination algorithm (Gauss or Gauss-Jordan) step-by-step.
    * Logs every step to the `steps_log` for display.
    * Applies pivoting (searching for '1' or max absolute value).
    * Checks for the solution type (Unique, Infinite, or No Solution) at the end.
* `back_substitution(matrix, m, n)`:
    * A helper function used *only* by Gauss Elimination to find the variable values after the matrix is in Row Echelon Form.
* `format_matrix(matrix)`:
    * A helper function to print the matrix neatly in the steps log.

### 2. GUI Code

* `create_matrix_grid()`:
    * This function creates the second window (the matrix input grid) dynamically based on the `m` and `n` dimensions provided by the user.
* **Root Window Setup**:
    * Initializes the main (first) window that asks the user to select the method and dimensions.
    * Uses `ttk` (themed tkinter widgets) for a cleaner, more modern look.

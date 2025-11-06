import tkinter as tk
from tkinter import ttk, messagebox

# Set your desired font size here
DEFAULT_FONT_SIZE = 12 

# ==================================
# Algorithm Helper Functions
# ==================================

def format_matrix(matrix):
    """Converts a list of lists (matrix) into a formatted string."""
    s = ""
    epsilon = 1e-9 # Threshold for zero
    
    for row in matrix:
        formatted_row = []
        for num in row:
            # Check if the number is "effectively zero"
            if abs(num) < epsilon:
                # If it is, treat it as positive 0.0 to avoid -0.00
                formatted_row.append(f"{0.0:8.2f}")
            else:
                # Otherwise, format it normally
                formatted_row.append(f"{num:8.2f}")
        
        s += "  ".join(formatted_row) + "\n"
    return s

def back_substitution(matrix, m, n):
    """
    Performs back substitution for (m x n) system.
    Assumes a unique solution (m >= n) and REF form.
    """
    solution = [0.0] * n
    # We only need to iterate up to n (number of variables)
    for i in range(n - 1, -1, -1):
        sum_ax = 0.0
        # Sum known variables (to the right of the pivot)
        for j in range(i + 1, n):
            sum_ax += matrix[i][j] * solution[j]
        
        pivot = matrix[i][i]
        if abs(pivot) < 1e-9:
             solution[i] = 0.0 
        else:
            # The constant is in the last column (index n)
            solution[i] = (matrix[i][n] - sum_ax) / pivot
    return solution

# ==================================
# Main Solver Function (MODIFIED for m x n)
# ==================================

def solve_system(matrix_entries, m, n, steps_text, method):
    
    steps_text.config(state='normal')
    steps_text.delete('1.0', tk.END)
    steps_log = []
    
    # 1. Read numbers (m rows, n+1 columns)
    matrix = []
    try:
        for i in range(m):
            row = []
            for j in range(n + 1):
                value = float(matrix_entries[i][j].get())
                row.append(value)
            matrix.append(row)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers in all fields.")
        steps_text.config(state='disabled')
        return
    
    method_name = "Gauss-Jordan" if method == "jordan" else "Gauss Elimination"
    steps_log.append(f"===== Selected Method: {method_name} (System: {m}x{n}) =====")
    steps_log.append("===== Initial Augmented Matrix =====")
    steps_log.append(format_matrix(matrix))
    steps_log.append("\n===== Starting Elimination =====")
    
    h = 0 # Current pivot row
    k = 0 # Current pivot column

    # Main algorithm loop
    while h < m and k < n:
        
        # --- [Pivot Logic Start] ---
        # 1. Check if current pivot (h,k) is 1
        if abs(matrix[h][k] - 1.0) < 1e-9:
            steps_log.append(f"\n--- Pivot at (R{h+1}, C{k+1}) is 1. No swap needed.")
        
        else:
            # 2. Not 1. Search for a '1' below
            steps_log.append(f"\n--- Pivot at (R{h+1}, C{k+1}) is not 1. Searching for swap...")
            i_one = -1
            for i in range(h + 1, m): # Look in rows below h
                if abs(matrix[i][k] - 1.0) < 1e-9:
                    i_one = i
                    break
            
            if i_one != -1:
                # 3. Found a '1'. Swap.
                steps_log.append(f"Found '1' in R{i_one+1}. Swapping with R{h+1}.")
                matrix[h], matrix[i_one] = matrix[i_one], matrix[h]
                steps_log.append(format_matrix(matrix))
            
            else:
                # 4. Fallback: No '1' found. Use max pivot.
                steps_log.append(f"No '1' found. Using max pivot (Partial Pivoting).")
                i_max = h
                for i in range(h + 1, m): # Look in rows below h
                    if abs(matrix[i][k]) > abs(matrix[i_max][k]):
                        i_max = i
                
                pivot_value = matrix[i_max][k]

                # 5. Check if max pivot is zero (skip column)
                if abs(pivot_value) < 1e-9:
                    steps_log.append(f"\n--- No pivot in Col {k+1}. Skipping...")
                    k += 1
                    continue 
                
                # 6. Swap with max pivot
                if i_max != h:
                    steps_log.append(f"Swapping R{h+1} with R{i_max+1} (max pivot).")
                    matrix[h], matrix[i_max] = matrix[i_max], matrix[h]
                    steps_log.append(format_matrix(matrix))
                
                # 7. Make pivot a 'Leading 1'
                pivot_value = matrix[h][k]
                steps_log.append(f"\n--- 'Leading 1' Step (R{h+1}) ---")
                steps_log.append(f"Operation: R{h+1} = R{h+1} / {pivot_value:.2f}")
                for j in range(k, n + 1): # Divide from col k to end
                    matrix[h][j] = matrix[h][j] / pivot_value
                steps_log.append(format_matrix(matrix))
        
        # --- [Pivot Logic End] ---

        # --- Step 4: Elimination (Zero other rows) ---
        for i in range(m): # Loop ALL rows (0 to m-1)
            if i == h:
                continue 
            
            factor = matrix[i][k]
            if abs(factor) < 1e-9:
                continue

            # 'jordan' zeros *above* (i < h) and *below* (i > h)
            # 'gauss' *only* zeros *below* (i > h)
            if method == 'gauss' and i < h:
                continue
            
            op_type = "Jordan Elimination" if method == 'jordan' else "Gauss Elimination"
            steps_log.append(f"\n--- '{op_type}' Step: Zeroing R{i+1} using R{h+1} ---")
            steps_log.append(f"Operation: R{i+1} = R{i+1} - ({factor:.2f}) * R{h+1}")

            for j in range(k, n + 1): # Start from col k
                matrix[i][j] = matrix[i][j] - factor * matrix[h][j]
            steps_log.append(format_matrix(matrix))
        
        h += 1 # Move to next pivot row
        k += 1 # Move to next pivot column
    
    # --- End of while loop ---
    num_pivots = h # Number of pivots found
    
    final_form_name = "RREF" if method == "jordan" else "Row Echelon Form"
    steps_log.append(f"\n===== Elimination Complete ({final_form_name}) =====")
    steps_log.append(format_matrix(matrix))
    
    # --- 8. Check for Special Cases (No Solution / Infinite / Unique) ---
    steps_log.append("\n===== Checking for Solution Type =====")

    # Check for No Solution (Inconsistency)
    for i in range(num_pivots, m): # Check rows below the pivots
        # Check if a row is [0 0 ... 0 | b] where b != 0
        is_all_coeffs_zero = all(abs(matrix[i][j]) < 1e-9 for j in range(n))
        constant = matrix[i][n]
        
        if is_all_coeffs_zero and abs(constant) > 1e-9:
            steps_log.append(f"\n!!! No Solution (Inconsistent System) !!!")
            steps_log.append(f"Inconsistency found in Row {i+1}: (0 = {constant:.2f})")
            steps_text.insert(tk.END, "\n".join(steps_log))
            steps_text.config(state='disabled')
            return
            
    # Check for Infinite vs Unique
    if num_pivots < n:
        # Fewer pivots than variables
        steps_log.append(f"\n!!! Infinite Solutions !!!")
        steps_log.append(f"System has {num_pivots} pivots and {n} variables.")
        steps_log.append("This indicates free variables exist.")
    
    else:
        # num_pivots == n (Unique Solution)
        steps_log.append("\n===== System has a Unique Solution =====")
        
        if method == 'gauss':
            steps_log.append("===== Starting Back Substitution =====")
            solution = back_substitution(matrix, m, n)
            
            steps_log.append("\n--- Final Solution ---")
            solution_text = []
            for i in range(n):
                solution_text.append(f"x{i+1} = {solution[i]:.4f}")
            steps_log.append("\n".join(solution_text))
            
        elif method == 'jordan':
            steps_log.append("\n--- Final Solution (from RREF) ---")
            solution_text = []
            # Solution is in the first 'n' rows of the last column
            for i in range(n):
                solution_text.append(f"x{i+1} = {matrix[i][n]:.4f}")
            steps_log.append("\n".join(solution_text))

    steps_text.insert(tk.END, "\n".join(steps_log))
    steps_text.config(state='disabled')

# ==================================
# GUI Creation Code (MODIFIED for m x n)
# ==================================

matrix_entries = []
num_rows_m = 0
num_cols_n = 0
method_var = None 

def create_matrix_grid():
    global num_rows_m, num_cols_n, matrix_entries, method_var
    
    try:
        # Read m and n from the new entries
        m = int(m_entry.get())
        n = int(n_entry.get())
        
        if m < 1 or n < 1 or m > 10 or n > 10:
            messagebox.showwarning("Warning", "Please enter numbers between 1 and 10.")
            return
        
        # Store them globally for the solver
        num_rows_m = m
        num_cols_n = n
        
    except ValueError:
        messagebox.showerror("Error", "Please enter valid integers for rows and columns.")
        return
        
    current_method = method_var.get() 
    method_name = "Gauss-Jordan" if current_method == "jordan" else "Gauss Elimination"

    root.withdraw()

    matrix_window = tk.Toplevel(root)
    matrix_window.title(f"Enter {m}x{n} System - ({method_name} Method)")

    matrix_entries = []
    
    headers_frame = ttk.Frame(matrix_window, padding="5")
    headers_frame.pack()
    # Create n + 1 headers
    for j in range(n + 1):
        if j < n:
            label = ttk.Label(headers_frame, text=f"x{j+1}", width=8, font=('Arial', DEFAULT_FONT_SIZE, 'bold'))
        else:
            label = ttk.Label(headers_frame, text="=", width=4, font=('Arial', DEFAULT_FONT_SIZE, 'bold'))
            label.pack(side=tk.LEFT, padx=5)
            label = ttk.Label(headers_frame, text="b", width=8, font=('Arial', DEFAULT_FONT_SIZE, 'bold'))
        label.pack(side=tk.LEFT, padx=5)

    grid_frame = ttk.Frame(matrix_window, padding="10")
    grid_frame.pack()
    
    # Create m rows
    for i in range(m):
        row_entries = []
        grid_col = 0
        # Create n+1 columns
        for j in range(n + 1):
            entry = ttk.Entry(grid_frame, width=8, justify='center', font=('Arial', DEFAULT_FONT_SIZE))
            entry.grid(row=i, column=grid_col, padx=5, pady=5)
            row_entries.append(entry)
            grid_col += 1
            
            if j == n - 1: # If this is the last variable column
                label = ttk.Label(grid_frame, text="=")
                label.grid(row=i, column=grid_col, padx=5)
                grid_col += 1
        
        matrix_entries.append(row_entries)

    steps_frame = ttk.Frame(matrix_window, padding="10")
    steps_frame.pack(fill='both', expand=True)
    
    steps_label = ttk.Label(steps_frame, text="Steps:")
    steps_label.pack(anchor='w')
    
    steps_text = tk.Text(steps_frame, height=15, width=60, state='disabled', font=('Courier New', DEFAULT_FONT_SIZE))
    steps_text.pack(fill='both', expand=True)

    # Pass m and n to the solver
    solve_button = ttk.Button(matrix_window, text="Solve System", 
                              command=lambda: solve_system(matrix_entries, m, n, steps_text, current_method))
    solve_button.pack(pady=10)
    
    def on_matrix_close():
        root.deiconify() 
        matrix_window.destroy()
    
    matrix_window.protocol("WM_DELETE_WINDOW", on_matrix_close)

# ----- Setup the Main (Root) Window [MODIFIED for m x n] -----
root = tk.Tk()
root.title("Linear System Solver (m x n)")
root.geometry("400x320") 

# --- [FONT STYLE] ---
style = ttk.Style(root)
style.configure('.', font=('Arial', DEFAULT_FONT_SIZE))
style.configure('TLabel', font=('Arial', DEFAULT_FONT_SIZE))
style.configure('TButton', font=('Arial', DEFAULT_FONT_SIZE))
style.configure('TRadiobutton', font=('Arial', DEFAULT_FONT_SIZE))
# --- [END FONT STYLE] ---

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(expand=True)

method_label = ttk.Label(main_frame, text="Select Solver Method:")
method_label.pack(pady=5)

# Default to 'jordan' as it's better for m x n
method_var = tk.StringVar(value="jordan") 

gauss_radio = ttk.Radiobutton(main_frame, text="Gauss Elimination", variable=method_var, value="gauss")
gauss_radio.pack(anchor='w', padx=20)

jordan_radio = ttk.Radiobutton(main_frame, text="Gauss-Jordan", variable=method_var, value="jordan")
jordan_radio.pack(anchor='w', padx=20)

# --- [NEW m x n Inputs] ---
m_label = ttk.Label(main_frame, text="Number of Equations (Rows, m):")
m_label.pack(pady=(10, 0))
m_entry = ttk.Entry(main_frame, width=10, justify='center', font=('Arial', DEFAULT_FONT_SIZE))
m_entry.pack(pady=5)

n_label = ttk.Label(main_frame, text="Number of Variables (Columns, n):")
n_label.pack(pady=(10, 0))
n_entry = ttk.Entry(main_frame, width=10, justify='center', font=('Arial', DEFAULT_FONT_SIZE))
n_entry.pack(pady=5)
# --- [End of m x n Inputs] ---

create_grid_button = ttk.Button(main_frame, text="Create Input Grid", command=create_matrix_grid)
create_grid_button.pack(pady=10)

root.mainloop()
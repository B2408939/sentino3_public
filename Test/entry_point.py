import tkinter as tk
from tkinter import messagebox

import general
import introduce_text
def switch_tab(name, container, current_tab):
    current_tab.set(name)
    for widget in container.winfo_children():
        widget.destroy()
    
    if name == "General":
        general.start_gui(parent=container)
    elif name == "About":
        introduce_text.show_about_frame(container)

# Open menu
def open_help_window():
    help_win = tk.Toplevel()
    help_win.title("User Guide")
    help_win.geometry("600x500")
    help_win.resizable(False, False)

    tk.Label(help_win, text="How to use Sentino3", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(help_win, text="""
    1. Select a model from the list in center panel.
    2. Enter hyperparameters (if any) in the format: 'key: value', one per line.
    3. Click 'Save' to apply the hyperarameters. Click 'Reset' to clear all inputs.
    4. Choose a dataset (CSV file or build-in sample).
    5. Click 'Quick run' to test the model with default evaluation (prints accuracy).
    6. Click 'Avanced run' to run with more evaluation metrics.
    7. View results, accuracy, and visualization (label distribution chart).
    Example:
        max_iter: 200
        C: 0.5
        solver: 'lbfgs'
    The source code is organized into modules.
    You can run it directly or launch from 'entry_point.py'
""", justify="left", font=("Arial", 11)).pack(padx=25, anchor="w")

def start_app():
    root = tk.Tk()
    root.title("Sentino3 - Entry Point")
    root.geometry("900x700")

    current_tab = tk.StringVar(value="General")

    # Current tab label
    status_label = tk.Label(root, textvariable=current_tab, font=("Arial", 12, "bold"), fg="blue")
    status_label.pack(pady=(0, 5))

    menubar = tk.Menu(root)

    # Navigation menu
    nav_menu = tk.Menu(menubar, tearoff=0)
    nav_menu.add_command(label="General", command=lambda: switch_tab("General", container, current_tab))
    nav_menu.add_command(label="About", command=lambda: switch_tab("About", container, current_tab))
    menubar.add_cascade(label="Navigation", menu=nav_menu)

    # Default view
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="User Guide", command=open_help_window)
    menubar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menubar)

    container = tk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True)

    switch_tab("General", container, current_tab)

    root.mainloop()

if __name__ == "__main__":
    start_app()

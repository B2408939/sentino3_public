import tkinter as tk
from tkinter import filedialog, messagebox

from model_runner import run_models
from data_loader import open_file, load_sample_data, show_class_distribution
from utils import parse_params_from_text
from state import model_hyperparams, model_names
import state

import threading
import urllib.error
model_vars = {}

def on_run(col_listbox, models_vars, normalize):
    selected = col_listbox.curselection()
    if not selected:
        messagebox.showwarning("No Target Selected", "Please select a column to be the target.")
        return
    target_col = col_listbox.get(selected[0])
    selected_models = [name for name, var in model_vars.items() if var.get()]
    if not selected_models:
        messagebox.showwarning("No Model Selected", "Please select at least one model.")
        return
    result = run_models(target_col, selected_models, normalize.get())
    messagebox.showinfo("Results", result)

def on_show_metrics(col_listbox, models_vars, normalize):
    selected = col_listbox.curselection()
    if not selected:
        messagebox.showwarning("No Target Selected", "Please select a column to be the target.")
        return
    target_col = col_listbox.get(selected[0])
    selected_models = [name for name, var in model_vars.items() if var.get()]
    if not selected_models:
        messagebox.showwarning("No Model Selected", "Please select at least one model.")
        return
    report = run_models(target_col, selected_models, normalize.get(), detailed=True)

    detail_win = tk.Toplevel()
    detail_win.title("Detailed Model Report")
    text = tk.Text(detail_win, wrap=tk.WORD, font=("Courier", 10))
    text.insert(tk.END, report)
    text.pack(expand=True, fill=tk.BOTH)

def start_gui(parent):
    global run_button, run_infor_button, run_distribution_button
    model_vars.clear()

    my_font = ("Consolas", 10)
    root = tk.Frame(parent)
    root.pack(fill=tk.BOTH, expand=True)
    normalize_var = tk.BooleanVar()

    frame_left = tk.Frame(root)
    frame_center = tk.Frame(root)
    frame_right = tk.Frame(root)

    frame_left.grid(row=0, column=0, padx=20, pady=20, sticky="n")
    frame_center.grid(row=0, column=1, padx=20, pady=20, sticky="n")
    frame_right.grid(row=0, column=2, padx=20, pady=20, sticky="n")

    show_folds_var = tk.BooleanVar()
    tk.Checkbutton(frame_right, text="Print results for each fold", variable=show_folds_var).pack()

    split_method = tk.StringVar(value="Train/Test Split")

    fold_frame = tk.Frame(frame_center)
    tk.Label(fold_frame, text="Number of folds (K):", font=("Arial", 11)).pack(side=tk.LEFT)
    fold_entry = tk.Entry(fold_frame, width=5)
    fold_entry.insert(0, "5")
    fold_entry.pack(side=tk.LEFT, padx=5)

    split_text = tk.Text(frame_right, width=30, height=8, font=my_font)

    def update_split_config():
        raw_text = split_text.get("1.0", tk.END).strip()
        try:
            params = parse_params_from_text(raw_text) if raw_text else {}
            if split_method.get() == "K-Fold Cross Validation":
                k = int(fold_entry.get())
                params["n_splits"] = k
            state.split_config = {
                "method": split_method.get(),
                "params": params,
                "show_folds": show_folds_var.get()
            }
        except:
            pass

    def update_fold_visibility(*args):
        if split_method.get() == "K-Fold Cross Validation":
            fold_frame.pack(pady=(5, 0))
        else:
            fold_frame.pack_forget()
        update_split_config()

    tk.Label(frame_right, text="Data splitting method:", font=("Arial", 11)).pack()
    tk.OptionMenu(frame_right, split_method, "Train/Test Split", "K-Fold Cross Validation").pack(pady=(0, 10))
    tk.Label(frame_right, text="Split parameters:", font=("Arial", 10)).pack()
    split_text.pack()
    tk.Label(frame_right, text="E.g.: test_size: 0.3 or shuffle: True", font=("Arial", 9), fg="gray").pack(pady=(2, 0))

    split_method.trace_add("write", lambda *args: update_fold_visibility())
    update_fold_visibility()

    def save_split_config():
        try:
            update_split_config()
            messagebox.showinfo("Success", f"Split configuration saved:\n{state.split_config}")
        except Exception as e:
            messagebox.showerror("Syntax Error", str(e))

    def reset_split_config():
        state.split_config = {}
        split_text.delete("1.0", tk.END)

    btn_split = tk.Frame(frame_right)
    btn_split.pack(pady=(5, 0))
    tk.Button(btn_split, text="Save", width=10, command=save_split_config).pack(side=tk.LEFT, padx=(0, 10))
    tk.Button(btn_split, text="Reset", width=10, command=reset_split_config).pack(side=tk.LEFT)

    param_text = tk.Text(frame_left, width=35, height=12, font=my_font)
    param_text.pack()
    tk.Label(frame_left, text="Enter hyperparameters:").pack()
    selected_model_var = tk.StringVar(value=model_names[0])
    tk.OptionMenu(frame_left, selected_model_var, *model_names).pack(pady=(5, 0))

    def save_params():
        text = param_text.get("1.0", tk.END).strip()
        try:
            params = parse_params_from_text(text)
            model_hyperparams[selected_model_var.get()] = params
            messagebox.showinfo("Success", f"Parameters saved for {selected_model_var.get()}:\n{params}")
        except Exception as e:
            messagebox.showerror("Syntax Error", f"An error occurred:\n{e}")

    def reset_params():
        for k in model_hyperparams:
            model_hyperparams[k] = {}
        param_text.delete("1.0", tk.END)

    button_frame = tk.Frame(frame_left)
    button_frame.pack(pady=(5, 2))
    tk.Button(button_frame, text="Save", width=10, command=save_params).pack(side=tk.LEFT, padx=(0, 10))
    tk.Button(button_frame, text="Reset", width=10, command=reset_params).pack(side=tk.LEFT)

    col_listbox = tk.Listbox(frame_center, width=35, height=12, font=my_font, exportselection=False)
    col_listbox.pack()

    btn_file_frame = tk.Frame(frame_center)
    btn_file_frame.pack(pady=5)

    btn_csv = tk.Button(btn_file_frame, text="Select CSV file",
          command=lambda: open_file(col_listbox, run_button, run_infor_button, run_distribution_button))
    btn_csv.pack(side=tk.LEFT, padx=(0, 5))

    def open_sample_popup():
        popup = tk.Toplevel()
        popup.title("Select Sample Dataset")
        popup.geometry("400x300")
        tk.Label(popup, text="Select a sample dataset:", font=("Arial", 11)).pack(pady=10)

        datasets = ["Iris", "Wine", "Breast Cancer", "20 News groups"]

        def load_and_show(name):
            state.df = load_sample_data(name)
            if state.df is None:
                messagebox.showerror("Error", f"Unable to load sample dataset: {name}")
                return
            col_listbox.delete(0, tk.END)
            for col in state.df.columns:
                col_listbox.insert(tk.END, col)
            run_button.config(state=tk.NORMAL)
            run_infor_button.config(state=tk.NORMAL)
            run_distribution_button.config(state=tk.NORMAL)
        
            messagebox.showinfo("Success", f"Dataset loaded: {name}")
            popup.destroy()

        for ds in datasets:
            tk.Button(popup, text=ds, width=20, command=lambda name=ds: load_and_show(name)).pack(pady=3)

    btn_sample = tk.Button(btn_file_frame, text="Select Sample Data", command=open_sample_popup)
    btn_sample.pack(side=tk.LEFT)

    btn_frame = tk.Frame(frame_center)
    btn_frame.pack(pady=10)
    run_button = tk.Button(btn_frame, text="Quick Run", state=tk.DISABLED,
                           command=lambda: on_run(col_listbox, model_vars, normalize_var))
    run_button.pack(side=tk.LEFT, padx=5)

    run_infor_button = tk.Button(btn_frame, text="Advanced Run", state=tk.DISABLED,
                                 command=lambda: on_show_metrics(col_listbox, model_vars, normalize_var))
    run_infor_button.pack(side=tk.LEFT, padx=5)

    run_distribution_button = tk.Button(btn_frame, text="Label Distribution Chart", state=tk.DISABLED,
                                        command=show_class_distribution)
    run_distribution_button.pack(side=tk.LEFT, padx=5)

    tk.Label(frame_center, text="Additional options:", font=("Arial", 11)).pack(pady=(10, 0))
    tk.Checkbutton(frame_center, text="Normalize data (Standard Scaler)", variable=normalize_var,
                   font=("Arial", 11)).pack()

    tk.Label(frame_center, text="Select models to run:", font=("Arial", 11)).pack(pady=(10, 0))
    for name in model_names:
        var = tk.BooleanVar()
        tk.Checkbutton(frame_center, text=name, variable=var, font=("Arial", 11)).pack(anchor="w", padx=10)
        model_vars[name] = var

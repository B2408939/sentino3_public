import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import seaborn as sns
import matplotlib.pyplot as plt
import state
from sklearn.datasets import load_iris, load_wine, load_breast_cancer, fetch_20newsgroups


def open_file(col_listbox, run_button, run_infor_button, run_distribution_button):
    path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not path:
        return
    state.df = pd.read_csv(path)
    col_listbox.delete(0, tk.END)
    for col in state.df.columns:
        col_listbox.insert(tk.END, col)
    run_button.config(state=tk.NORMAL)
    run_infor_button.config(state=tk.NORMAL)
    run_distribution_button.config(state=tk.NORMAL)


def load_sample_data(name):
    if name == "Iris":
        data = load_iris(as_frame=True)
        df = data.frame
    elif name == "Wine":
        data = load_wine(as_frame=True)
        df = data.frame
    elif name == "Breast Cancer":
        data = load_breast_cancer(as_frame=True)
        df = data.frame
    elif name == "20 News groups":
        data = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))
        df = pd.DataFrame({
            "text": data.data,
            "target": data.target
        })
        df["target_name"] = [data.target_names[i] for i in data.target]
    else:
        messagebox.showerror("Lỗi", "Dataset không hợp lệ")
        return None

    state.df = df
    return state.df


def show_class_distribution():
    if state.df is None or state.df.empty:
        messagebox.showwarning("Chưa có dữ liệu", "Bạn chưa chọn file CSV hoặc dữ liệu trống.")
        return

    # Ưu tiên vẽ bằng "target_name" nếu có
    if "target_name" in state.df.columns:
        target_col = "target_name"
    elif "target" in state.df.columns:
        target_col = "target"
    else:
        target_col = None
        for col in state.df.columns:
            if state.df[col].nunique() <= 20 and state.df[col].dtype in ['int64', 'object']:
                target_col = col
                break

    if not target_col:
        messagebox.showwarning("Không tìm thấy nhãn", "Không có cột nào phù hợp làm nhãn.")
        return

    plt.figure(figsize=(8, 5))
    sns.countplot(x=state.df[target_col], order=sorted(state.df[target_col].unique()))
    plt.title("Phân phối các nhãn")
    plt.xlabel("Nhãn")
    plt.ylabel("Số lượng")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

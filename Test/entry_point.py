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

# 👉 Trang trợ giúp mở trong cửa sổ riêng
def open_help_window():
    help_win = tk.Toplevel()
    help_win.title("Hướng dẫn sử dụng Sentino3")
    help_win.geometry("600x500")
    help_win.resizable(False, False)

    tk.Label(help_win, text="Hướng dẫn sử dụng Sentino3", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(help_win, text="""
    1. Chọn mô hình từ danh sách mô hình ở giữa.
    2. Nhập siêu tham số (Nếu có) theo cú pháp: key: value, mỗi dòng một tham số.
    3. Ấn lưu để đưa siêu tham số vào mô hình. Ấn reset sẽ xóa hết tất.
    4. Chọn datasets (file định dạng CSV hoặc datasets có sẵn).
    5. Nhấn "Chạy nhanh" để thử nhanh mô hình (In độ chính xác).
    6. Nhấn "Chạy chuyên sâu" để thử với nhiều đánh giá hơn.
    7. Xem kết quả, độ chính xác, và đồ thị minh hoạ (Tần xuất nhãn).
    Ví dụ:
        max_iter: 200
        C: 0.5
        solver: 'lbfgs'
    Mã nguồn gồm nhiều module để chạy.
    Có thể chạy trực tiếp hoặc qua file "entry_point.py"
""", justify="left", font=("Arial", 11)).pack(padx=25, anchor="w")

def start_app():
    root = tk.Tk()
    root.title("Sentino3 - Entry Point")
    root.geometry("900x700")

    current_tab = tk.StringVar(value="General")

    # Label hiển thị tên tab hiện tại
    status_label = tk.Label(root, textvariable=current_tab, font=("Arial", 12, "bold"), fg="blue")
    status_label.pack(pady=(0, 5))

    menubar = tk.Menu(root)

    # Menu điều hướng
    nav_menu = tk.Menu(menubar, tearoff=0)
    nav_menu.add_command(label="General", command=lambda: switch_tab("General", container, current_tab))
    nav_menu.add_command(label="About", command=lambda: switch_tab("About", container, current_tab))
    menubar.add_cascade(label="Điều hướng", menu=nav_menu)

    # Menu trợ giúp
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="Hướng dẫn sử dụng", command=open_help_window)
    menubar.add_cascade(label="Trợ giúp", menu=help_menu)

    root.config(menu=menubar)

    container = tk.Frame(root)
    container.pack(fill=tk.BOTH, expand=True)

    # Giao diện mặc định
    switch_tab("General", container, current_tab)

    root.mainloop()

if __name__ == "__main__":
    start_app()
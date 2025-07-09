import tkinter as tk

def show_about_frame(parent):
    frame = tk.Frame(parent)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Version: 1.0", font=("Arial", 13)).pack()
    tk.Label(frame, text="Developed by B24 with ChatGPT", font=("Arial", 13)).pack(pady=(0, 30))
    description = (
        "Sentino3 is a simple yet powerful AutoML graphical user interface designed for students, "
        "researchers, and developers who want to explore machine learning without writing complex code. "
        "\n\nThis tool provides an intuitive workflow that allows users to quickly import datasets, "
        "select target columns, configure model hyperparameters, and evaluate model performance—all through a clean, interactive interface. "
        "\n\nSentino3 supports multiple popular classification algorithms such as Logistic Regression, "
        "Decision Trees, Random Forest, SVM, and K-Nearest Neighbors, making it ideal for academic projects, learning, and prototyping."
        "\n\nOur mission is to make machine learning more accessible by simplifying experimentation, "
        "reducing the need for manual scripting, and enabling insights through automation."
    )
    tk.Label(frame, text=description, font=("Arial", 11), wraplength=700, justify="left").pack(padx=20)

    return frame

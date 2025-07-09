> **Challenge: This entire project was built solely through conversations with ChatGPT.**  
> No external documentation, no Stack Overflow, no help from other people.  
> Every line of code, every design decision, and every feature idea came from chatting with AI – step by step.

# sentino3_public
A simple and modular AutoML graphical user interface application designed to help users easily train, test, and evaluate machine learning models. Sentino3 supports importing external models, managing datasets, tuning hyperparameters, and visualizing results, making AutoML accessible for both beginners and advanced users.
# Sentino3 - AutoML GUI (Test Version)

This code was co-developed with the assistance of **ChatGPT (OpenAI - GPT-4o)**.
---
<pre>
Folder Structure
/Test/
│
├── data_csv/
│ ├── Iris.csv # Sample dataset: Iris
│ ├── winequality_red.csv # Sample dataset: Red wine
│ └── winequality_white.csv # Sample dataset: White wine
│
├── data_loader.py # Functions for loading and preprocessing datasets
├── entry_point.py # Main entry point for launching the GUI
├── general.py # General-purpose utility functions
├── introduce_text.py # Introductory text for display in the GUI
├── model_runner.py # Core logic for model training and evaluation
├── state.py # Global variables and shared application state
└── utils.py # Hyperparameter parsing and other helper functions
</pre>

## How to Run

1. **Clone the repository** or download the `/Test/` folder.
2. **Install dependencies** (if not already installed):
3. **Run entry_point.py**

Key Features
User-friendly Tkinter interface
Supports various ML models: Decision Tree, Random Forest, KNN, SVM, etc.
Allows manual input of hyperparameters
Lets users select the target column easily
Visualizes dataset distribution and model performance
Works with built-in or custom CSV datasets

Notes
This is an early-stage prototype. Advanced features may not be fully implemented yet.
The goal is to create a beginner-friendly AutoML experience with modular extensibility.
The source code was developed with support from ChatGPT (OpenAI), and is intended for educational and prototyping purposes.

Dev: B24


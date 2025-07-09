# state.py
model_names = ["Logistic Regression", "Decision Tree", "Random Forest", "SVM", "KNN"]
model_hyperparams = {name: {} for name in model_names}
df = None
split_config = {}  # Include: {"method": "Train/Test Split", "params": {"test_size": 0.2, "random_state": 42}}

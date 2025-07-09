import time
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import state
from state import model_hyperparams

def run_models(target_col, selected_models, normalize=False, detailed=False):
    if state.df is None:
        return "No data available!"

    try:
        X = state.df.drop(columns=[target_col])
        y = state.df[target_col]

        if normalize:
            scaler = StandardScaler()
            X = scaler.fit_transform(X)
            
            import pandas as pd
            X = pd.DataFrame(X, columns=state.df.drop(columns=[target_col]).columns)

        split_conf = state.split_config or {}
        method = split_conf.get("method", "Train/Test Split")
        params = split_conf.get("params", {})
        show_folds = split_conf.get("show_folds", False)

        results = []
        for model_name in selected_models:
            params_model = model_hyperparams.get(model_name, {})
            try:
                if model_name == "Logistic Regression":
                    model = LogisticRegression(**params_model)
                elif model_name == "Decision Tree":
                    model = DecisionTreeClassifier(**params_model)
                elif model_name == "Random Forest":
                    model = RandomForestClassifier(**params_model)
                elif model_name == "SVM":
                    model = SVC(**params_model)
                elif model_name == "KNN":
                    model = KNeighborsClassifier(**params_model)
                else:
                    results.append(f"Unable to recognize the model {model_name}")
                    continue

                start_time = time.time()

                if method == "Train/Test Split":
                    X_train, X_test, y_train, y_test = train_test_split(X, y, **params)
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    acc = accuracy_score(y_test, y_pred)
                    elapsed = time.time() - start_time

                    if detailed:
                        results.append(f"\n{model_name} (Train/Test)\n")
                        results.append(classification_report(y_test, y_pred, zero_division=0))
                        results.append(f"(Runtime: {elapsed:.2f} sec)\n")
                        results.append("-" * 60 + "\n")
                    else:
                        results.append(f"{model_name}: {acc:.2%} (Runtime: {elapsed:.2f} sec)")

                elif method == "K-Fold Cross Validation":
                    kf = KFold(**params)
                    fold_accs = []
                    fold = 1
                    y_preds_all = []
                    y_tests_all = []
                    for train_idx, test_idx in kf.split(X):
                        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
                        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
                        model.fit(X_train, y_train)
                        y_pred = model.predict(X_test)
                        acc = accuracy_score(y_test, y_pred)
                        fold_accs.append(acc)
                        if show_folds:
                            results.append(f"Fold {fold} - {model_name}: {acc:.2%}")
                        if detailed:
                            y_preds_all.extend(y_pred)
                            y_tests_all.extend(y_test)
                        fold += 1
                    elapsed = time.time() - start_time

                    if detailed:
                        results.append(f"\n{model_name} (K-Fold)\n")
                        results.append(classification_report(y_tests_all, y_preds_all, zero_division=0))
                        results.append(f"(Runtime: {elapsed:.2f} sec)\n")
                        results.append("-" * 60 + "\n")
                    else:
                        mean_acc = sum(fold_accs) / len(fold_accs)
                        results.append(f"{model_name} (K-Fold): {mean_acc:.2%} (Runtime: {elapsed:.2f} sec)")

            except Exception as model_err:
                results.append(f"{model_name} Error: {model_err}")

        return "\n".join(results)
    except Exception as e:
        return f"🔥 Error: {e}"

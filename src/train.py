import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("data/dataset.csv")
X = df.drop(columns=["label"])
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

models = {
    "RandomForest": RandomForestClassifier(n_estimators=300, random_state=42),
    "GradientBoosting": HistGradientBoostingClassifier(random_state=42),
}

best_name, best_score = None, 0
for name, m in models.items():
    score = cross_val_score(m, X_train, y_train, cv=5).mean()
    print(f"{name}: CV accuracy {score:.3f}")
    if score > best_score:
        best_name, best_score = name, score

model = models[best_name].fit(X_train, y_train)
pred = model.predict(X_test)
print(f"\n=== Best: {best_name} ===")
print(classification_report(y_test, pred, target_names=["safe", "phishing"]))
print("Confusion matrix:")
print(confusion_matrix(y_test, pred))

imp = permutation_importance(model, X_test, y_test, n_repeats=5, random_state=42)
print("\n=== Feature importance ===")
print(pd.Series(imp.importances_mean, index=X.columns).sort_values(ascending=False).round(3))

joblib.dump(model, "model.pkl")
print("\nSaved model.pkl")

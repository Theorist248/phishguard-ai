import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv("data/dataset.csv")
X = df.drop(columns=["label"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print("=== Test results ===")
print(classification_report(y_test, pred, target_names=["safe", "phishing"]))
print("Confusion matrix (rows=actual, cols=predicted):")
print(confusion_matrix(y_test, pred))

scores = cross_val_score(model, X, y, cv=5)
print(f"\n5-fold CV accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})")

print("\n=== Feature importance ===")
imp = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print(imp.round(3))

joblib.dump(model, "model.pkl")
print("\nSaved model.pkl")

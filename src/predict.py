import sys
import joblib
import pandas as pd
from src.features import extract_features

model = joblib.load("model.pkl")

def predict(url):
    X = pd.DataFrame([extract_features(url)])
    return round(model.predict_proba(X)[0][1] * 100)

if __name__ == "__main__":
    for u in sys.argv[1:]:
        print(f"{predict(u):>3}% phishing  {u}")

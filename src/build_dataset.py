import pandas as pd
from src.features import extract_features

phish = [u.strip() for u in open("data/phishing_urls.txt") if u.strip()]
safe = (pd.read_csv("data/top-1m.csv", header=None, names=["rank", "domain"])
          .head(50000).sample(len(phish), random_state=42)["domain"].tolist())

rows = [dict(extract_features(u), label=1) for u in phish]
rows += [dict(extract_features(d), label=0) for d in safe]

df = pd.DataFrame(rows).sample(frac=1, random_state=42)
df.to_csv("data/dataset.csv", index=False)
print(df["label"].value_counts())
print(df.head())

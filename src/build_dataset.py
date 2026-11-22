import random
import pandas as pd
from src.features import extract_features

random.seed(42)
N = 5000

phish = set()
for f in ["data/phishing_urls.txt", "data/phishing_links_big.txt"]:
    try:
        phish |= {u.strip() for u in open(f, errors="ignore") if u.strip().startswith("http")}
    except FileNotFoundError:
        pass
phish = random.sample(sorted(phish), min(N, len(phish)))

SUBS = ["", "", "www.", "www.", "mail.", "accounts.", "login.", "m.", "support.", "secure.", "api."]
top = pd.read_csv("data/top-1m.csv", header=None, names=["rank", "domain"]).head(30000)
safe = [random.choice(SUBS) + d for d in top["domain"].sample(len(phish), random_state=42)]

rows = [dict(extract_features(u), label=1) for u in phish]
rows += [dict(extract_features(d), label=0) for d in safe]

df = pd.DataFrame(rows).sample(frac=1, random_state=42)
df.to_csv("data/dataset.csv", index=False)
print(df["label"].value_counts())

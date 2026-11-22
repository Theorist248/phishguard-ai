import joblib
import pandas as pd
import streamlit as st
import tldextract
from src.features import extract_features

st.set_page_config(page_title="PhishGuard AI", page_icon="🛡️")
model = joblib.load("model.pkl")

_ext = tldextract.TLDExtract(suffix_list_urls=())
TOP = set(open("data/top10k.txt").read().split())


def registered_domain(u):
    if not u.startswith(("http://", "https://")):
        u = "http://" + u
    e = _ext(u)
    return f"{e.domain}.{e.suffix}"


def explain(f):
    reasons = []
    if f["is_free_host"]: reasons.append("Hosted on a free website platform (common for throwaway phishing pages)")
    if f["bad_tld"]: reasons.append("Uses a TLD that is heavily abused for phishing (.xyz, .top, .click...)")
    if f["keyword_count"]: reasons.append(f"Contains {f['keyword_count']} sensitive keyword(s) like login/verify/kyc/upi")
    if f["brand_in_subdomain"]: reasons.append("A well-known brand name appears in the subdomain (impersonation pattern)")
    if f["brand_in_domain"]: reasons.append("A well-known brand name is embedded in a different domain (impersonation pattern)")
    if f["has_ip"]: reasons.append("Uses a raw IP address instead of a domain name")
    if f["has_at"]: reasons.append("Contains '@', which can hide the real destination")
    if f["is_shortener"]: reasons.append("Uses a URL shortener that hides the real destination")
    if f["num_hyphens"] >= 2: reasons.append(f"Many hyphens ({f['num_hyphens']}) in the hostname")
    if f["digit_ratio"] > 0.2: reasons.append("High proportion of digits in the hostname")
    if f["longest_token"] > 15: reasons.append("Contains a very long, unusual word in the hostname")
    if f["domain_entropy"] > 3.5: reasons.append("Domain name looks random (high entropy)")
    return reasons


st.title("🛡️ PhishGuard AI")
st.caption("Paste a URL to get a phishing risk score. The URL is analysed as text only and is never visited.")

url = st.text_input("URL to check", placeholder="e.g. sbi-login-verify.xyz")

if st.button("Analyse") and url.strip():
    feats = extract_features(url.strip())
    score = round(model.predict_proba(pd.DataFrame([feats]))[0][1] * 100)

    known = registered_domain(url.strip()) in TOP
    if feats["is_free_host"]:
        known = False

    if known:
        st.success(f"✅ Known popular domain (Tranco top 10k). Model score: {score}%")
    elif score >= 70:
        st.error(f"🚨 Likely PHISHING: {score}% risk")
    elif score >= 30:
        st.warning(f"⚠️ SUSPICIOUS: {score}% risk")
    else:
        st.success(f"✅ Looks SAFE: {score}% risk")
    st.progress(score / 100)

    st.subheader("Why?")
    reasons = explain(feats)
    if reasons:
        for r in reasons:
            st.write("•", r)
    else:
        st.write("No red-flag patterns found in the hostname.")

    with st.expander("Raw features the model saw"):
        st.json(feats)

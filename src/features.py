import math
import re
from collections import Counter
from urllib.parse import urlparse
import tldextract

_extract = tldextract.TLDExtract(suffix_list_urls=())

KEYWORDS = ["login", "verify", "secure", "account", "update", "upi", "kyc",
            "bank", "wallet", "signin", "confirm", "password", "gift", "reward"]
BRANDS = ["paypal", "google", "facebook", "instagram", "amazon", "microsoft", "apple",
          "netflix", "sbi", "hdfc", "icici", "axis", "paytm", "phonepe", "gpay",
          "flipkart", "whatsapp", "irctc", "kotak", "airtel", "jio", "roblox"]
FREE_HOSTS = ["blogspot.com", "vercel.app", "netlify.app", "github.io", "weebly.com",
              "wixsite.com", "000webhostapp.com", "web.app", "pages.dev", "workers.dev"]
SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "rb.gy"]
BAD_TLDS = ["xyz", "top", "click", "icu", "tk", "ml", "ga", "cf", "gq", "live", "buzz", "shop", "site"]


def _entropy(s):
    if not s:
        return 0.0
    n = len(s)
    return -sum(c / n * math.log2(c / n) for c in Counter(s).values())


def extract_features(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    host = (urlparse(url).hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    ext = _extract("http://" + host)
    registered = f"{ext.domain}.{ext.suffix}"
    tokens = [t for t in re.split(r"[.\-]", host) if t]
    letters = [c for c in ext.domain if c.isalpha()]

    return {
        "host_length": len(host),
        "domain_length": len(ext.domain),
        "num_dots": host.count("."),
        "num_hyphens": host.count("-"),
        "num_digits": sum(c.isdigit() for c in host),
        "digit_ratio": sum(c.isdigit() for c in host) / max(len(host), 1),
        "subdomain_count": len(ext.subdomain.split(".")) if ext.subdomain else 0,
        "domain_entropy": _entropy(ext.domain),
        "vowel_ratio": sum(c in "aeiou" for c in letters) / max(len(letters), 1),
        "longest_token": max((len(t) for t in tokens), default=0),
        "num_tokens": len(tokens),
        "tld_len": len(ext.suffix),
        "is_com": int(ext.suffix == "com"),
        "has_ip": int(bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host))),
        "has_at": int("@" in url),
        "is_free_host": int(registered in FREE_HOSTS),
        "is_shortener": int(registered in SHORTENERS),
        "bad_tld": int(ext.suffix in BAD_TLDS),
        "keyword_count": sum(k in host for k in KEYWORDS),
        "brand_in_subdomain": int(any(b in ext.subdomain for b in BRANDS)),
        "brand_in_domain": int(any(b in ext.domain and ext.domain != b for b in BRANDS)),
    }

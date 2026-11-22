import re
from urllib.parse import urlparse
import tldextract

_extract = tldextract.TLDExtract(suffix_list_urls=())

KEYWORDS = ["login", "verify", "secure", "account", "update", "upi", "kyc",
            "bank", "wallet", "signin", "confirm", "password", "gift", "reward"]
FREE_HOSTS = ["blogspot.com", "vercel.app", "netlify.app", "github.io", "weebly.com",
              "wixsite.com", "000webhostapp.com", "web.app", "pages.dev", "workers.dev"]
SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "rb.gy"]
BAD_TLDS = ["xyz", "top", "click", "icu", "tk", "ml", "ga", "cf", "gq", "live", "buzz", "shop", "site"]


def extract_features(url):
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    host = (urlparse(url).hostname or "").lower()
    ext = _extract(url)
    registered = f"{ext.domain}.{ext.suffix}"

    return {
        "host_length": len(host),
        "num_dots": host.count("."),
        "num_hyphens": host.count("-"),
        "num_digits": sum(c.isdigit() for c in host),
        "subdomain_count": len(ext.subdomain.split(".")) if ext.subdomain else 0,
        "has_ip": int(bool(re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host))),
        "has_at": int("@" in url),
        "is_free_host": int(registered in FREE_HOSTS),
        "is_shortener": int(registered in SHORTENERS),
        "bad_tld": int(ext.suffix in BAD_TLDS),
        "keyword_count": sum(k in host for k in KEYWORDS),
    }

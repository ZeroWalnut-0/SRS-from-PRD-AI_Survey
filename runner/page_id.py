from __future__ import annotations
import os
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

def extract_page_id(url: str, html: str) -> str:
    u = url or ""
    try:
        qs = parse_qs(urlparse(u).query)
        for k in ("PAGE", "Page", "page", "NPAGE", "npage"):
            if k in qs and qs[k]:
                v = str(qs[k][0]).strip()
                if v:
                    return v
    except Exception:
        pass

    try:
        soup = BeautifulSoup(html or "", "lxml")
        for nm in ("PAGE", "Page", "page", "NPAGE", "npage", "VARS", "VAR", "QNum"):
            el = soup.select_one(f'input[name="{nm}"]') or soup.select_one(f'input[id="{nm}"]')
            if el:
                v = (el.get("value") or "").strip()
                if v:
                    return v
    except Exception:
        pass

    try:
        path = urlparse(u).path or ""
        stem = os.path.splitext(os.path.basename(path))[0]
        if stem:
            return stem
    except Exception:
        pass

    return u or "UNKNOWN"

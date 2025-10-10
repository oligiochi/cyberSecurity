#!/usr/bin/env python3
"""
csrf_scanner.py - modulo riutilizzabile

Espone:
  - sniff_csrf(url, do_test_post=False, session=None, verbose=True)
     -> ritorna un dict con i risultati
"""

import requests
import re
from bs4 import BeautifulSoup

COMMON_CSRF_NAMES = [
    "csrfmiddlewaretoken", "csrf_token", "csrf", "csrftoken",
    "XSRF-TOKEN", "_csrf", "_csrf_token", "token", "anti_csrf"
]

def _fetch(session, url):
    try:
        return session.get(url, timeout=10)
    except Exception as e:
        return None

def _find_tokens_in_html(html):
    soup = BeautifulSoup(html or "", "html.parser")
    findings = []
    forms = []

    # input hidden
    for inp in soup.find_all("input", {"type": "hidden"}):
        name = inp.get("name")
        val = inp.get("value", "")
        findings.append(("form-hidden", name, val))

    # forms
    for f in soup.find_all("form"):
        forms.append({
            "action": f.get("action"),
            "method": f.get("method", "GET").upper(),
            "inputs": [(i.get("name"), i.get("type")) for i in f.find_all("input")]
        })

    # meta tags
    for meta in soup.find_all("meta"):
        mname = meta.get("name") or meta.get("id")
        content = meta.get("content")
        if mname and content:
            findings.append(("meta", mname, content))

    # JS inline simple regex
    m = re.findall(r"(?:csrf[_-]?token|csrfToken|CSRF_TOKEN|XSRF-TOKEN)['\"\s:=]*['\"]?([A-Za-z0-9\-\._=]+)['\"]?", html or "")
    for found in m:
        findings.append(("js-token", None, found))

    return findings, forms

def _find_tokens_in_cookies(session):
    d = session.cookies.get_dict()
    findings = []
    for k, v in d.items():
        if any(c.lower() in k.lower() for c in ["csrf", "xsrf", "token"]):
            findings.append(("cookie", k, v))
    return findings

def _try_post(session, url, data=None, json_body=None, headers=None):
    try:
        if json_body is not None:
            return session.post(url, json=json_body, headers=headers or {}, timeout=8)
        else:
            return session.post(url, data=(data or {}), headers=headers or {}, timeout=8)
    except Exception as e:
        return None

def sniff_csrf(url, do_test_post=False, session=None, verbose=True):
    """
    Esegue analisi CSRF sulla pagina `url`.
    Parametri:
      - url: pagina da GETtare (string)
      - do_test_post: se True prova POST di test (non distruttivo)
      - session: optional requests.Session() da riusare (se None ne crea una)
      - verbose: se True stampa info a stdout
    Ritorna:
      dict con campi:
        - status_get, allow_methods, findings_html, forms, cookie_findings,
          probable_names (list), post_tests (dettagli sui test se fatti)
    """
    session = session or requests.Session()
    session.headers.update({"User-Agent": "csrf-scanner/1.0"})
    result = {
        "url": url,
        "status_get": None,
        "allow_methods": None,
        "findings_html": [],
        "forms": [],
        "cookie_findings": [],
        "probable_names": [],
        "post_tests": []
    }

    r = _fetch(session, url)
    if not r:
        if verbose:
            print(f"[!] GET fallita per {url}")
        return result

    result["status_get"] = r.status_code

    # OPTIONS
    try:
        opt = session.options(url, timeout=6)
        result["allow_methods"] = opt.headers.get("Allow") or opt.headers.get("allow")
    except Exception:
        result["allow_methods"] = None

    html = r.text

    findings_html, forms = _find_tokens_in_html(html)
    cookie_findings = _find_tokens_in_cookies(session)

    result["findings_html"] = findings_html
    result["forms"] = forms
    result["cookie_findings"] = cookie_findings

    probable = set()
    for source, name, val in findings_html + cookie_findings:
        if name:
            probable.add(name)
    probable.update(COMMON_CSRF_NAMES)
    result["probable_names"] = sorted(probable)

    if verbose:
        print(f"[+] GET {url} -> {r.status_code}")
        print(f"[+] OPTIONS Allow: {result['allow_methods']}")
        print(" - findings_html:", findings_html)
        print(" - cookie_findings:", cookie_findings)
        print(" - probable token names:", result["probable_names"])

    # test POST se richiesto
    if do_test_post:
        if verbose:
            print("[*] Eseguo test POST non distruttivi...")
        test_payload = {"test_param": "csrf_test"}
        test_results = []

        # POST senza token
        r_no = _try_post(session, url, data=test_payload)
        test_results.append({"type": "no_token", "status": getattr(r_no, "status_code", None), "len": len(r_no.text) if r_no else None})
        if verbose:
            print(f"  POST senza token -> {getattr(r_no,'status_code',None)}")

        # tenta invio con token preso da first form-hidden
        token_sent = False
        token_name = None
        token_val = None
        for t in findings_html:
            if t[0] == "form-hidden" and t[1]:
                token_name, token_val = t[1], t[2] or "SCANNER_DUMMY"
                break
        if not token_name and cookie_findings:
            token_name, token_val = cookie_findings[0][1], cookie_findings[0][2]

        if token_name:
            # form field
            payload = dict(test_payload)
            payload[token_name] = token_val
            r_with = _try_post(session, url, data=payload)
            test_results.append({"type": "with_token_field", "field": token_name, "status": getattr(r_with, "status_code", None), "len": len(r_with.text) if r_with else None})
            if verbose:
                print(f"  POST con token field '{token_name}' -> {getattr(r_with,'status_code',None)}")

            # header double-submit (se cookie token)
            headers = {"X-CSRFToken": token_val, "X-CSRF-Token": token_val}
            r_hdr = _try_post(session, url, data=test_payload, headers=headers)
            test_results.append({"type": "header_token", "header_names": ["X-CSRFToken","X-CSRF-Token"], "status": getattr(r_hdr, "status_code", None), "len": len(r_hdr.text) if r_hdr else None})
            if verbose:
                print(f"  POST double-submit header -> {getattr(r_hdr,'status_code',None)}")
            token_sent = True

        result["post_tests"] = test_results

    return result

# CLI wrapper per backward compatibility
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("url")
    p.add_argument("--test-post", action="store_true")
    args = p.parse_args()
    res = sniff_csrf(args.url, do_test_post=args.test_post, verbose=True)
    # stampa compatta finale
    print("\n=== SUMMARY ===")
    print("Result keys:", list(res.keys()))

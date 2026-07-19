import sys
import json
import requests
from bs4 import BeautifulSoup


def fetch(username, out="contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    r = requests.get(
        url,
        headers={"X-Requested-With": "XMLHttpRequest", "User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    days = {}
    for el in soup.find_all(attrs={"data-date": True}):
        d = el.get("data-date")
        lvl = int(el.get("data-level") or 0)
        if d:
            days[d] = lvl
    with open(out, "w") as f:
        json.dump(days, f)
    print(f"Fetched {len(days)} days → {out}")


if __name__ == "__main__":
    fetch(
        sys.argv[1] if len(sys.argv) > 1 else "pers-fs",
        sys.argv[2] if len(sys.argv) > 2 else "contributions.json",
    )

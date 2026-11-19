"""Read a published four-vertex trial. Record. Decide nothing."""
from __future__ import annotations
import json
import urllib.request

URL = "https://raw.githubusercontent.com/jacksonjp0311-gif/locus/main/data/commons/four_vertex.jsonl"


def read_trials() -> dict:
    try:
        with urllib.request.urlopen(URL, timeout=12) as r:
            lines = r.read().decode().splitlines()
        n = 0
        accepted = 0
        for line in lines:
            try:
                t = json.loads(line)
            except Exception:
                continue
            n += 1
            if t.get("evaluate", {}).get("accept"):
                accepted += 1
        return {"available": True, "n": n, "accepted": accepted}
    except Exception:
        return {"available": False, "n": 0, "accepted": 0}


if __name__ == "__main__":
    print(json.dumps(read_trials()))

"""Witness. Third vertex.

Pattern: read both lineages. Score. Append a receipt.
Never keep. Never mutate. Fail open.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXCHANGE = ROOT / "data" / "commons" / "exchange.jsonl"
RECEIPT = ROOT / "data" / "commons" / "witness.jsonl"


FEEDS = {
    "colony": "https://raw.githubusercontent.com/jacksonjp0311-gif/agent-colony/main/data/commons/exchange.jsonl",
    "one-mind": "https://raw.githubusercontent.com/jacksonjp0311-gif/one-mind/main/data/commons/exchange.jsonl",
}


def read_remote() -> dict:
    """Fetch public exchanges. Unavailable is not zero."""
    import urllib.request
    out = {}
    for name, url in FEEDS.items():
        try:
            with urllib.request.urlopen(url, timeout=12) as r:
                lines = r.read().decode().splitlines()[-400:]
            recs = []
            for line in lines:
                try:
                    recs.append(json.loads(line))
                except Exception:
                    continue
            out[name] = {"available": True, "records": recs, "n": len(recs)}
        except Exception:
            out[name] = {"available": False, "records": [], "n": 0}
    return out


def read_exchange() -> list:
    remote = read_remote()
    recs = []
    for name, pack in remote.items():
        recs.extend(pack["records"])
    if recs:
        return recs
    if not EXCHANGE.exists():
        return []
    out = []
    for line in EXCHANGE.read_text(encoding="utf-8").splitlines()[-400:]:
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def score(records: list) -> dict:
    colony = sum(1 for r in records if r.get("source") == "colony")
    one_mind = sum(1 for r in records if r.get("source") == "one-mind")
    return {"colony": colony, "one-mind": one_mind, "total": len(records)}


def append(rec: dict) -> None:
    if not rec:
        return
    try:
        RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        with RECEIPT.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec) + "\n")
    except Exception:
        return


def cycle() -> dict:
    """One witness pass. Read, score, append. Decide nothing."""
    try:
        t = ROOT / "TRANSLATOR.md"
        if t.exists():
            t.read_text(encoding="utf-8")
    except Exception:
        pass
    records = read_exchange()
    s = score(records)
    rec = {"source": "witness", "kind": "observation", **s}
    append(rec)
    return rec


if __name__ == "__main__":
    print(json.dumps(cycle()))

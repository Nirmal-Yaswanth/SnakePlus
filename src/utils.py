import json
from pathlib import Path

HIGH_SCORE_FILE = Path(__file__).resolve().parent / "highscore.txt"

def load_highscore():
    if HIGH_SCORE_FILE.exists():
        try:
            with open(HIGH_SCORE_FILE, "r") as f:
                return json.load(f).get("best", 0)
        except Exception:
            return 0
    return 0

def save_highscore(score):
    best = load_highscore()
    if score > best:
        with open(HIGH_SCORE_FILE, "w") as f:
            json.dump({"best": score}, f)
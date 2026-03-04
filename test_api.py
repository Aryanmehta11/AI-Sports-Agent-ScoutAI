from sports_api import get_live_matches

matches = get_live_matches()

for m in matches[:3]:

    print("Match:", m["name"])
    print("Status:", m["status"])
    print("Teams:", m["teams"])
    print("Score:", m.get("score"))
    print("----")
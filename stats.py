import json
import oll

ALL_STATS = {}
with open("data.json", "r") as f:
	s = f.read()
	if s:
		ALL_STATS = json.loads(s)

OLL_STATS = ALL_STATS["OLL"]
OLL_count = OLL_STATS["count"]
for case in OLL_STATS["encounters"]:
	OLL_count += case["reps"]

def stats_oll():
	oll_stats = [(case["reps"],case["str"]) for case in OLL_STATS["encounters"]]
	for case in sorted(oll_stats,reverse=True):
		percent = round(case[0]/OLL_count * 100, 2)
		print(f"{percent}%", f"({case[0]}/{OLL_count})")
		oll.str_to_oll(case[1]).visualize()
		print()


if __name__ == "__main__":
	pass
import json
import oll

ALL_STATS = {}
with open("data.json", "r") as f:
	s = f.read()
	if s:
		ALL_STATS = json.loads(s)

OLL_STATS = ALL_STATS["OLL"]
OLL_count = 0
for case in OLL_STATS:
	OLL_count += case["reps"]
# print("Total OLL encounters:", OLL_count)


def stats_oll():
	oll_stats = [(case["reps"],case["str"]) for case in OLL_STATS]
	for case in sorted(oll_stats,reverse=True):
		percent = round(case[0]/OLL_count * 100, 2)
		print(f"{percent}%", f"({case[0]}/{OLL_count})")
		oll.str_to_oll(case[1]).visualize()
		print()


if __name__ == "__main__":
	pass
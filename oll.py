# This project aims to record the statistic of how likely a case in PLL or OLL appears in my practice solves
# by inputting a case I encounter while I solve

import sys # for commandline arguments
import json

SHADE_CHAR:str; NO_SHADE_CHAR:str; DISPLAY_SHADE_CHAR:str
# LOADING CONFIG
with open(".cfg", "r", encoding="UTF-8") as f:
	s = json.loads(f.read())
	SHADE_CHAR = s["OLL"]["shade"]
	NO_SHADE_CHAR = s["OLL"]["no_shade"]
	DISPLAY_SHADE_CHAR = s["OLL"]["display_shade"]

class Oll:
	def __init__(self) -> None:
		self.values = [[False for j in range(3)] for i in range(4)]

	def print(self) -> None:
		s = ""
		for i in self.values:
			for j in i:
				s += Oll.convert(j)
			s += " "
		print(s)

	def visualize(self) -> None:
		# FIRST LINE
		s = "  "
		for i in self.values[0]:
			s += Oll.convert(i,"-")
		print(s)

		# TOP LAYER AND ITS SIDES
		top_layer = self.get_top_layer()
		for i in range(3):
			s = Oll.convert(self.values[3][2-i],"|")
			for j in top_layer[i]:
				s += Oll.convert(j)
			s += Oll.convert(self.values[1][i],"|")
			print(s)

		# LAST LINE
		s = "  "
		for i in reversed(self.values[2]):
			s += Oll.convert(i,"-")
		print(s)

	def get_top_layer(self):
		flat_values = [j for i in self.values for j in i]
		top_layer = [[False for j in range(3)] if i!=1 else [False, True, False] for i in range(3)]

		# print(flat_values)
		for i in range(len(flat_values)):
			# print(i, i//3, i%3) if i%3==0 or i%3==1 else None
			match (i % 3):
				case 0:
					top_layer[0][0] = True if not (flat_values[i] or flat_values[i-1]) else False
				case 1:
					top_layer[0][1] = not flat_values[i]
				case 2:
					top_layer = Oll.rotate_top(top_layer)
		return top_layer

	def __eq__(self, __value: object) -> bool:
		values_copy = self.values
		for i in self.values:
			if values_copy == __value.values:
				return True
			values_copy = Oll.rotate(values_copy)
		return False

	@property
	def to_str(self) -> str:
		s = ""
		for i in self.values:
			for j in i:
				s += Oll.convert(j, t=SHADE_CHAR, space=False)
			s += " "
		return s

	@staticmethod
	def convert(i:bool, f:str = NO_SHADE_CHAR, t:str = DISPLAY_SHADE_CHAR, space=True) -> str:
		return (t if i else f) + (" " if space else "")

	@staticmethod
	def rotate_top(top_layer: [[bool]]) -> [[bool]]:
		new_top = [[top_layer[x][2-y] for x in range(len(top_layer[y]))] for y in range(len(top_layer))]
		return new_top

	@staticmethod
	def print_multi_array(array) -> None:
		for i in array:
			s = ""
			for j in i:
				s += Oll.convert(j)
			print(s)
	
	@staticmethod
	def rotate(array:list):
		array.insert(0, array.pop())
		return array

def get_oll() -> Oll:
	s = input()
	return str_to_oll(s)

# considering the format of s is "abc def ghi jkl"
def str_to_oll(s:str) -> Oll:
	values = s.split()
	for i in range(len(values)):
		temp = []
		for j in range(3):
			if j < len(values[i]):
				temp.append(True if values[i][j] == SHADE_CHAR else False if values[i][j] == NO_SHADE_CHAR else None)
			elif j >= len(values[i]):
				temp.append(temp[-1])
		values[i] = temp
	o = Oll()
	o.values = values
	return o

OLL_CASES = []
with open("oll.txt", "r") as f:
	cases = f.read()
	OLL_CASES = [str_to_oll(c) for c in cases.splitlines()]

# STATS VARIABLES

# YOUR_STATS:dict = {
# 	"OLL": [
# 	]
# }
PRE_STATS = {
	"PLL": {
		"count": 0,
		"encounters": [],
	},
	"OLL": {
		"count": 0,
		"encounters": [],
	}
}
OLL_STATS = PRE_STATS["OLL"]

class OllStat:
	def __init__(self, s:str) -> None:
		self.reps:int = 1
		self.str:str = s

# READING DATA.JSON
with open("data.json", "r") as f:
	s = f.read()
	if s:
		PRE_STATS = json.loads(s)
		OLL_STATS = PRE_STATS["OLL"]

def stat_save_json():
	with open("data.json", "w") as f:
		# s = json.dumps(YOUR_STATS, indent=2)
		# json.dump(YOUR_STATS, f, indent=2)
		# f.write(s)
		POST_STATS = PRE_STATS
		POST_STATS["OLL"] = OLL_STATS
		json.dump(POST_STATS, f, indent=2)

def add_stat(s:str) -> None:
	OLL_STATS["count"] += 1
	for i in range(len(OLL_STATS["encounters"])):
		case = OLL_STATS["encounters"][i]
		if case["str"] == s:
			OLL_STATS["encounters"][i]["reps"] += 1
			stat_save_json()
			return
	OLL_STATS["encounters"].append(OllStat(s).__dict__)
	stat_save_json()

# MAIN ##############################################################################

def main():
	s:str = ""
	while (True):
		s = input("RUBIKS/OLL> ")
		if s in ["q","Q"]:
			return
		o:Oll = str_to_oll(s)
		for i, case in enumerate(OLL_CASES):
			if o == case:
				add_stat(o.to_str)

def main_argv(args:list):
	s = " ".join(args)
	o:Oll = str_to_oll(s)
	for case in OLL_CASES:
		if o == case:
			add_stat(o.to_str)

if __name__ == "__main__":
	ARGS = sys.argv[1:]
	if len(ARGS) == 0:
		main()
	elif len(ARGS) == 4:
		main_argv(ARGS)

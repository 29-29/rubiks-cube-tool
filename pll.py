from enum import Enum
import json
import sys

COLORS = {
	"GREEN": 1,
	"RED": 2,
	"BLUE": 3,
	"ORANGE": 4
}

COLOR_KEYS = {
	"R": COLORS["RED"],
	"B": COLORS["BLUE"],
	"O": COLORS["ORANGE"],
	"G": COLORS["GREEN"]
}

class Pll:
	def __init__(self) -> None:
		self.values:list(list(int)) = [[j+1 for i in range(3)] for j in range(4)]
		self.name:str = ""

	def __repr__(self) -> str:
		s:str = f"{{{{Name: {self.name}, }}Case: {self.to_str.strip()}}}"
		s:str = "{" + (f"Name: {self.name}, " if self.name else "") + f"Case: {self.to_str.strip()}" + "}"
		return s
	
	@property
	def to_str(self) -> str:
		s = ""
		for i in self.values:
			for j in i:
				s += str(j)
			s += " "
		return s
	
	# FIXME rework equality checking
	def __eq__(self, o:object) -> bool:
		values_copy = self.values
		for j in range(4):
			for i in range(4):
				# print(' '.join([''.join([str(r) for r in c]) for c in values_copy]), o.to_str, sep=' | ')
				if values_copy == o.values:
					return True
				# print('next color')
				values_copy = Pll.next_color(values_copy)
			# print('rotate')
			values_copy = Pll.rotate(values_copy.copy())
		return False

	@staticmethod
	def next_color(values:list) -> list:
		new_values = [[v%4+1 for v in i] for i in values]
		return new_values
	
	@staticmethod
	def rotate(values:list) -> list:
		new_values = values.copy()
		new_values.insert(0, new_values.pop())
		return new_values


def get_pll() -> Pll:
	s:str = input()
	return str_to_pll(s)

def str_to_pll(s:str) -> Pll:
	if len(s.split()) == 5:
		name:str = s.split()[0]
		values:list(list(str)) = s.split()[1:]
	elif len(s.split()) == 4:
		values:list = s.split()
	for i in range(len(values)):
		temp:list(int) = []
		for j in range(len(values[i])):
			if values[i][j].isnumeric():
				color = int(values[i][j])
			else:
				color = COLOR_KEYS[values[i][j].upper()]
			temp.append(color)
		values[i] = temp
	p:Pll() = Pll()
	try:
		p.name = name
	except:
		pass
	p.values = values
	return p

def list_to_pll(l:list) -> Pll:
	assert len(l) == 4 and [len(m) == 3 for m in l]
	p:Pll = Pll()
	p.values = l
	return p

PLL_CASES = []
with open("pll.txt", "r") as f:
	cases = f.read().splitlines()
	PLL_CASES = [str_to_pll(c) for c in cases]

PRE_STATS = {
	"PLL": {
		"count": 0,
		"encounters": [],
	},
	"OLL": {
		"count": 0,
		"encounters": []
	}
}
PLL_STATS = PRE_STATS["PLL"]

with open("data.json", "r") as f:
	s = f.read()
	if s:
		PRE_STATS = json.loads(s)
		PLL_STATS = PRE_STATS["PLL"]

def stat_save_json() -> None:
	with open("data.json", "w") as f:
		POST_STATS = PRE_STATS
		POST_STATS["PLL"] = PLL_STATS
		json.dump(POST_STATS, f, indent=2)

def add_stat(s:str, name:str) -> None:
	PLL_STATS["count"] += 1
	for i in range(len(PLL_STATS["encounters"])):
		case = PLL_STATS["encounters"][i]
		if case["case"] == s:
			PLL_STATS["encounters"][i]["reps"] += 1
			stat_save_json()
			return
	PLL_STATS["encounters"].append(PllStat(s,name).__dict__)
	stat_save_json()

class PllStat:
	def __init__(self, s:str="", name:str="") -> None:
		self.reps:int = 1
		self.case:str = s
		self.name:str = name

# MAIN ###################################################

def main(args=[]):
	if len(args) == 0:
		s:str
		while True:
			s = input("RUBIKS/PLL> ")
			if s.lower() == 'q':
				return
			p:Pll = str_to_pll(s)
			for case in PLL_CASES:
				if p == case:
					print('found match')
					add_stat(case.to_str, case.name)
	elif len(args) == 4:
		s:str = " ".join(args)
		p:Pll = str_to_pll(s)
		for case in PLL_CASES:
			if p == case:
				add_stat(case.to_str, case.name)

if __name__ == "__main__":
	ARGS = sys.argv[1:]
	main(ARGS)

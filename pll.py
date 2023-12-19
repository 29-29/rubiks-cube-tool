from enum import Enum

# TODO Make color enums
# class Colors(Enum):
# 	GREEN = 1
# 	RED = 2
# 	BLUE = 3
# 	ORANGE = 4
COLORS = {
	"GREEN": 1,
	"RED": 2,
	"BLUE": 3,
	"ORANGE": 4
}

color_keys = {
	"R": COLORS["RED"],
	"B": COLORS["BLUE"],
	"O": COLORS["ORANGE"],
	"G": COLORS["GREEN"]
}

# TODO Write PLL class
class Pll:
	def __init__(self) -> None:
		self.values = [[j+1 for i in range(3)] for j in range(4)]


def get_pll() -> Pll:
	s = input()
	return str_to_pll(s)

def str_to_pll(s:str) -> Pll:
	values = s.split()
	for i in range(len(values)):
		temp:list(int) = []
		for j in range(len(values[i])):
			temp.append(color_keys[values[i][j].upper()])
		values[i] = temp
	p:Pll() = Pll()
	p.values = values
	return p

p:Pll = get_pll()
print(p.values)
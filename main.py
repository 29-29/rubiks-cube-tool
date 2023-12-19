import oll
import pll
import stats

arg = ""
while (True):
	arg = input("RUBIKS> ")
	if arg in ["q", "Q"]:
		quit()

	arg = arg.split()
	match arg[0]:
		case "oll":
			if len(arg[1:]) == 0:
				oll.main()
			elif len(arg[1:]) == 4:
				oll.main_argv(arg[1:])
		case 'pll':
			if len(arg[1:]) == 0:
				pll.main()
			elif len(arg[1:]) == 4:
				pll.main(arg[1:])
			# pll.main(arg[1:])
		case "stats":
			if arg[1] == "oll":
				stats.stats_oll()
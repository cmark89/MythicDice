import math
from random import randint

DEBUG = False
levels = {
	"Miniscule 2" : 0,
	"Miniscule" : 1,
	"Weak" : 2,
	"Low" : 3,
	"Below Average" : 4,
	"Average" : 5,
	"Above Average" : 6,
	"High" : 7,
	"Exceptional" : 8,
	"Incredible" : 9,
	"Awesome" : 10,
	"Superhuman" : 11,
	"Superhuman 2" : 12
}

table = []
#Miniscule 2
table.append([50, 25, 10, 5, 5, 0, 0, -20, -20, -50, -40, -55, -65])
#Miniscule
table.append([75, 50, 25, 15, 10, 5, 5, 0, 0, -20, -20, -35, -45])
#Weak
table.append([90, 75, 50, 35, 25, 15, 10, 5, 5, 0, 0, -15, -25])
#Low
table.append([95, 85, 65, 50, 45, 25, 15, 10, 5, 5, 5, -5, -15])
#Below Average
table.append([100, 90, 75, 55, 50, 35, 20, 15, 10, 5, 5, 0, -10])
#Average
table.append([105, 95, 85, 75, 65, 50, 35, 25, 15, 10, 10, 5, -5])
#Above Average
table.append([110, 95, 90, 85, 80, 65, 50, 45, 25, 20, 15, 5, 0])
#High
table.append([115, 100, 95, 90, 85, 75, 55, 50, 35, 25, 20, 10, 5])
#Exceptional
table.append([120, 105, 95, 95, 90, 85, 75, 65, 50, 45, 35, 15, 5])
#Incredible
table.append([125, 115, 100, 95, 95, 90, 80, 75, 55, 50, 45, 20, 10])
#Awesome
table.append([130, 125, 110, 95, 95, 90, 85, 80, 65, 55, 50, 25, 10])
#Superhuman
table.append([150, 145, 130, 100, 100, 95, 95, 90, 85, 80, 75, 50, 25])
#Superhuman 2
table.append([170, 165, 150, 120, 120, 100, 100, 95, 95, 90, 90, 75, 50])


def get_values(acting_rank, difficulty_rank):
	mod = 0
	if acting_rank.startswith("Miniscule ") or \
			acting_rank.startswith("Superhuman "):
		acting_rank, mod = adjust_rank(acting_rank, mod, 1)
	if difficulty_rank.startswith("Miniscule ") or \
			difficulty_rank.startswith("Superhuman "):
		difficulty_rank, mod = adjust_rank(difficulty_rank, mod, -1)
	
	act = levels[acting_rank]
	diff = levels[difficulty_rank]

	# Roll under this number to get a yes
	success_chance = table[act][diff] + mod
	# This is the breadth of the failure condition
	fail_range = 100 - success_chance
	# Return critical yes, yes, and critical no in order
	return math.ceil(success_chance * .2), success_chance, \
			math.ceil(101 - (fail_range * .2))


def roll(acting, difficulty):
	vals = get_values(acting, difficulty)
	exceptional_yes = None
	yes = None
	exceptional_no = None
	if vals[0] > 0:
		exceptional_yes = vals[0]
	if vals[1] > 0:
		yes = vals[1]
	if vals[1] < 100:
		exceptional_no = vals[2]
	roll = randint(1,100)

	if DEBUG:
		if exceptional_yes:
			print("Exceptional Yes: " + str(exceptional_yes) + " or lower")
		if yes:
			print("Yes: " + str(yes) + " or lower")
		if exceptional_no:
			print("Exceptional No: " + str(exceptional_no) + " or above")

	result = None
	if exceptional_yes and roll <= exceptional_yes: 
		result = "Exceptional Yes"
	elif yes and roll <= yes: 
		result = "Yes"
	elif exceptional_no and roll >= exceptional_no: 
		result = "Exceptional No"
	else:
		result = "No"

	return result, roll
		


def adjust_rank(rank, mod, is_acting):
	# is_acting is 1 if acting, -1 if difficulty;
	# this is used to flip the mod as it's applied
	vals = rank.split(" ")	
	if int(vals[1]) <= 2:
		pass
	else :
		if vals[0] == "Miniscule":
			rank = "Miniscule 2"
			mod += (-20 * is_acting) * (int(vals[1]) - 2)
		elif vals[0] == "Superhuman":
			rank = "Superhuman 2"
			mod += (20 * is_acting) * (int(vals[1]) - 2)
	return rank, mod
		
# Used for the dropdown list required by GUI frontends
ranklist = []
for i in range(0,9):
	ranklist.append("Miniscule %s" % str(10-i))
ranklist.extend(["Miniscule", "Weak", "Low", "Below Average", \
			"Average", "Above Average", "High", "Exceptional", \
			"Incredible", "Awesome", "Superhuman"])
for i in range(2, 11):
	ranklist.append("Superhuman %s" % i)

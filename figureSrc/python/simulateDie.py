import random

def main():
	random.seed(0)
	data = []
	for i in range(10000):
		sum_dice = simulate_dice()
		data.append(sum_dice)
	for i in range(13):
		print(i, data.count(i))

def simulate_dice():
	d1 = sim_die()
	d2 = sim_die()
	return d1 + d2

def sim_die():
	return random.randint(1, 6)


if __name__ == '__main__':
	main()
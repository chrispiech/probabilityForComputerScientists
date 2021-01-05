import pydealer
import numpy as np
from tqdm import tqdm

MAX_POINTS = 37 #4 aces, 4 kings, 4 queens, 1 jack
N_RUNS = 1000000

def main():
	cond_count = np.zeros((37, 37),dtype=int)
	for i in tqdm(range(N_RUNS)):
		simulate_one(cond_count)
	print(cond_count)
	np.savetxt('bridgeCond.csv', cond_count)
	
def simulate_one(cond_count):
	deck = pydealer.Deck()
	deck.shuffle()
	hands = []
	hand_points = []
	# deal the four hands
	for i in range(4):
		hands.append(deck.deal(13))
	for yours_i in range(4):
		for other_i in range(4):
			if yours_i == other_i: continue
			your_points = calc_points(hands[yours_i])
			other_points = calc_points(hands[other_i])
			cond_count[your_points][other_points] += 1


def calc_points(hand):
	points = 0
	for card in hand:
		value = card.value
		if value == 'Ace': points += 4
		if value == 'King': points += 3
		if value == 'Queen': points += 2
		if value == 'Jack': points += 1
	return points

def print_normalized(hist):
	for i in range(len(hist[0])):
		print(hist[1][i], hist[0][i])

if __name__ == '__main__':
	main()
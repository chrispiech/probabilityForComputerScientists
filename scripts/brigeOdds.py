import pydealer
import numpy as np
from tqdm import tqdm

MAX_POINTS = 37 #4 aces, 4 kings, 4 queens, 1 jack
N_RUNS = 1000000

def main():
	points = []
	for i in tqdm(range(N_RUNS)):
		points.extend(simulate_one())
	hist = np.histogram(points, bins=range(MAX_POINTS))
	print_normalized(hist)
	
def simulate_one():
	deck = pydealer.Deck()
	deck.shuffle()
	hands = []
	hand_points = []
	for i in range(4):
		hands.append(deck.deal(13))
	for hand in hands:
		hand_points.append(calc_points(hand))
	return hand_points


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
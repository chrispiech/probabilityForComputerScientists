import itertools

COINS = list('H' * 4 + 'T' * 6)
def main():
	seen = set([])
	permutations = list(itertools.permutations(COINS))
	for p in permutations:
		if p in seen: continue
		seen.add(p)
		print(p)

if __name__ == '__main__':
	main()
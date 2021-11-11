import json

def main():
	data = json.load(open('count_map.json'))
	for name, counts in data.items():
		total = get_total(counts)
		if total > 10000:
			max_prob = get_max_prob(counts, total)
			if max_prob > 0.4:
				print(name, max_prob)

def get_max_prob(counts, n):
	max_val = None
	for year, count in counts.items():
		pr = (count + get_neighbors(year, counts))/n
		if max_val == None or pr > max_val:
			max_val = pr
	return max_val

def get_neighbors(year, counts):
	low_key = str(int(year)-1)
	high_key = str(int(year)+1)
	n = 0
	if low_key in counts:
		n += counts[low_key]
	if high_key in counts:
		n += counts[high_key]
	return n

def get_total(counts):
	n = 0
	for year, count in counts.items():
		n += count
	return n

if __name__ == '__main__':
	main()
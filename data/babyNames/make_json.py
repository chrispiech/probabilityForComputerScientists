import pickle
import json

def main():
	names = pickle.load(open('count_map.pkl', 'rb'))
	json_map = {}
	for key, count in names.items():
		name = key[0].lower()
		year = key[1]
		if name not in json_map:
			json_map[name] = {}
		json_map[name][year] = count
		print(year, count)
	json.dump(json_map, open('count_map.json', 'w'))

if __name__ == '__main__':
	main()
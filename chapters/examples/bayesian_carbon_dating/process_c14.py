import csv
import json
def main():
    reader = csv.reader(open('incalc14.csv'))
    writer = csv.writer(open('historical_c14.csv', 'w'))
    next(reader)
    sorted_data = []
    for row in reader:
        year = float(row[0])
        d_c14 = float(row[1])
        sorted_data.append([year, d_c14])

    out_data = {}
    writer.writerow(['bp','year','delta c14'])
    for year in range(1922,-7979, -1):
    # for year in range(-655,-656, -1):
        bp = 2022-year
        c14 = get_c14_guess(sorted_data, year)
        print(bp, year, c14)
        writer.writerow([bp, year, c14])
        out_data[bp] = {
            'year':year,
            'deltaC14':c14
        }
    json.dump(out_data, open('historical_c14.json', 'w'))
        

def get_c14_guess(sorted_data, year):
    curr_index=0
    while True:
        curr_row = sorted_data[curr_index]
        curr_year = curr_row[0]
        if curr_year <= year:
            break
        curr_index += 1
    prev_row = sorted_data[curr_index-1]
    c14 = interpolate(prev_row, curr_row, year)
    return c14

def interpolate(row_b, row_a, year):

    delta_years = row_b[0] - row_a[0]
    rise = row_b[1] - row_a[1]

    point_delta = year - row_a[0]
    point_pct = point_delta / delta_years
    
    c14 = row_a[1] + rise * point_pct

    return c14


if __name__ == '__main__':
    main()
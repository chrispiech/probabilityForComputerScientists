def main():
	html = '<table>'
	for row in range(1, 7):
		row_html = '<tr>'
		for col in range(1, 7):
			col_html = '<td style="width:50px">({},{})</td>'.format(row, col)
			row_html += col_html
		row_html += '</tr>'
		html += row_html
	html += '</table>'
	print(html)

if __name__ == '__main__':
	main()
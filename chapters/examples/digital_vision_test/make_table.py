import csv

def main():

    reader =csv.reader(open('prior.csv'))

    rows_html = ''
    for row in reader:
        rows_html += make_html(row)
    table_html = f'<table>\n{rows_html}</table>'
    
    out_file = open('priorTable.html', 'w')
    out_file.write(table_html)

def make_html(row):
    col_html= ''

    for value in row:
        col_html += f'    <td>{value}</td>\n'

    return f'  <tr>\n{col_html}  </tr>\n'

if __name__ =='__main__':
    main()
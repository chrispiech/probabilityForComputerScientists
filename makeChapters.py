from bs4 import BeautifulSoup
import os
import pathlib


INDEX_TEMPLATE = '''
% rebase('templates/chapter.html', title="{title}")
 
<center><h1>{title}</h1></center>
<hr/>
'''

EXAMPLE_TEMPLATE = '''
<li>
    <a href="#{uid}" data-toggle="collapse" aria-expanded="true" class="dropdown-toggle show">Worked Examples</a>
    <ul class="collapse list-unstyled show" id="{uid}">
        {example_html}
    </ul>
</li>
'''

def main():
	create_directories_and_files()
	create_sidebar()

def create_sidebar():
	html = ''
	for part_key in book_outline:
		part_html = create_part_html(part_key,)
		html += part_html
	writer = open('templates/chapterList.html', 'w')
	writer.write(html)
	

def create_part_html(part_key):
	part = book_outline[part_key]
	html = '<!-- {} -->\n'.format(part_key)
	html += '<ul class="list-unstyled components">\n'
	if part['title']:
		title = part['title']
		html += '<li><p href="{{pathToLang}}{}">{}</p></li>\n'.format(part_key, title)
	html += '<li>\n'
	for section_key in part['sections']:
		section_path = '{{pathToLang}}' + part_key + '/' + section_key
		section_title = part['sections'][section_key]
		sidebar_id = 'sidebar-' + section_key
		html += '<a id={} href="{}">{}</a>\n'.format(sidebar_id, section_path, section_title)
	
	if 'examples' in part:
		example_html = ''
		for example_key in part['examples']:
			example_path = '{{pathToLang}}examples' + '/' + example_key
			example_title = part['examples'][example_key]
			sidebar_id = 'sidebar-' + example_key
			example_html += '<li><a href="{}">{}</a></li>'.format(example_path, example_title)
		
		example_data = {
			'uid':part_key+'_examples',
			'example_html':example_html
		}
		html += EXAMPLE_TEMPLATE.format(**example_data)
	html += '</li>\n'
	html += '</ul>\n\n'
	return html

def create_directories_and_files():
	safe_mkdir('chapters')
	for part_key in book_outline:
		part = book_outline[part_key]
		part_path = 'chapters/'+part_key
		safe_mkdir(part_path)
		for section_key in part['sections']:
			title = part['sections'][section_key]
			section_path = part_path + '/' + section_key

			safe_mkdir(section_path)
			make_index(section_path, title)
		if 'examples' in part:
			for example_key in part['examples']:
				title = part['examples'][example_key]
				example_path =  'chapters/examples/' + example_key

				safe_mkdir(example_path)
				make_index(example_path, title)

def make_index(path, title):
	index_data = {
		'title':title
	}
	index_path = path + '/index.html'
	index_html = INDEX_TEMPLATE.format(**index_data)
	safe_make_file(index_path, index_html)

def safe_make_file(path, content):
	if not os.path.isfile(path):
		print('creating ' + path)
		writer = open(path, 'w')
		writer.write(content)

def safe_mkdir(path):
	pathlib.Path(path).mkdir(exist_ok=True)
# def extract_chapters():
# 	html = open('templates/parts/sideBar.html').read()
# 	soup = BeautifulSoup(html, 'html.parser')
# 	parts = soup.find_all('ul')
# 	for part in parts:
# 		title = part.find('p')
# 		if title:
# 			print(title.text)
# 	# raw_lines = html_text.split('\n')
# 	# lines = []
# 	# for line in raw_lines:
# 	# 	line = line.strip()
# 	# 	if line != '':
# 	# 		lines.append(line)
# 	# return lines

if __name__ == '__main__':
	main()
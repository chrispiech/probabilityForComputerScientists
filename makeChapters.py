from bs4 import BeautifulSoup
import os
import pathlib

book_outline = {
	'intro': {
		'title':None,
		'sections': {
			'intro':'Introduction',
			'free_book':'A Free Online Textbook',
			'notation': 'Notation',
			'python': 'Probability in Python'
		}
	},
	'part1': {
		'title':'Part 1: Core Probability',
		'sections': {
			'counting':'Counting',
			'combinatorics':'Combinatorics',
			'probability':'Definition of Probability',
			'equally_likely':'Equally Likely Outcomes',
			'prob_or':'Probability of or',
			'prob_and':'Probability of and',
			'cond_prob':'Conditional Probability',
			'law_total':'Law of Total Probability',
			'bayes_theorem':"Bayes' Theorem",
			'random_computers':'Randomness in Computers',
			'log_probabilities':'Log Probabilities'
		}
	},
	'part2':{
		'title':'Part 2: Random Variables',
		'sections': {
			'rvs':'Random Variables',
			'pmf':'Likelihood Functions',
			'expectation':'Expectation',
			'variance':'Variance',
			'binomial':'Bernoulli and Binomial',
			'poisson':'Poisson Distribution',
			'continuous':'Continuous Distribution',
			'normal':'Normal Distribution',
			'convolution':'Convolution',
			'all_distributions':'Random Variable Reference'
		}
	},
	'part3':{
		'title':'Part 3: Probabilistic Models',
		'sections': {
			'joint':'Joint Probability',
			'independent_vars':'Independence in Variables',
			'cond_distributions':'Conditional Distributions',
			'variable_bayes':'Bayes Theorem Revisited',
			'continuous_joint':'Continuous Joint',
			'multivariate_gaussian':'Multivariate Gaussian',
			'bayesian_networks':'Bayesian Networks',
			'computational_inference':'Computational Inference',
		}
	},
	'part4':{
		'title':'Part 4: Uncertainty Theory',
		'sections': {
			'clt':'Central Limit Theorem',
			'bootstrapping':'Bootstrapping',
			'parameters':'Uncertainty in Parameters',
			'beta':'Beta Distribution',
			'bounds':'Probability Bounds'
		}
	},
	'part5':{
		'title':'Part 5: Machine Learning',
		'sections': {
			'mle':'Maximum Likelihood Estimation',
			'map':'Maximum A Posteriori',
			'naive_bayes':'Naïve Bayes',
			'optimization':'Gradient Ascent Optimization',
			'linear_regression':'Linear Regression',
			'log_regression':'Logistic Regression',
			'neural_nets':'Artificial Neural Networks'
		}
	}
}

INDEX_TEMPLATE = '''
% rebase('templates/chapter.html', title="{title}")
 
<center><h1>{title}</h1></center>
<hr/>
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
		html += '<a href="{}">{}</a>\n'.format(section_path, section_title)
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
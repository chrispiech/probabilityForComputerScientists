#!/usr/bin/env python

# make sure to run 
# > python -m pip install bottle
# I used version bottle-0.12.19
from bottle import SimpleTemplate
from bs4 import BeautifulSoup
import json
import hjson

import os.path
import sys

IGNORE_DIRS = [
]
TEMPLATE_DIR = 'chapters'
ROOT = 'pythonreader'
OUT_DIR = 'en'

# Use the -t flag if you want to compile for local tests
DEPLOY = False

class IndexBuilder(object):

    # Function: Run
    # -------------
    # This function compiles all the html files (recursively)
    # from the templates dir into the current folder. Folder
    # hierarchy is preserved
    def run(self):
        self.index = []
        book_data = hjson.load(open('bookOutline.hjson'))
        for part_key, part in book_data.items():
            for section_key, title in part['sections'].items():
                path = '{}/{}'.format(part_key, section_key)
                self.addSectionToIndex(path, section_key, title)
            if not 'examples' in part: continue
            for section_key, title in part['examples'].items():
                path = '{}/{}'.format('examples', section_key)
                self.addSectionToIndex(path, section_key, title)
        json.dump(self.index,open('searchIndex.json', 'w'))

    #####################
    # Private Helpers
    #####################

    def addSectionToIndex(self, rel_path, key, title):
        sectionDirPath = os.path.join(TEMPLATE_DIR, rel_path)
        for fileName in os.listdir(sectionDirPath):
            if fileName.endswith('.html'):
                filePath = os.path.join(sectionDirPath, fileName)
                self.addFileToIndex(filePath, rel_path, key, title)

    def addFileToIndex(self, filePath, url, key, title):
        print(filePath)
        templateText = open(filePath).read()
        # compiledHtml = SimpleTemplate(templateText).render(pathToRoot = '../' + pathToLangRoot, pathToLang = pathToLangRoot)
        soup = BeautifulSoup(templateText, 'html.parser')
        newItem = {
            'id':key,
            'title':title,
            'url':url,
            'text':self.sanitizeText(soup.get_text())
        }
        self.index.append(newItem)
        

    def sanitizeText(self, text):
        sText = ''
        for line in text.split('\n'):
            stripped = line.strip()
            if stripped.startswith('%'):
                continue
            sText += line + '\n'
        return sText


if __name__ == '__main__':
    IndexBuilder().run()

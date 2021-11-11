#!/usr/bin/env python

# make sure to run 
# > python -m pip install bottle
# I used version bottle-0.12.19
from bottle import SimpleTemplate
from makeChapters import make_chapters
import os.path
import sys

IGNORE_DIRS = [
]
TEMPLATE_DIR = 'chapters'
ROOT = 'pythonreader'
OUT_DIR = 'en'

# Use the -t flag if you want to compile for local tests
DEPLOY = False

class Compiler(object):

    # Function: Run
    # -------------
    # This function compiles all the html files (recursively)
    # from the templates dir into the current folder. Folder
    # hierarchy is preserved
    def run(self):
        make_chapters()
        templateFilePaths = self.getTemplateFilePaths('')
        for templateFilePath in templateFilePaths:
            self.compileTemplate(templateFilePath)

    #####################
    # Private Helpers
    #####################

    def compileTemplate(self, relativePath):
        print(relativePath)
        pathToLangRoot = self.getPathToRoot(relativePath)
        filePath = os.path.join(TEMPLATE_DIR, relativePath)
        templateText = open(filePath).read()
        params = {
            'pathToRoot': '../' + pathToLangRoot, 
            'pathToLang' : pathToLangRoot,
            'beta':'<a href="">BETA</a>'
        }
        compiledHtml = SimpleTemplate(templateText).render(params)
        
        fileName, fileExtension = os.path.splitext(relativePath)
        compiledHtml = compiledHtml.encode('utf8')
        path = OUT_DIR + '/' + relativePath
        self.makePath(path)
        open(path, 'wb').write(compiledHtml)

    def makePath(self, path):
        dirPath = os.path.dirname(path)
        if dirPath == '': return
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        
    def getPathToRoot(self, relativePath):
        if DEPLOY:
            return ROOT
        return self.getRelPathToRoot(relativePath)

    def getRelPathToRoot(self, relativePath):
        dirs = self.splitDirs(relativePath)
        depth = len(dirs) - 1
        pathToRoot = ''
        for i in range(depth, 0, -1):
            curr = dirs[i]
            pathToRoot += '../'
        return pathToRoot

    def splitDirs(self, filePath):
        if filePath == '': return []
        rootPath, last = os.path.split(filePath)
        rootDirs = self.splitDirs(rootPath)
        rootDirs.append(last)
        return rootDirs

    def isTemplateFile(self, fileName):
        extension = os.path.splitext(fileName)[1]
        return extension == '.html'

    def getTemplateFilePaths(self, root):
        if root in IGNORE_DIRS: return []
        paths = []
        templateDirPath = os.path.join(TEMPLATE_DIR, root)
        for fileName in os.listdir(templateDirPath):
            filePath = os.path.join(root, fileName)
            templateFilePath = os.path.join(TEMPLATE_DIR, filePath)
            if os.path.isdir(templateFilePath):
                childPaths = self.getTemplateFilePaths(filePath)
                for childPath in childPaths:
                    paths.append(childPath)
            elif self.isTemplateFile(fileName):
                paths.append(filePath)
        return paths


if __name__ == '__main__':
    Compiler().run()

# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 00:22:32 2020

@author: Michael Gribov
"""

import os
try:
  import simplejson as json
except ImportError:
  import json


DIRECTORY = 'directory'
FILE = 'file'
_type = '_type'
_ext = '_ext'
_fn = '_fn'
_info = '_info'



class FiledJson:
    
    def _scan(self, dir):
        for dirpath, dirnames, filenames in os.walk(dir):    
            dirpath = dirpath[len(dir):].lstrip('\\').split('\\');        
            current = self.setCurrent(dirpath)
        
            for dirname in dirnames:            
                #current[dirname] = {_type: DIRECTORY}
                self._addDir(dirname)
            for filename in filenames:
                #current[filename] = {_type: FILE}
                self._addFile(filename)
            
    def _fullFileName(self, name):
        return self.dir.lstrip('\\') + (os.sep if self.dir > '' else '') + name

    def _addFile(self, filename):
        
        fn = self._fullFileName(filename)
        
        p = filename.rfind('.')
        if (p > -1):
            ext = filename[p + 1:]
            name = filename[:p]
        
        if (name == _info):
            return
                
        node = self.getJsonFile(fn)
        
        
        if (name in self.current):
            node = node.update(self.current[name])

        node.update({
            _type: FILE,
            _ext: ext,
            _fn: fn,
            'name': name    
        })
        
        
        self.current[name] = node
    
    def _addDir(self, dirname):
        
        fn = self._fullFileName(dirname)
        name = dirname
        
        node = self.getJsonFile(fn + os.sep + _info +'.json')
        
        if (name in self.current):
            node = node.update(self.current[name])
        
                
        
        
        node.update({
            _type: DIRECTORY,            
            _fn: fn,
            'name': name    
        })
        
        
        self.current[name] = node
        
    def getJsonFile(self, fn):
        result = {}
        fn = self.base + os.sep + fn
        
        if(os.path.isfile(fn)):            
            try:    
                with open(fn, 'r', encoding='utf-8') as file: 
                    result = json.load(file)                     
            except json.JSONDecodeError as ex:
                result = {'error': ex}
        return result
        
        
    def __init__(self, dir):
        self.base = dir
        self.dir = ''
        self.structure = {}
        self.current = self.structure
        self._scan(self.base)


    

    def setCurrent(self, path):        
        if (len(path) and path[0] != ''):
            path.insert(0, '')
            
        
        self.current = self.structure        
        p = []        
        for name in path:
            p.append(name)
            if not name in self.current:
                self._addDir(name)      
                
            self.dir = os.sep.join(p)    
            self.current = self.current[name]
        
        
        return self.current


    def __str__(self):
        return self.dump()
        
    def dump(self, node = False, short = True, indent = ''):
        result = ''
        if (node == False):
            node = self.structure
        
        for name in node:
            if (not short or name[:1] != '_' and name != 'name'):
                value = node[name]
                if (not short or value):
                    if ( not (isinstance(value, dict) or isinstance(value, list))):                    
                        result += "{}{}: {}\n".format(indent, name,value)
                        #print('{}{}: {}'.format(indent, name,value))
                
        for name in node:
            value = node[name]            
            if (isinstance(value, dict) or isinstance(value, list)):
                
                #print("\033[32m{}{}:\033[0m" .format(indent, name))
                result +="{}{}:\n" .format(indent, name)
                #print("{}{}:" .format(indent, name))
                result += self.dump(value, short, indent + ". ")
                #print(indent)
        return result    
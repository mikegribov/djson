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
_size = '_size'
_ctime = '_ctime'
_type = '_type'
_ext = '_ext'
_fn = '_fn'
_info = '_info'



class FiledJson:
    
    def _scan(self, dir):
        filename = dir + '.json'
        if (os.path.isfile(filename) and os.path.exists(filename)):            
            self._addFile(filename, True)
            print(self.structure)
        else:
    
            for dirpath, dirnames, filenames in os.walk(dir):    
                dirpath = dirpath[len(dir):].lstrip('\\').split('\\');        
                current = self.setCurrent(dirpath)
            
                for dirname in dirnames:                                
                    self._addDir(dirname)
                for filename in filenames:                    
                    self._addFile(filename)
                            
            self.structure [self.name] = self.structure.pop('')           
            
    def _fullFileName(self, name):        
        return os.path.join(self.base, self.dir.lstrip('\\'), name)

    def _addFile(self, filename, fullName = False):
        
        if fullName:
            fn = filename 
            filename = os.path.split(filename)[1]
        else:
            fn = self._fullFileName(filename) 
        
        
        (name, ext) = os.path.splitext(filename)
        
        if (name == _info):
            return
                
        node = self.getJsonFile(fn)
        
        
        if (name in self.current):
            node = node.update(self.current[name])

        node.update({
            _ctime: os.path.getctime(fn),
            _size: os.path.getsize(fn),
            _type: FILE,
            _ext: ext[1:],
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
        
        #if (os.path.exists(fn)):
        #    node[_ctime] = os.path.getctime(fn)
        
        
        node.update({
            _ctime: os.path.getctime(fn),
            _type: DIRECTORY,            
            _fn: fn,
            'name': name    
        })
        
            
        self.current[name] = node
        
    def getJsonFile(self, fn):
        result = {}
        
        if(os.path.isfile(fn)):            
            try:    
                with open(fn, 'r', encoding='utf-8') as file: 
                    result = json.load(file)                     
            except json.JSONDecodeError as ex:
                result = {'error': ex}
        return result
        
        
    def __init__(self, name):
        self.base = name                    # base directory name
        self.name = os.path.split(name)[1]  # name of root node
        self.dir = ''                       # current directory related base directory
        self.structure = {}                 # result structure
        self.current = self.structure       # current structure node
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
                
        for name in node:
            value = node[name]            
            if (isinstance(value, dict) or isinstance(value, list)):
                
                #print("\033[32m{}{}:\033[0m" .format(indent, name))
                result +="{}{}:\n" .format(indent, name)                
                result += self.dump(value, short, indent + ". ")                
        return result    
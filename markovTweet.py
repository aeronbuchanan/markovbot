#!/usr/bin/python3

import sys
import random
import time

class Sentence:
    def __init__(self):
        #print 'New sentence!'
        self.terminals = ['.', '!', '?']
        self.words = []
        self.terminated = False
        
    #@staticmethod:
    #def terminals:
    #    return (c in ['.', '!', '?'])
        
    def isTerminated(self):
        return self.terminated
    
    def add(self, _string):
        if self.terminated:
            return _string
        if any( (c in _string for c in self.terminals) ):
            self.terminated = True
            i = _string.__len__()
            for c in self.terminals:
                if c in _string:
                    i = min(i, _string.find(c))
            self.addd(_string[:i+1])
            #print('Sentence is "' + ' '.join(self.words) + '"')
            #print('Rest is "' + _string[i+1:] + '"')
            return _string[i+1:]
        else:
            self.addd(_string)
            return ''
            
    def addd(self, _string):
        self.words.extend(_string.split())
        #print('After addition -> ' + str(self.words))

class MarkovLookup:
    class Node:
        def __init__(self, _level, _max):
            self.level = _level
            self.maxDepth = _max
            self.weight = self.level ** 2
            self.values = {}
            self.children = {}
            
        def isLeaf(self):
            return self.level == self.maxDepth
            
        def add(self, _keys, _value):
            if not self.isLeaf() and _keys.__len__() > 0:
                #print('"' + _value + '" with ' + str(_keys) + '=> adding \'' + str(_keys[-1]) + '\' to ' + str(self.children.keys()))
                lastKey = _keys[-1]
                if lastKey not in self.children.keys():
                    self.children[lastKey] = MarkovLookup.Node(self.level + 1, self.maxDepth)
                self.children[lastKey].add(_keys[:-1], _value)
            #else:
            if _value not in self.values.keys():
                self.values[_value] = 0
            self.values[_value] += self.weight
            #print('Set node value: ' + _value)
                
        def addSentence(self, _sentence):
            for i in range(1, _sentence.words.__len__()):
                self.add(_sentence.words[:i], _sentence.words[i])
                
        def lookup(self, _words):
            suggestions = {}
            if not self.isLeaf() and _words.__len__() > 0 and _words[0] in self.children.keys():
                suggestions = self.children[_words[0]].lookup(_words[1:]).copy()
            else:
                if self.level > 0:
                    for (k, v) in self.values.items():
                        if k in suggestions.keys():
                            suggestions[k] += v
                        else:
                            suggestions[k] = v
            return suggestions
                
        def display(self, _pre):
            print(_pre + 'Values: ' + str(self.values))
            print(_pre + 'Keys: ' + str(self.children.keys()))
            for k in self.children.keys():
                print(_pre + k + ':')
                self.children[k].display(_pre + '  ')
            

    def __init__(self, _depth = 6):
        self.tree = MarkovLookup.Node(0, _depth)
        self.currentSentence = Sentence()
        self.firstWords = []

    def add(self, _string):
        s = _string.lower();
        while s.__len__() > 0:
            s = self.currentSentence.add(s)
            if self.currentSentence.isTerminated():
                self.firstWords.append(self.currentSentence.words[0])
                self.tree.addSentence(self.currentSentence)
                self.currentSentence = Sentence()
                
    def lookup(self, _words):
        #print("Lookup " + str(_words))
        ws = list(_words)
        ws.reverse()
        ss = self.tree.lookup(ws)
        #print("Suggestions: " + str(ss))
        t = 0
        for v in ss.values():
            t += v
        s = '#'
        if t > 0:
            r = int(random.random() * t)
            t = 0
            for i in ss.items():
                t += i[1]
                if t > r:
                    s = i[0]
                    break
        #print("Chosen: " + s)
        return s
                     
    def display(self):
        print('Root: ')
        self.tree.display('')

if sys.argv.__len__() < 2:
    print(sys.argv[0] + ": please provide at least one text source file")
    exit()

ml = MarkovLookup(2)

# load files
for f in sys.argv[1:]:
    with open(f, "r") as h:
        for line in h:
            ml.add(line)

# display tree
#ml.display()

# generate sentences
while 1:
    # get first word
    ks = list(ml.firstWords)
    ws = [ks[int(random.random()*ks.__len__())]]
    w = ''
    while w != '#':
        w = ml.lookup(ws)
        ws.append(w)
    print(' '.join(ws).capitalize())
    print()
    time.sleep(5)
        

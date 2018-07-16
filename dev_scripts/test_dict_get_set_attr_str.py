#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 14:13:07 2018

@author: jonasg
"""

class MyDict(dict):
    
    def __init__(self, *args, **kwargs):
        super(MyDict, self).__init__(*args, **kwargs)
    
    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, val):
        self[key] = val
        
    def __str__(self):
        s = ''
        for k, v in self.items():
            s += '{}: {}'.format(k, v)
        return s
        
d = MyDict(bla=1, blub=2)
print(d)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 11:29:14 2018

@author: jonasg
"""
class FH(object):
    def __init__(self):
        self.log = None
        
    def open_log(self):
        self.log = open('out/log_class_test.csv', 'w+')
    
    def add_to_log(self, text):
        self.log.write(text + '\n')
    
    def close_log(self):
        if self.log:
            self.log.close()
            self.log = None
            
if __name__ == '__main__':
    
    fh = FH()
    
    fh.open_log()
    
    fh.add_to_log('bla')
    fh.add_to_log('blub')
    fh.add_to_log('42')
    
    fh.close_log()
    
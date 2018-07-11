#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 14:01:48 2018

@author: jonasg
"""
import abc

class Base(abc.ABC):
    def __init__(self, bla=42):
        self.bla = bla
        
class Derived(Base):
    def __init__(self, blub="40too", **kwargs):
        super(Derived, self).__init__(**kwargs)
        self.blub = blub
        
c = Derived(bla=420)
print(c.bla)
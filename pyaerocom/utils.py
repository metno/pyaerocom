#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Small helper utility functions for pyaerocom
"""   
class BrowseDict(dict):
    """Dictionary with get / set attribute methods
    
    Example
    -------
    >>> d = BrowseDict(bla = 3, blub = 4)
    >>> print(d.bla)
    3
    """
    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, val):
        self[key] = val
        
def list_to_shortstr(lst, indent=3):
    """Custom function to convert a list into a short string representation"""
    if len(lst) == 0:
        return "\n" + indent*" " + "[]\n"
    
    s = "\n" + indent*" " + "[%s\n" %lst[0]
    if len(lst) > 4:
        s += (indent+1)*" " + "%s\n" %lst[1]
        s += (indent+1)*" " + "...\n"
        s += (indent+1)*" " + "%s\n" %lst[-2]
    else: 
        for item in lst[1:-1]:
            s += (indent+1)*" " + "%s" %item
    s += (indent+1)*" " + "%s]\n" %lst[-1]
    return s
        
def dict_to_str(dictionary, s="", indent=3):
    """Custom function to convert dictionary into string (e.g. for print)
    
    Parameters
    ----------
    dictionary : dict
        the dictionary
    s : str
        the input string
    indent : int
        indent of dictionary content
    
    Returns
    -------
    str
        the modified input string
        
    Example
    -------
    
    >>> string = "Printing dictionary d"
    >>> d = dict(Bla=1, Blub=dict(BlaBlub=2))
    >>> print(dict_to_str(d, string))
    Printing dictionary d
       Bla: 1
       Blub (dict)
        BlaBlub: 2
    
    """
    for k, v in dictionary.items():
        if isinstance(v, dict):
            s += "\n" + indent*" " + "%s (dict)" %k
            s = dict_to_str(v, s, indent+1)
        else:
            s += "\n" + indent*" " + "%s: %s" %(k,v)
    return s

def str_underline(s):
    """Create underlined string"""
    return "{}\n{}\n".format(s, len(s)*"-")


#!/usr/bin/env python
"""
seevars
"""
import re
# def my_vars(local):
#     varss = [vars for vars in local if not vars.startswith('__')]
#     return varss


def shows(local):
    """
    local recibe vars()
    """
    for v in local:
        if not v.startswith('__'):
            # get type
            the_type = re.findall(r"\'([\w]+)\'", str(type(local[v])))[0]
            
            # show vars
            print('\033[1m' + v + '\033[0m' + ' '+ the_type)
            
def value(local):
    for v in local:
        if not v.startswith('__'):
            # get type
            the_type = re.findall(r"\'([\w]+)\'", str(type(local[v])))[0]
            
            # show vars
            print('\033[1m' + v + '\033[0m' + ' '+ the_type + ': ' + str(local[v]))
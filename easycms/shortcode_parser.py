import re
from hashlib import sha1
import op_associazione.easycms.parsers
from django.core.cache import cache

def import_parser(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

from os import sys

def parse(value):
    ex = re.compile(r'\[(.*?)\]')
    groups = ex.findall(value)
    pieces = {}
    parsed = value

    for item in groups:
        if ' ' in item:
            name, space, args = item.partition(' ')
            args = __parse_args__(args)
        else:
            name = item
            args = {}
        # print >>sys.stderr, 'search:'+ item 
        try:
            item_hash = sha1(item).hexdigest()
            if False and cache.get(item_hash):
                parsed = re.sub(r'\[' + item + r'\]', cache.get(item_hash), parsed)
            else:
                module = import_parser('op_associazione.easycms.parsers.' + name)
                function = getattr(module, 'parse')
                result = function(args)
                cache.set(item_hash, result, 3600)
                parsed = re.sub(r'\[' + item + r'\]', result, parsed)
        except ImportError:
            pass
    return parsed

def __parse_args__(value):
        ex = re.compile(r'[ ]*(\w+)=([^" ]+|"[^"]*")[ ]*(?: |$)')
        groups = ex.findall(value)
        kwargs = {}
        
        for group in groups:
                if group.__len__() == 2:
                        item_key = group[0]
                        item_value = group[1]
                        
                        if item_value.startswith('"'):
                                if item_value.endswith('"'):
                                        item_value = item_value[1:]
                                        item_value = item_value[:item_value.__len__() - 1]
                        
                        kwargs[item_key] = item_value
                        
        return kwargs
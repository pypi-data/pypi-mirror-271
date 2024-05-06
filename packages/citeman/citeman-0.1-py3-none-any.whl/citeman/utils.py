import re

def removeBraces(string):
    return re.sub(r'^\{?(.*?)\}?$', r'\1', string)
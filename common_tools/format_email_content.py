import json

def format_json(j):
    return(json.dumps(j, indent=4))

def format_contents(c):
    return '\n========================\n'.join(map(format_json, c))
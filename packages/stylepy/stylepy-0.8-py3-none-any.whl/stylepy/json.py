import pprint

def pretty_json(input, returnValue = False):
    pprint.pprint(input, width=50, indent=2)
import pprint

def timeComplexity(value, desc, returnValue = False):
    result = f'\n 🕒 Time Complexity: Approximately {value}'

    if (desc):
        result += f'\n    Description: {desc}'
        
    if (returnValue):
        return result

    print(result)
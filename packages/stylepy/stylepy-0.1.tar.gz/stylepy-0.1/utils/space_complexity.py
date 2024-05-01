def spaceComplexity(value, desc, returnValue = False):
    result = f' 💾 Space Complexity: Approximately {value}'

    if (desc):
        result += f'\n    Description: {desc}'
        
    if (returnValue):
        return result

    print(result)
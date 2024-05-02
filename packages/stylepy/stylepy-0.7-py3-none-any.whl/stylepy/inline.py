def span(*text, returnValue = False):
    combined_text = " ".join(str(t) for t in text)  # Join all elements of text into one string
    result = f"\033[1m{combined_text}\033[0m"

    if (returnValue):
        return result
    
    # Using ANSI escape code for bold text
    print(result)
    
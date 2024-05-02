def h1(text, returnValue = False):
    result = f"\n{'=' * 40}\n{text}\n{'=' * 40}"

    if (returnValue):
        return result

    print(result)

def h2(text, returnValue = False):
    result = f"\n{'-' * 35}\n{text}\n{'-' * 35}"

    if (returnValue):
        return result

    print(result)


def h3(text, returnValue = False):
    result = f"\n{text}\n{'-' * 30}"

    if (returnValue):
        return result

    print(result)


def h4(*text, returnValue = False):
    combined_text = " ".join(str(t) for t in text)  # Join all elements of text into one string
    result = f"\n{combined_text}\n{'-' * 25}"

    if (returnValue):
        return result

    print(result)

def h5(text, returnValue = False):
    result = f"\n{text}\n{'-' * 20}"

    if (returnValue):
        return result

    print(result)

def h6(text, returnValue = False):
    result = f"\n{text}\n{'-' * 15}"

    if (returnValue):
        return result

    print(result)
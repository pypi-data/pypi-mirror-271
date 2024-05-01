def blockquote(items, indent_char='> ', emoji='💬', new_line = False, returnValue = False):
    if (new_line):
        print('\n')
    for item in items:
        print(f"{emoji} {indent_char}{item}")

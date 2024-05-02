def ordered_list(items, returnValue = False):
    for i, item in enumerate(items, start=1):
        print(f"{i}. {item}")

def bullet_list(items, bullet_char='*', returnValue = False):
    for item in items:
        print(f"{bullet_char} {item}")
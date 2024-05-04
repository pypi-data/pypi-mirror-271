'''
Used for various common tasks.
'''

def empty(a: int|list|str) -> bool:
    '''
    Returns True if a is empty ("", [], "-", etc.).'''
    if isinstance(a, list):
        if len(a) == 0:
            return True
        if len(a) == 1:
            a = a[0]
        else:
            for i in a:
                if not empty(i):
                    return False
            return True
    elif isinstance(a, str):
        return len(a) == 0 or a in ["-", " ", "."]
    elif isinstance(a, int):
        return a == 0
    return False

def latinise(word: str):
    '''
    Converts a string to latin characters.
    '''
    # āçēīłṉōṟşūƶĀÇĒĪŁṈŌṞŞŪƵ
    word = word.replace("ā", "a" )
    word = word.replace("ç", "ch")
    word = word.replace("ē", "e" )
    word = word.replace("ī", "i" )
    word = word.replace("ł", "w" )
    word = word.replace("ṉ", "ny")
    word = word.replace("ō", "o" )
    word = word.replace("ṟ", "rw")
    word = word.replace("ş", "sh")
    word = word.replace("ū", "u" )
    word = word.replace("ƶ", "zh")
    word = word.replace("Ā", "A" )
    word = word.replace("Ç", "Ch")
    word = word.replace("Ē", "E" )
    word = word.replace("Ī", "I" )
    word = word.replace("Ł", "W" )
    word = word.replace("Ṉ", "Ny")
    word = word.replace("Ō", "O" )
    word = word.replace("Ṟ", "Rw")
    word = word.replace("Ş", "Sh")
    word = word.replace("Ū", "U" )
    word = word.replace("Ƶ", "Zh")
    return word

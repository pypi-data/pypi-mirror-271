import functools

def vowels_counter(text, caseSensitive = True):
    """ This function counts the occurrence of each vowel in the text 
    
    param1 text: An input string form which vowels will be counted
    param2 caseSensitive: Default True. This parameter states if the vowels to bew counted should be treated as caseSensitive 
        that is, if True, 'a' and 'A' will be treated as different vowels and if False, 'a' and 'A' will be treated as a same vowel

    returns: A dictionary having vowel as key and its count in the text as value

    """

    if text == None or text == '':
        return {}
    
    vowels = None
    
    if caseSensitive:
        vowels = 'aeiouAEIOU'

    else:
        vowels = 'aeiou'
        text = text.lower()

    result = {}.fromkeys(vowels, 0)
    for t in text:
        if t in vowels:
            result[t] += 1

    return result

# vowels_counter("A fox was found in the jungle.", caseSensitive = True)
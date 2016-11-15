# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random

WORDLIST_FILENAME = "ps4/words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("ps4/fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    ###
    if shift > 27 or shift < -27:
        print "invalid entry"
        assert False
    elif shift < 0:
        # a negative shift is the same as 27 - the positive shift
        shift = 27 - abs(shift)
        # print shift
    else:
        pass
    # first what we do is define the list of alphabetical characters
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']
    # print len(alphabet)

    coded_key = {}

    for idx, letter in enumerate(alphabet):
        coded_key.update({letter : alphabet[(idx + shift)%27] })
        # print coded_key

    return coded_key

def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)

    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ###
    if shift > 27 or shift < 0:
        print "invalid entry"
        assert False
    else:
        pass

    encoder = build_coder(shift)

    return encoder

def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)

    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    ###
    if shift > 27 or shift < 0:
        print "invalid entry"
        assert False
    else:
        pass
    shift = 27 - shift #to decode we need to do the opposite shift for the encode

    decoder = build_coder(shift)

    return decoder

def apply_coder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    ### TODO
    encoded_text = ''

    for c in text:

        try: #try to encode, make sure to keep the cases the same

            if c.isupper():

                encoded_text = encoded_text + coder[c.lower()].upper()

            else:

                encoded_text = encoded_text + coder[c]

        except KeyError:  #must be punctuation if it's a keyError as it's not in our dict so leave alone
            encoded_text = encoded_text + c

        #print encoded_text

    return encoded_text

def apply_shift(text, shift, mode):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.

    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    ###
    if mode == 0: # encode
        shifted_text = apply_coder(text, build_encoder(shift))
    elif mode == 1: # decode
        shifted_text = apply_coder(text, build_decoder(shift))

    # print shifted_text

    return shifted_text
#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    """
    ### TODO
    best_shift = 0
    max_real_words = 0
    shift_words = 0

    for i in range(0,27,1):
        try_decode = apply_coder(text, build_decoder(i))
        word_list = try_decode.split(' ')

        for w in word_list:
            if is_word(wordlist, w):
                shift_words+=1

        if shift_words > max_real_words:
            max_real_words = shift_words
            best_shift = i


        shift_words = 0
        word_list = ''

    return best_shift
#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts, mode):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    ### TODO.
    if mode == "encode":
        mode = 0
    elif mode == "decode":
        mode = 1

    for c in shifts:
        text = text[:c[0]] + apply_shift(text[c[0]:], c[1], mode)

    #print text

    return text
# Problem 4: Multi-level decryption.
#


def find_best_shifts(wordlist, text):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)

    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """

    shifts = find_best_shifts_rec(wordlist, text, 0)

    return shifts
    # print apply_shifts(text, shifts)

def find_best_shifts_rec(wordlist, text, start):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """

    best_shift = 0
    max_real_words = 0
    shift_words = 0
    partial_decode = []
    partial_decode_txt = ''
    max_word_length = 0

    print "trying to decode: " + text[start:]

    for i in range(0,27,1):
        word_length = 0
        try_decode = apply_coder(text[start:], build_decoder(i))
        word_list = try_decode.split(' ')

        for w in word_list:
            if is_word(wordlist, w):
                shift_words+=1
                word_length = word_length + len(w)
            else:
                break;

        if (shift_words >= max_real_words) and (word_length > max_word_length):
            max_real_words = shift_words
            max_word_length = word_length
            best_shift = i
            partial_decode = word_list
            partial_decode_txt = try_decode

        shift_words = 0

    print partial_decode
    print str(start) + ' : ' + str(best_shift)
    print max_real_words
    print len(partial_decode)

    if max_real_words == 0: # we're fucked
    #couldn't find any real words, probably fucked
        return None

    elif max_real_words == len(partial_decode): # everything decoded.
        print "we're in the base case!"
        # print "the final values are: " + str(start) + ' : ' + str(best_shift)
        return [(start, best_shift)]

    else: #we need to keep decoding

        # now we need to find the new start value to send
        # this will be the location of the space after the final real word in the text
        new_start = start + len(" ".join(partial_decode[:max_real_words])) + 1
        # now we need to send through the correct decoded text
        new_text = text[:start] + partial_decode_txt

        # print "new_text:" + new_text
        # print "new_start:" + str(new_start)

        return [(start, best_shift)] + find_best_shifts_rec(wordlist, new_text, new_start)

def decrypt_fable():
    """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    s = get_fable_string()
    print s

    shifts = find_best_shifts(wordlist, s)
    print shifts

    decoded_fable = apply_shifts(s, shifts, 'decode')

    # print decoded_fable

    return decoded_fable




#What is the moral of the story?
#
#
#
#
#

# Decoding pseudocode
# 1. Apply a shift of zero
# 2. Run the text through the decoder
# 3. Separate into words by using spaces as a splitter
# 4. Check each words using the is_words function
# 5. Store result against the shift in a list [shift, num words, output text]
# 6. Repeat for each shift
# 7. Take the maximum num words found and then return the output text

# multi-decode pseudocode
# The base case will be when the text attempting to be shifted is already a word, so in this case return the shift/start tuple for it
# 1. Run find_best_shift for the whole text
# 2. Decode the string and then split into substrings based on the spaces.
# 3. Check that the first substring is a real word
# 4. If so, run the last substring again through the same algorithm
# 3.

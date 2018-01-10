# This file contains utilities for processing/cleanup/tokenizing text

from stopping import Stopping

import sys

## setup fwrite's encoding format
#reload(sys)
#sys.setdefaultencoding('utf-8')

## Globals ####################################################################

SPACE = " "

## Text processing utilities, static methods ###################################

# given a character c
# returns true iff the c is a whitespace.
# determine using c's ascii values
def is_whitespace(c):
    return (ord(c) >= 0 and ord(c) <= 32)

# given a character c
# returns true if and only if it is a quote, ', ", `
def is_quote(c):
    return (c == '"'  or \
            c == '\'' or \
            c == '`')

# given a character c
# returns true iff it is a backet (, ), {, }, [, ],
def is_bracket(c):
    return (c == '(' or \
            c == ')' or \
            c == '{' or \
            c == '}' or \
            c == '[' or \
            c == ']')

# given a character c
# returns true iff c is an !
def is_exclamation(c):
    return (c == '!')

# given a character c
# returns true iff c is an &
def is_ampersand(c):
    return (c == '&')


# given a character c
# returns true iff and only if it is a comma
def is_comma(c):
    return (c == ',')

# given a character c
# returns true iff the c is a
#   1. !
#   2. &
#   3. +
#   4. *
#   5. :
#   6. ;
#   7. <
#   8. >
#   9. =
#  10. ?
#  11. \
#  12. ^
#  13. _
#  14. ,
#  15. |
#  16. ~
#  17. whitespaces
#  18. quotes
#  19. brackets
#
def other_punctuation(c):
    return (is_whitespace(c)  or \
            is_quote(c)       or \
            is_bracket(c)     or \
            is_exclamation(c) or \
            is_ampersand(c)   or \
            (c == '+')        or \
            (c == '*')        or \
            (c == ':')        or \
            (c == ';')        or \
            (c == '>')        or \
            (c == '<')        or \
            (c == '?')        or \
            (c == '\\')       or \
            (c == '^')        or \
            (c == '_')        or \
            (c == '|')        or \
            (c == '~'))

## The following characters need special handling

# given a character c
# returns true if and only if it is a #
def is_hash(c):
    return (c == '#')

# given a character c
# returns true if and only if it is a $
def is_dollar(c):
    return (c == '$')

# given a character c
# returns true iff it is a percent
def is_percent(c):
    return (c == '%')

# given a character c
# returns true iff it is a hyphen/dash
def is_hyphen(c):
    return (c == '-')

# given a character c
# returns true iff it is a period
def is_period(c):
    return (c == '.')

# given a character c
# return true iff it is a @
def is_attherate(c):
    return (c == '@')

# given a character c
# returns true iff it is a number
def is_number(c):
    return (ord(c) >= 48 and ord(c) <= 57)

# given a character c
# returns true iff it is an upper case english alphabet
def is_alpha_upper(c):
    return (ord(c) >= 65 and ord(c) <= 90 )

# given a character c
# returns true iff it is a  lower case english alphabet
def is_alpha_lower(c):
    return (ord(c) >= 97 and ord(c) <= 122)

# given a character c
# returns true iff it is an alphabet
def is_alphabet(c):
    return (is_alpha_upper(c) or is_alpha_lower(c))

# given a character c
# returns true iff it is either an alphabet or a number
def is_alphanumeric(c):
    return (is_alphabet(c) or is_number(c))

# given a characer c
# always returns True. Refer to is_escorted_by() and its uses in the code for
# how this function is used
def is_any(c):
    return True

# given a text string
# return true iff the string is contains all numbers
def is_numeric(text):
    return all(map(lambda c: is_number(c), list(text)))

## Utilities ###################################################################

# given a ascii character string and a list of punctuations, replace all
# occurances of the punctuations in the list, to spaces
def to_space_punclst(text, puncs):

    # turn text to list
    textl = list(text)

    for i in range(0, len(textl)):
        if (textl[i] in puncs):
            textl[i] = SPACE

    # turn list back to string
    return list_to_string(textl)

# given a ascii character string and a method m, replace all characters in the
# string with spaces if the method m returns true with that character as input
def to_space(text, m):

    # turn text to list
    textl = list(text)

    for i in range(0, len(textl)):
        if (m(textl[i])):
            textl[i] = SPACE

    # turn list back to string
    return list_to_string(textl)

# given a list of ascii characters, and a postion in the list, return few
# characters around that position, including that character
def vicinity(textl, i):

    # vicinity region. NEIGHBOURHOOD characters
    NEIGHBOURHOOD = 10

    if (i > NEIGHBOURHOOD and len(textl) > i + NEIGHBOURHOOD):
        return textl[i-NEIGHBOURHOOD : i+NEIGHBOURHOOD]
    elif (i > NEIGHBOURHOOD and len(textl) < i + NEIGHBOURHOOD):
        return textl[i-NEIGHBOURHOOD:]
    elif (i < NEIGHBOURHOOD and len(textl) > i + NEIGHBOURHOOD):
        return textl[:i+NEIGHBOURHOOD]
    else:
        return textl

# Given a list of ascii characters, concatenate all the characters to form a
# string
def list_to_string(l):
    if l == []:
        return ""
    else:
        return reduce(lambda x, y: x + y, l)

# given a list of ascii chars, textl, a position, pos, in the string,
# and 2 functions, lc and rc, return true if and only if both
# lc(text[pos-1]) and rc(text[pos+1]) return true
def is_escorted_by(textl, pos, lc, rc):
    # cannot check left side
    if (pos == 0):
        return False

    # cannot check right side
    if (pos == len(textl) - 1):
        return False

    return (lc(textl[pos - 1]) and rc(textl[pos + 1]))

# given a ascii string text
# handles all occurances of the hash character
def handle_hash(text):

    # convert to list
    textl = list(text)

    for i in range(0, len(textl)):

        if is_hash(textl[i]):
            # may be hash is not really important ???
            textl[i] = SPACE

    # return processed list as string
    return list_to_string(textl)

# given a ascii string text handles all occurances of hyphens
def handle_hyphen(text):

    # convert to list
    textl = list(text)

    for i in range(0, len(textl)):

        if is_hyphen(textl[i]):
            # RULE : if the hyphen is accompanied on either sides by alnum.
            #        keep it!.
            keep_it = is_escorted_by(textl, i, is_alphanumeric, is_alphanumeric)

            if not keep_it:
                textl[i] = SPACE

    # return processed list as string
    return list_to_string(textl)

# given a ascii string, text, handles all occurances of @
def handle_attherate(text):

    # convert to list
    textl = list(text)

    for i in range(0, len(textl)):

        if is_attherate(textl[i]):
            # RULE: if @ appears sandwiched between alphanumerics. keep it!
            #       Why? : email addresses
            keep_it = is_escorted_by(textl, i, is_alphanumeric, is_alphanumeric)

            if not keep_it:
                textl[i] = SPACE

    # return processed list as string
    return list_to_string(textl)

# given a ascii string, text, handles all occurances of $
def handle_dollar(text):

    # convert to list
    textl = list(text)

    for i in range(0, len(textl)):

        if is_dollar(textl[i]):
            # RULE 1: if dollar is sandwiched between alphanumerics. keep it!
            #         Why? : US$5million
            # RULE 2: if dollar is the start of a word, i.e. sandwiched
            #         btw a whitespace, and a number. keep it!
            #         Why? : $5
            # RULE 3: if dollar is the end of word and has a number in before
            #         it. keep it!
            #         Why? : 5$
            keep_it = is_escorted_by(textl, i, is_alphanumeric, is_alphanumeric) or \
                      is_escorted_by(textl, i, is_whitespace, is_number)         or \
                      is_escorted_by(textl, i, is_number, is_whitespace)

            if not keep_it:
                textl[i] = SPACE

    return list_to_string(textl)

# given a ascii string, text, handle every occurance of a % sign
def handle_percent(text):

    # turn text string to list
    textl = list(text)

    for i in range(0, len(textl)):

        if (is_percent(textl[i])):
            # RULE 1: if the % sign is the start of a word and followed by a
            #         number. keep it!
            #         Why? : %5
            # RULE 2: if the % sign is the end of a word and preceded by a number.
            #         keep it!
            #         Why? : 5%
            keep_it = is_escorted_by(textl, i, is_whitespace, is_number) or \
                      is_escorted_by(textl, i, is_number, is_whitespace)

            if not keep_it:
                textl[i] = SPACE

    return list_to_string(textl)

# given a list of ascii characters, handle every occurance of period
def handle_period(text):

    # Convert text to list
    textl = list(text)

    # Running processed text
    rtext = ""

    for i in range(0, len(textl)):

        if (is_period(textl[i])):

            # Keep period rules !!!
            # RULE 1 : if period is escorted by a number on both sides. keep it!
            #           Why? : 0.5
            # RULE 2 : if period is has a number to its right and a whitespace to
            #          to its left. keep it!
            #          Why? : .5
            preserve_period = is_escorted_by(textl, i, is_number, is_number) or \
                              is_escorted_by(textl, i, is_whitespace, is_number)

            if preserve_period:
                rtext = rtext + textl[i]
                continue

            # Delete period rules !!!
            # RULE 1 : if period is sandwiched between, 2 Capital letters. delete it!
            #          Why? : U.S -> US
            # RULE 2 : if period is preceded by a Capital letter and followed by
            #          a space and then a non captial letter. delete it.
            #          Why? : "U.S.A. is a nice country" -> "USA is a nice country":
            delete_period = (is_escorted_by(textl, i, is_alpha_upper, is_alpha_upper) or  \
                             (is_escorted_by(textl, i, is_alpha_upper, is_whitespace) and \
                              (not is_escorted_by(textl, i+1, is_period, is_alpha_upper))))

            if delete_period:
                # We are deleting it. End of discussion
                # Deleting is equivalent to not adding period to rtext
                continue

            # Replace with space
            rtext = rtext + SPACE
            continue

        # not a period. we want it !
        rtext = rtext + textl[i]

    return rtext

# given a ascii string, handles every occurance of comma
def handle_comma(text):

    # list version of string
    textl = list(text)

    for i in range(0, len(text)):

        if is_comma(textl[i]):

            # RULE 1: if there is an number on either sides of the comma
            #         preserve it.
            #         Why? : 2,000
            keep_it = is_escorted_by(textl, i, is_number, is_number)

            if not keep_it:
                textl[i] = SPACE

    return list_to_string(textl)

## Export functions ############################################################

# given a text txt
# handle all punctuations in the text and return
def handle_punctuation(text):

    assert (text != None)

    # NOTE: it is very important to turn punctuations that dont have any special
    #       rules to convert to space FIRST
    #       This is because, handling punctuations that are important and have
    #       more semantic meaning, contain rules, that depend on the neighbouring
    #       characters being spaces.
    #       I think, in general it is better to process punctuations that less
    #       rules first and more rules last

    # other punctuations;; These punctuations are not special... we want to turn
    # their occurance to spaces
    to_space_punc = ['#', '@', '$', '!', '&', '+', '*', ':', ';', '>', '<', \
                     '?', '\\', '^', '/', '|', '~', '_', '%', '=']

    # handle punctuations that we can just turn to spaces
    text = to_space_punclst(text, to_space_punc)
    # handle whitespaces
    text = to_space(text, is_whitespace)
    # handle quotes
    text = to_space(text, is_quote)
    # handle braces
    text = to_space(text, is_bracket)

    # comma
    text = handle_comma(text)
    # hyphen
    text = handle_hyphen(text)
    # period
    text = handle_period(text)

    return text

# given an ASCII text string, perform fold all alphabets in the text to lowercase
# returns casefolded text
def foldcase(text):
    return text.lower()

# given an ASCII text string. Preserves only 1 whitespace between words in the
# string.
# returns the text string that is rid of extraneous whitespaces
def clean_extraneous_whitespace(text):

    # convert all whitespaces to just spaces
    text = to_space(text, is_whitespace)

    # convert text to words
    words = text.split(" ")

    # filter words that are not whitespaces
    words = filter(lambda w: w.strip() != "", words)

    # strip words off whitespaces
    words = map(lambda w: w.strip(), words)

    return " ".join(words)

# given an ASCII text string, do necessary processing and return the processed text
def process_text(text, stopfile = "", casefold = True, handlepunc = True):

    # handle punctuations
    if (handlepunc):
        text = handle_punctuation(text)

    # fold case
    if (casefold):
        text = foldcase(text)

    # clean the text. remove extraneous whitespace
    text = clean_extraneous_whitespace(text)

    # remove stopwords
    text = Stopping(stopfile).stop(text)

    return text

# given an ASCII text string, and a non negative integer n
# returns a list of all word ngrams in the input string
def word_ngrams(text, n):

    assert(n > 0)

    words = text.split(' ')

    ng = []

    for i in range(0, len(words) - n + 1):
        # word ngram
        wng = " ".join(words[i:i+n])
        assert (len(wng.split(" ")) == n)
        # store word ngram
        ng.append(" ".join(words[i:i+n]))

    return ng


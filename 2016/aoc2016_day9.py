
'''
Advent of Code - 2016 - Day 9
http://adventofcode.com/2016

Last Updated: 2017-Feb-02
First Created: 2017-Jan-08
Python 3.5
Chris

--- Day 9: Explosives in Cyberspace ---

Wandering around a secure area, you come across a datalink port to a new part of the network.
After briefly scanning it for interesting files, you find one file in particular that catches your attention.
It's compressed with an experimental format, but fortunately, the documentation for the format is nearby.

The format compresses a sequence of characters. Whitespace is ignored. To indicate that some sequence should be repeated, a marker is added to the file, like (10x2).
To decompress this marker, take the subsequent 10 characters and repeat them 2 times.
Then, continue reading the file after the repeated data. The marker itself is not included in the decompressed output.

If parentheses or other characters appear within the data referenced by a marker, that's okay -
treat it like normal data, not a marker, and then resume looking for markers after the decompressed section.

For example:

    ADVENT contains no markers and decompresses to itself with no changes, resulting in a decompressed length of 6.
    A(1x5)BC repeats only the B a total of 5 times, becoming ABBBBBC for a decompressed length of 7.
    (3x3)XYZ becomes XYZXYZXYZ for a decompressed length of 9.
    A(2x2)BCD(2x2)EFG doubles the BC and EF, becoming ABCBCDEFEFG for a decompressed length of 11.
    (6x1)(1x3)A simply becomes (1x3)A - the (1x3) looks like a marker, but because it's within a data section of another marker,
    it is not treated any differently from the A that comes after it. It has a decompressed length of 6.
    X(8x2)(3x3)ABCY becomes X(3x3)ABC(3x3)ABCY (for a decompressed length of 18), because the decompressed data from the (8x2) marker (the (3x3)ABC) is skipped and not processed further.

What is the decompressed length of the file (your puzzle input)? Don't count whitespace.

To begin, get your puzzle input.

--- Part Two ---

Apparently, the file actually uses version two of the format.

In version two, the only difference is that markers within decompressed data are decompressed. This, the documentation explains, provides much more substantial compression capabilities,
allowing many-gigabyte files to be stored in only a few kilobytes.

For example:

    (3x3)XYZ still becomes XYZXYZXYZ, as the decompressed section contains no markers.
    X(8x2)(3x3)ABCY becomes XABCABCABCABCABCABCY, because the decompressed data from the (8x2) marker is then further decompressed, thus triggering the (3x3) marker twice for a total of six ABC sequences.
    (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated 241920 times.
    (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.

Unfortunately, the computer you brought probably doesn't have enough memory to actually decompress the file; you'll have to come up with another way to get its decompressed length.

What is the decompressed length of the file using this improved format?

'''

import re

def get_data():
    with open('aoc2016_day9.txt', 'r') as input_file:
        return input_file.read()

def problem_one(data):
    ans = ''
    current_index = 0
    bracket = -1
    for idx, character in enumerate(data):
        if idx >= current_index:
            if bracket == -1:
                if character == '(':
                    bracket = idx
                else:
                    ans += character
            else:
                if character == ')':
                    a, b = [int(x) for x in data[bracket + 1:idx].split('x')] # a = num characters, b = num times to repeat
                    # print('hi', data[current_index:bracket])
                    # print('hi2', idx+1, a, data[idx + 1: idx + 1 + a] * b)
                    ans += data[idx + 1: idx + 1 + a] * b
                    current_index = idx + 1 + a
                    bracket = -1

    return ans

def problem_two(data):
    ans = ''
    current_index = 0
    bracket = -1
    for idx, character in enumerate(data):
        if idx >= current_index:
            if bracket == -1:
                if character == '(':
                    bracket = idx
                else:
                    ans += character
            else:
                if character == ')':
                    a, b = [int(x) for x in data[bracket + 1:idx].split('x')] # a = num characters, b = num times to repeat
                    new_data = data[idx + 1: idx + 1 + a] * b + data[idx + 1 + a:]
                    return len(ans) + problem_two(new_data)


    return len(ans)

### norvig
matcher = re.compile(r'[(](\d+)x(\d+)[)]').match # e.g. matches "(2x5)" as ('2', '5')
def decompress_length(s):
    """Decompress string s by interpreting '(2x5)' as making 5 copies of the next 2 characters.
    Recursively decompress these next 5 characters. Return the length of the decompressed string."""
    s = re.sub(r'\s', '', s) # "whitespace is ignored"
    length = 0
    i = 0
    while i < len(s):
        m = matcher(s, i)
        if m:
            C, R = map(int, m.groups())
            i = m.end(0)                              # Advance to end of '(CxR)'
            length += R * decompress_length(s[i:i+C]) # Decompress C chars and add to length
            i += C                                    # Advance past the C characters
        else:
            length += 1                               # Add 1 regular character to length
            i += 1                                    # Advance past it
    return length

def decompress(s):
    "Decompress string s by interpreting '(2x5)' as making 5 copies of the next 2 characters."
    s = re.sub(r'\s', '', s) # "whitespace is ignored"
    result = []
    i = 0
    while i < len(s):
        m = matcher(s, i)
        if m:
            i = m.end()                # Advance to end of '(CxR)' match
            C, R = map(int, m.groups())
            result.append(s[i:i+C] * R) # Collect the C characters, repeated R times
            i += C                      # Advance past the C characters
        else:
            result.append(s[i])         # Collect 1 regular character
            i += 1                      # Advance past it
    return cat(result)
###

test_data = ['ADVENT', 'A(1x5)BC', '(3x3)XYZ', 'A(2x2)BCD(2x2)EFG', '(6x1)(1x3)A', 'X(8x2)(3x3)ABCY', '(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN']
test_data = ['ADVENT', 'A(2x2)BCD(2x2)EFG']

def do_one():
    for item in test_data:
        print(decompress(item))

    data = get_data()
    result = problem_one(data)
    print(len(result), 120765)


def do_two():
    for item in test_data:
        ans = problem_two(item)
        print(ans)
        try:
            print(len(ans))
        except TypeError:
            pass
    # data = get_data()
    # result = problem_two(data)
    # print(result)

do_one()

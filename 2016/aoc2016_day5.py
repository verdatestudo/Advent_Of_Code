
'''
Advent of Code - 2016 - Day 5
http://adventofcode.com/2016

Last Updated: 2017-Jan-07
First Created: 2017-Jan-06
Python 3.5
Chris

--- Day 5: How About a Nice Game of Chess? ---

You are faced with a security door designed by Easter Bunny engineers that seem to have acquired most of their security knowledge by watching hacking movies.

The eight-character password for the door is generated one character at a time by finding the MD5 hash of some Door ID (your puzzle input) and an increasing integer index (starting with 0).

A hash indicates the next character in the password if its hexadecimal representation starts with five zeroes. If it does, the sixth character in the hash is the next character of the password.

For example, if the Door ID is abc:

    The first index which produces a hash that starts with five zeroes is 3231929, which we find by hashing abc3231929; the sixth character of the hash, and thus the first character of the password, is 1.
    5017308 produces the next interesting hash, which starts with 000008f82..., so the second character of the password is 8.
    The third time a hash starts with five zeroes is for abc5278568, discovering the character f.

In this example, after continuing this search a total of eight times, the password is 18f47a30.

Given the actual Door ID, what is the password?

Your puzzle input is reyedfim.

--- Part Two ---

As the door slides open, you are presented with a second door that uses a slightly more inspired security mechanism. Clearly unimpressed by the last version (in what movie is the password decrypted in order?!), the Easter Bunny engineers have worked out a better solution.

Instead of simply filling in the password from left to right, the hash now also indicates the position within the password to fill. You still look for hashes that begin with five zeroes; however, now, the sixth character represents the position (0-7), and the seventh character is the character to put in that position.

A hash result of 000001f means that f is the second character in the password. Use only the first result for each position, and ignore invalid positions.

For example, if the Door ID is abc:

    The first interesting hash is from abc3231929, which produces 0000015...; so, 5 goes in position 1: _5______.
    In the previous method, 5017308 produced an interesting hash; however, it is ignored, because it specifies an invalid position (8).
    The second interesting hash is at index 5357525, which produces 000004e...; so, e goes in position 4: _5__e___.

You almost choke on your popcorn as the final character falls into place, producing the password 05ace8e3.

Given the actual Door ID and this new method, what is the password? Be extra proud of your solution if it uses a cinematic "decrypting" animation.

'''

import hashlib
from itertools import count
from itertools import islice
import timeit


def get_next_digit(puzzle_input):
    '''
    Generator. Yields the md5 hash of puzzle_input + ascending number, where the first
    five digits are '00000'.
    (Using [0:5] is supposedly quicker than 'startswith')
    '''
    for x in count():
        md5_hash = hashlib.md5('{}{}'.format(puzzle_input, x).encode('utf-8')).hexdigest()
        if md5_hash[0:5] == '00000':
            yield md5_hash

def get_door_id_basic(puzzle_input, password_length):
    '''
    Solution using generator. See description.
    '''
    digits = iter(get_next_digit(puzzle_input))
    answers = [next(digits)[5] for _ in range(password_length)]
    return ''.join(answers)

def get_door_id_slice(puzzle_input, password_length):
    '''
    Using itertools islice, slightly quicker.
    '''
    hashes = islice(get_next_digit(puzzle_input), password_length)
    return ''.join([x[5] for x in hashes]) # only need 6th digit.

def get_door_id_2(puzzle_input, password_length):
    '''
    Part 2. Get md5 hash starting with '00000'. 6th digit is index of answer,
    if it's an integer, and if that index hasn't already been used.
    7th digit is the answer.
    '''
    hashes = iter(get_next_digit(puzzle_input)) # use iter so generator remembers it's position and doesn't start again from start.
    answers = ['' for _ in range(password_length)]
    while any([x == '' for x in answers]):
        print(answers)
        next_hash = next(hashes)
        position_hash = int(next_hash[5], 16) # use base 16 as per norvig answer.
        if 0 <= position_hash < 8 and answers[position_hash] == '':
            answers[position_hash] = next_hash[6]
    return ''.join(answers)

def get_door_id_old(puzzle_input, password_length):
    '''
    Solution without generator. Kept to show time difference.
    '''
    answers = []
    for x in count():
        md5_hash = hashlib.md5('{}{}'.format(puzzle_input, x).encode('utf-8')).hexdigest()
        if md5_hash[0:5] == '00000':
            answers.append(md5_hash[5])
        if len(answers) == password_length:
            return ''.join(answers)

def run_and_time(funk, details):
    '''
    Run and time a funk (function) using details (tuple).
    '''
    test_input, password_length, answer = details
    start = timeit.default_timer()
    print(funk(test_input, password_length), answer)
    stop = timeit.default_timer()
    print('Running time for {}: {:.4f}'.format(funk.__name__, stop - start))


test1 = ('abc', 8, '18f47a30')
ans1 = ('reyedfim', 8, 'f97c354d')

test2 = ('abc', 8, '05ace8e3')
ans2 = ('reyedfim', 8, '863dde27')

# run_and_time(get_door_id_basic, test1) # ~ 48.5 secs
# run_and_time(get_door_id_old, test1) # ~ 53.3 secs
# run_and_time(get_door_id_slice, test1) # ~ 47.5 secs

# run_and_time(get_door_id_2, test2) # ~ 67.8 secs
# run_and_time(get_door_id_2, ans2) # ~ 126.2 secs

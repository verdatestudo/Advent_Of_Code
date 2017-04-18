
'''
Advent of Code - 2016 - Day 4
http://adventofcode.com/2016

Last Updated: 2017-Jan-05
First Created: 2017-Jan-02
Python 3.5
Chris

--- Day 4: Security Through Obscurity ---

Finally, you come across an information kiosk with a list of rooms.
Of course, the list is encrypted and full of decoy data, but the instructions to decode the list are barely hidden nearby.
Better remove the decoy data first.

Each room consists of an encrypted name (lowercase letters separated by dashes) followed by a dash, a sector ID, and a checksum in square brackets.

A room is real (not a decoy) if the checksum is the five most common letters in the encrypted name, in order, with ties broken by alphabetization. For example:

    aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters are a (5), b (3), and then a tie between x, y, and z, which are listed alphabetically.
    a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are all tied (1 of each), the first five are listed alphabetically.
    not-a-real-room-404[oarel] is a real room.
    totally-real-room-200[decoy] is not.

Of the real rooms from the list above, the sum of their sector IDs is 1514.

What is the sum of the sector IDs of the real rooms?

--- Part Two ---

With all the decoy data out of the way, it's time to decrypt this list and get moving.

The room names are encrypted by a state-of-the-art shift cipher, which is nearly unbreakable without the right software.
However, the information kiosk designers at Easter Bunny HQ were not expecting to deal with a master cryptographer like yourself.

To decrypt a room name, rotate each letter forward through the alphabet a number of times equal to the room's sector ID. A becomes B, B becomes C, Z becomes A, and so on. Dashes become spaces.

For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.

What is the sector ID of the room where North Pole objects are stored?


'''

import re

def get_file_input(filename):
    with open(filename, 'r') as data_file:
        parsed_data = []
        for line in data_file:
            parsed_data.append(re.match(r"(.+)-(\d+)\[([a-z]+)\]", line).groups())
    return parsed_data

def day4():
    #data = get_file_input('aoc2016_day4.txt')
    data = [['aaaaa-bbb-z-y-x', '123', 'abxyz'], ['a-b-c-d-e-f-g-h', '987', 'abcde'], ['not-a-real-room', '404', 'oarel'], ['totally-real-room', '200', 'decoy']]

    answer = 0

    for letters, value, five in data:
        # should use Counter here.
        count_dict = {letter: letters.count(letter) for letter in letters if letter != '-'}
        order_dict = [[key, value] for key, value in count_dict.items()]
        # can sort both at same time by converting to negative (for reverse)
        order_dict = sorted(order_dict, key = lambda x: x[0])
        order_dict = sorted(order_dict, key = lambda x: x[1], reverse=True)
        if ''.join(x[0] for x in order_dict[0:5]) == five:
            answer += int(value)
    return answer

def day4_2():
    data = get_file_input('aoc2016_day4.txt')
    #data = [['aaaaa-bbb-z-y-x', '123', 'abxyz'], ['a-b-c-d-e-f-g-h', '987', 'abcde'], ['not-a-real-room', '404', 'oarel'], ['totally-real-room', '200', 'decoy']]

    answer = []

    for letters, value, five in data:
        # should use maketrans and translate as per Norvig solution.
        my_string = ''.join([chr(((ord(x) - 97 + int(value)) % 26) + 97) if x != '-' else x for x in letters]).replace('-', ' ')
        answer.append([my_string, value])

    with open('aoc2016_day4_answer.txt', 'w') as the_file:
        for item in answer:
            the_file.write(' '.join([item[0], item[1], '\n']))

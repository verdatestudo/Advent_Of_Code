'''
Advent of Code - 2016 - Day 21
http://adventofcode.com/2016

Last Updated: 2017-Mar-08
First Created: 2017-Mar-03
Python 3.5
Chris

--- Day 21: Scrambled Letters and Hash ---

The computer system you're breaking into uses a weird scrambling function to store its passwords.
It shouldn't be much trouble to create your own scrambled password so you can add it to the system; you just have to implement the scrambler.

The scrambling function is a series of operations (the exact list is provided in your puzzle input).
Starting with the password to be scrambled, apply each operation in succession to the string. The individual operations behave as follows:

    swap position X with position Y means that the letters at indexes X and Y (counting from 0) should be swapped.
    swap letter X with letter Y means that the letters X and Y should be swapped (regardless of where they appear in the string).
    rotate left/right X steps means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
    rotate based on position of letter X means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations.
    Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
    reverse positions X through Y means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
    move position X to position Y means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.

For example, suppose you start with abcde and perform the following operations:

    swap position 4 with position 0 swaps the first and last letters, producing the input for the next step, ebcda.
    swap letter d with letter b swaps the positions of d and b: edcba.
    reverse positions 0 through 4 causes the entire string to be reversed, producing abcde.
    rotate left 1 step shifts all letters left one position, causing the first letter to wrap to the end of the string: bcdea.
    move position 1 to position 4 removes the letter at position 1 (c), then inserts it at position 4 (the end of the string): bdeac.
    move position 3 to position 0 removes the letter at position 3 (a), then inserts it at position 0 (the front of the string): abdec.
    rotate based on position of letter b finds the index of letter b (1), then rotates the string right once plus a number of times equal to that index (2): ecabd.
    rotate based on position of letter d finds the index of letter d (4), then rotates the string right once, plus a number of times equal to that index,
    plus an additional time because the index was at least 4, for a total of 6 right rotations: decab.

After these steps, the resulting scrambled password is decab.

Now, you just need to generate a new scrambled password and you can access the system. Given the list of scrambling operations in your puzzle input, what is the result of scrambling abcdefgh?

To begin, get your puzzle input.

Your puzzle answer was agcebfdh.
--- Part Two ---

You scrambled the password correctly, but you discover that you can't actually modify the password file on the system. You'll need to un-scramble one of the existing passwords by reversing the scrambling process.

What is the un-scrambled version of the scrambled password fbgdceah?

Your puzzle answer was afhdbegc.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

from itertools import permutations

def parse_data(filename='aoc2016_day21.txt'):
    """Split each line of commands into individual words and extract important parts."""

    # idx of important parts of string depending on cmd type.
    step_dict = {'swap': (0, 2, 5),
                 'reverse': (0, 2, 4),
                 'rotate': (0, 1, -2, -1),
                 'move': (0, 2, 5)
                 }

    try:
        with open(filename, 'r') as f:
            steps = f.readlines()
    except FileNotFoundError:
        steps = TEST_STEPS

    for step in steps:
        details = step.split()
        yield [int(details[x]) if details[x].isdigit() else details[x] for x in step_dict[details[0]]]

def swap_password(chars, x, y):
    if isinstance(x, str): x, y = chars.index(x), chars.index(y)

    chars[x], chars[y] = chars[y], chars[x]
    return chars

def reverse_password(chars, x, y):
    chars[x:y+1] = chars[x:y+1][::-1]
    return chars

def rotate_password(chars, x, y, z):
    if isinstance(y, str):
        # then rotate right based on position of z, + 1, +1 if i >=4. Use modulo.
        i = chars.index(z)
        y = (i + 1 + (i >= 4)) % len(chars)
        return chars[-y:] + chars[:-y]
    else:
        # rotate based on direction x, using y amount
        if x == 'left':
            return chars[y:] + chars[:y]
        else:
            return chars[-y:] + chars[:-y]

def move_password(chars, x, y):
    chars.insert(y, chars.pop(x))
    return chars

def move_dict(password, operator, x, y, z=0):
    return {
        'swap': lambda: swap_password(password, x, y),
        'reverse': lambda: reverse_password(password, x, y),
        'rotate': lambda: rotate_password(password, x, y, z),
        'move': lambda: move_password(password, x, y)
    }.get(operator, None)()

def part_one(password, filename='aoc2016_day21.txt'):
    chars = list(password)
    for cmd in parse_data(filename):
        chars = move_dict(chars, *cmd)
    return ''.join(chars)

def part_two(password, goal_password='fbgdceah'):
    """ Password is short enough to simply try each permutation.

    If using an unscramble function, I believe the steps would be:
    - swap: same
    - reverse: same
    - rotate: left = right, right = left
    - rotate: would have to test each possibility
    - move: reverse it
    """
    for perm in permutations(password):
        potential_password = ''.join(perm)
        print('Calculating permutation: {}'.format(potential_password))
        if part_one(perm) == goal_password:
            return ''.join(perm)

TEST_STEPS = ['swap position 4 with position 0',
         'swap letter d with letter b',
         'reverse positions 0 through 4',
         'rotate left 1 step',
         'move position 1 to position 4',
         'move position 3 to position 0',
         'rotate based on position of letter b',
         'rotate based on position of letter d'
         ]

print(part_one('abcdefgh'))
print(part_one('abcde', filename='test'))
# print(part_two('fbgdceah'))

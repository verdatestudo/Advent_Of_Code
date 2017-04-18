'''
Advent of Code - 2016 - Day 15
http://adventofcode.com/2016

Last Updated: 2017-Feb-24
First Created: 2017-Feb-22
Python 3.5
Chris

--- Day 15: Timing is Everything ---

The halls open into an interior plaza containing a large kinetic sculpture.
The sculpture is in a sealed enclosure and seems to involve a set of identical spherical capsules
that are carried to the top and allowed to bounce through the maze of spinning pieces.

Part of the sculpture is even interactive!
When a button is pressed, a capsule is dropped and tries to fall through slots
in a set of rotating discs to finally go through a little hole at the bottom and come out of the sculpture.
If any of the slots aren't aligned with the capsule as it passes, the capsule bounces off the disc and soars away.
You feel compelled to get one of those capsules.

The discs pause their motion each second and come in different sizes; they seem to each have a fixed number of positions at which they stop.
You decide to call the position with the slot 0, and count up for each position it reaches next.

Furthermore, the discs are spaced out so that after you push the button, one second elapses before the first disc is reached,
and one second elapses as the capsule passes from one disc to the one below it.
So, if you push the button at time=100, then the capsule reaches the top disc at time=101, the second disc at time=102, the third disc at time=103, and so on.

The button will only drop a capsule at an integer time - no fractional seconds allowed.

For example, at time=0, suppose you see the following arrangement:

Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.

If you press the button exactly at time=0, the capsule would start to fall; it would reach the first disc at time=1.
Since the first disc was at position 4 at time=0, by time=1 it has ticked one position forward.
As a five-position disc, the next position is 0, and the capsule falls through the slot.

Then, at time=2, the capsule reaches the second disc.
The second disc has ticked forward two positions at this point: it started at position 1, then continued to position 0, and finally ended up at position 1 again.
Because there's only a slot at position 0, the capsule bounces away.

If, however, you wait until time=5 to push the button, then when the capsule reaches each disc,
the first disc will have ticked forward 5+1 = 6 times (to position 0),
and the second disc will have ticked forward 5+2 = 7 times (also to position 0).
In this case, the capsule would fall through the discs and come out of the machine.

However, your situation has more than two discs; you've noted their positions in your puzzle input.
What is the first time you can press the button to get a capsule?

Your puzzle answer was 121834.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

After getting the first capsule (it contained a star! what great fortune!),
the machine detects your success and begins to rearrange itself.

When it's done, the discs are back in their original configuration as if it were time=0 again,
but a new disc with 11 positions and starting at position 0 has appeared exactly one second below the previously-bottom disc.

With this new disc, and counting again starting from time=0 with the configuration in your puzzle input,
what is the first time you can press the button to get another capsule?

Your puzzle answer was 3208099.

Both parts of this puzzle are complete! They provide two gold stars: **
'''

import re
from collections import namedtuple
from operator import mul
from functools import reduce
import hashlib

def get_data(part_two=False):
    data = []
    with open('aoc2016_day15.txt', 'r') as f:
        for idx, line in enumerate(f, 1):
            total_positions, time, start_position = [int(x) for x in re.match(r'.* (\d+) positions; at time=(\d+), it is at position (\d+).', line).groups()]
            data.append(Disc(idx, total_positions, time, start_position))
    if part_two:
        data.append(Disc(7, 11, 0, 0))
    return tuple(data)

def solve(data):
    '''
    Disc start position + idx (i.e time lag after button press) gives the position
    of the disc at time = 0. Therefore if you add current_time (which is the time we press the button),
    you get the position of the disc at time = current_time.

    If all discs are at position = 0 at current_time, then we have a solution.

    Note: optimization by getting the max positions disc.
    With my data this is 19, so we find the first time this disc is open
    (total_positions - idx - start_position) = 19 - 6 - 7 = 6.
    So our answer must be in the range(6, BIG_NUMBER, 19), i.e 6, 25, 44 etc.
    '''
    big = 100000000000000000000000000000000000000000000000
    max_disc = [disc for disc in data if disc.total_positions == max([disc2.total_positions for disc2 in data])][0]

    for current_time in range(max_disc.total_positions - max_disc.start_position - max_disc.idx, big, max_disc.total_positions):
        if all((disc.start_position + disc.idx + current_time) % disc.total_positions == 0 for disc in data):
            return 'Discs are first aligned at: {}'.format(current_time)

def solve_crm(data):
    '''
    Solve using CRM (see additional_crm)
    '''
    product_of_mods = reduce(mul, [disc.total_positions for disc in data])
    nums = []

    for idx, disc in enumerate(data):
        disc_product_of_mods = product_of_mods // disc.total_positions # product of all mods (total positions) except current disc
        target_rem = disc.total_positions - disc.start_position - disc.idx # target remainder is when disc reaches open position (p=0). e.g disc with 43 positions, starting at 2, idx at 1 is 40.
        rem = disc_product_of_mods % disc.total_positions

        nums.append(mod_inv(rem, disc.total_positions) * target_rem * disc_product_of_mods)
    return 'Discs are first aligned at: {}'.format(sum(nums) % product_of_mods)

def extended_gcd(aa, bb):
    '''
    From: https://rosettacode.org/wiki/Modular_inverse#Python
    '''
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def mod_inv(a, m):
    '''
    From: https://rosettacode.org/wiki/Modular_inverse#Python
    '''
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m

def additional_crm(part_two=False):
    '''
    https://www.reddit.com/r/adventofcode/comments/5ifvyc/2016_day_15_part_3_our_discs_got_larger/

    Disc #1 has 43 positions; at time=0, it is at position 2.
    Disc #2 has 53 positions; at time=0, it is at position 7.
    Disc #3 has 61 positions; at time=0, it is at position 10.
    Disc #4 has 37 positions; at time=0, it is at position 2.
    Disc #5 has 127 positions; at time=0, it is at position 9.

    Spoiler: 6xxxxxxx5

    Disc #1 has 101 positions; at time=0, it is at position 2.
    Disc #2 has 163 positions; at time=0, it is at position 7.
    Disc #3 has 263 positions; at time=0, it is at position 10.
    Disc #4 has 293 positions; at time=0, it is at position 2.
    Disc #5 has 373 positions; at time=0, it is at position 9.
    Disc #6 has 499 positions; at time=0, it is at position 0.
    Disc #7 has 577 positions; at time=0, it is at position 0.

    Spoiler: 6xxxxxxxxxxxxxxx6

    Need to use Chinese Remainder Theorem to solve this efficiently.

    https://www.youtube.com/watch?v=ru7mWZJlRQg
    http://www.cut-the-knot.org/blue/chinese.shtml

    Example:
    Consider x = 2 (mod3), x = 2 (mod 4), x = 1 (mod 5)
    Fill in other mods to each section e.g x = (4*5) + (3*5) + (3*4)
    If remainder of new number = final remainder, do nothing. e.g (4*5) mod 3 = 2
    Else, make it equal remainder 1 (always go to this step for large numbers, finding the inverse, using extended euclidean algorithm).
    https://www.youtube.com/watch?v=mgvA3z-vOzc
    e.g (3*4) mod 5 = 2. Take that 2*3 mod 5 = 1. So final number is (3*4*3).
    Then get to required remainder. e.g (3*5) mod 4 = 3. 3*3 mod 4 = 1. 1*2 mod 4 = 2. Final number is (3*5*3*2).
    Add all numbers together - (4*5=20) + (3*5*3*2=90) + (3*4*3=36) = 146.
    This is a solution, and to find other solutions add/subtract total mod (3*4*5=60). e.g 26, 86, 146, 206 are all solutions.
    '''
    if not part_two:
        data = tuple([\
        Disc(1, 43, 0, 2),\
        Disc(2, 53, 0, 7),\
        Disc(3, 61, 0, 10),\
        Disc(4, 37, 0, 2),\
        Disc(5, 127, 0, 9)
        ])

        return solve_crm(data)

    else:
        data = tuple([\
        Disc(1, 101, 0, 2),\
        Disc(2, 163, 0, 7),\
        Disc(3, 263, 0, 10),\
        Disc(4, 293, 0, 2),\
        Disc(5, 373, 0, 9),\
        Disc(6, 499, 0, 0),\
        Disc(7, 577, 0, 0)
        ])

        return solve_crm(data)

import pdb

def md5_hash_check(hashes):
    for idx in range(len(hashes[0])):
        if all(x[idx] is '0' for x in hashes):
            return idx
    return False

def additional_md5_hash(n=8, time=0):
    '''
    https://www.reddit.com/r/adventofcode/comments/5ig8xp/2016_day_15_sculpture_now_with_anticheat_measures/

    Using md5 hashes, find n hashes in a row that have a 0 in the same index location.
    '''
    hashes = ['00000000000000000000000000000000']
    #hashes = ['e993e9aea4402d5749251b307c1188f0'] # test

    for _ in range(n):
        hashes.append(hashlib.md5(hashes[-1].encode('utf-8')).hexdigest())
    while md5_hash_check(hashes[-n:]) == False:
        time += 1
        hashes.pop(0)
        print(time, hashes[-1])
        hashes.append(hashlib.md5(hashes[-1].encode('utf-8')).hexdigest())
    return 'Press the button at t = {} and location = {}.'.format(time, md5_hash_check(hashes[-n:]))


Disc = namedtuple('Disc', ['idx', 'total_positions', 'time', 'start_position'])

print(solve(get_data()))
print(solve(get_data(part_two=True)))
print(additional_crm())
print(additional_crm(part_two=True))
# print(additional_md5_hash(7), 4445615, 14)
#print(additional_md5_hash(8), 204947638, 13)

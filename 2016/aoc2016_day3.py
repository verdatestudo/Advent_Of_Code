
'''
Advent of Code - 2016 - Day 3
http://adventofcode.com/2016

Last Updated: 2017-Jan-02
First Created: 2017-Jan-02
Python 3.5
Chris

--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways and office furniture that makes up this part of Easter Bunny HQ.
This must be a graphic design department; the walls are covered in specifications for triangles.

Or are they?

The design document gives the side lengths of each triangle it describes, but... 5 10 25? Some of these aren't triangles. You can't help but mark the impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining side.
For example, the "triangle" given above is impossible, because 5 + 10 is not larger than 25.

In your puzzle input, how many of the listed triangles are possible?

--- Part Two ---

Now that you've helpfully marked up their design documents, it occurs to you that triangles are specified in groups of three vertically. Each set of three numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification, numbers with the same hundreds digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603

In your puzzle input, and instead reading by columns, how many of the listed triangles are possible?

'''

import re

def get_data_from_file(day):
    "Open this day's input file."
    filename = 'aoc2016_day{}.txt'.format(day)
    data = [[int(x) for x in re.findall('(\d+)', line)] for line in open(filename, 'r')]
    return data

def check_triangle_1():
    '''
    See description.
    '''
    data = get_data_from_file(3)
    data = [sorted(triangle) for triangle in data]
    pos_triangles = sum([side[0] + side[1] > side[2] for side in data])
    return pos_triangles

def check_triangle_2():
    '''
    See description.
    '''
    data = get_data_from_file(3)
    new_triangles = []
    for x in range(0, len(data), 3):
        three_new_triangles = zip(*data[x:x+3])
        new_triangles.extend(three_new_triangles)
    data = [sorted(triangle) for triangle in new_triangles]
    pos_triangles = sum([side[0] + side[1] > side[2] for side in data])
    return pos_triangles

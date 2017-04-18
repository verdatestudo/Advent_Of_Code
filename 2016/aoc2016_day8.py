
'''
Advent of Code - 2016 - Day 8
http://adventofcode.com/2016

Last Updated: 2017-Jan-08
First Created: 2017-Jan-08
Python 3.5
Chris

--- Day 8: Two-Factor Authentication ---

You come across a door implementing what you can only assume is an implementation of two-factor authentication after a long game of requirements telephone.

To get past the door, you first swipe a keycard (no problem; there was one on a nearby desk).
Then, it displays a code on a little screen, and you type that code on a keypad. Then, presumably, the door unlocks.

Unfortunately, the screen has been smashed. After a few minutes, you've taken everything apart and figured out how it works.
Now you just have to work out what the screen would have displayed.

The magnetic strip on the card you swiped encodes a series of instructions for the screen; these instructions are your puzzle input.
The screen is 50 pixels wide and 6 pixels tall, all of which start off, and is capable of three somewhat peculiar operations:

    rect AxB turns on all of the pixels in a rectangle at the top-left of the screen which is A wide and B tall.
    rotate row y=A by B shifts all of the pixels in row A (0 is the top row) right by B pixels. Pixels that would fall off the right end appear at the left end of the row.
    rotate column x=A by B shifts all of the pixels in column A (0 is the left column) down by B pixels. Pixels that would fall off the bottom appear at the top of the column.

For example, here is a simple sequence on a smaller screen:

    rect 3x2 creates a small rectangle in the top-left corner:

    ###....
    ###....
    .......

    rotate column x=1 by 1 rotates the second column down by one pixel:

    #.#....
    ###....
    .#.....

    rotate row y=0 by 4 rotates the top row right by four pixels:

    ....#.#
    ###....
    .#.....

    rotate column x=1 by 1 again rotates the second column down by one pixel, causing the bottom pixel to wrap back to the top:

    .#..#.#
    #.#....
    .#.....

As you can see, this display technology is extremely powerful, and will soon dominate the tiny-code-displaying-screen market.
That's what the advertisement on the back of the display tries to convince you, anyway.

There seems to be an intermediate check of the voltage used by the display: after you swipe your card, if the screen did work, how many pixels should be lit?

To begin, get your puzzle input.

--- Part Two ---

You notice that the screen is only capable of displaying capital letters; in the font it uses, each letter is 5 pixels wide and 6 tall.

After you swipe your card, what code is the screen trying to display?

'''

import re

class grid():

    def __init__(self, height, width):
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.height = height
        self.width = width

    def convert_and_apply_commands(self, line):
        a, b = map(int, re.findall('(\d+)', line))
        if line[0:4] == 'rect':
            self.rect(b, a)
        else:
            if line[7:10] == 'col':
                self.rotate_col(a, b)
            elif line[7:10] == 'row':
                self.rotate_row(a, b)
            else:
                print('error')

    def rect(self, height, width):
        for row in range(height):
            for col in range(width):
                self.grid[row][col] = 1

    def rotate_row(self, row_no, distance):
        indices = [(i + distance) % self.width for i, x in enumerate(self.grid[row_no]) if x == 1]
        new_row = [1 if x in indices else 0 for x in range(self.width)]
        self.grid[row_no] = new_row

    def rotate_col(self, col_no, distance):
        indices = [(row_no + distance) % self.height for row_no in range(self.height) if self.grid[row_no][col_no] == 1]
        for row_no in range(self.height):
            if row_no in indices:
                self.grid[row_no][col_no] = 1
            else:
                self.grid[row_no][col_no] = 0

    def show(self):
        print('---')
        for row in self.grid:
            print(row)
        print('---')

    def sum_on(self):
        return sum([sum(x) for x in self.grid])


def get_data(filename):
    with open(filename, 'r') as input_file:
        return [line.strip() for line in input_file]

def test_grid():
    test_grid = grid(3, 7)
    test_data = ['rect 3x2', 'rotate column x=1 by 1', 'rotate row y=0 by 40', 'rotate column x=1 by 1']

    for line in test_data:
        print(line)
        test_grid.convert_and_apply_commands(line)
        test_grid.show()

def problem():
    data = get_data('aoc2016_day8.txt')

    grid1 = grid(6, 50)

    for line in data:
        print(line)
        grid1.convert_and_apply_commands(line)
        grid1.show()

    print(grid1.sum_on(), 106)

    for y in range(0, grid1.width, 5):
        for x in range(grid1.height):
            print(grid1.grid[x][y: y + 5])
        print('\n')

    print('Code is: CFLELOYFCS')

# test_grid()
# problem()


'''
Advent of Code - 2016 - Day 10
http://adventofcode.com/2016

Last Updated: 2017-Feb-03
First Created: 2017-Jan-08
Python 3.5
Chris

--- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around handing small microchips to each other.

Upon closer examination, you notice that each bot only proceeds when it has two microchips, and once it does,
it gives each one to a different bot or puts it in a marked "output" bin. Sometimes, bots take microchips from "input" bins, too.

Inspecting one of the microchips, it seems like they each contain a single number; the bots must use some logic to decide what to do with each chip.
You access the local control computer and download the bots' instructions (your puzzle input).

Some of the instructions specify that a specific-valued microchip should be given to a specific bot; the rest of the instructions indicate what a given bot should do with its lower-value or higher-value chip.

For example, consider the following instructions:

value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2

    Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2 chip and a value-5 chip.
    Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
    Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and gives the value-3 chip to bot 0.
    Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in output 0.

In the end, output bin 0 contains a value-5 microchip, output bin 1 contains a value-2 microchip, and output bin 2 contains a value-3 microchip.
In this configuration, bot number 2 is responsible for comparing value-5 microchips with value-2 microchips.

Based on your instructions, what is the number of the bot that is responsible for comparing value-61 microchips with value-17 microchips?

To begin, get your puzzle input.

--- Part Two ---

What do you get if you multiply together the values of one chip in each of outputs 0, 1, and 2?


'''

import re
from collections import defaultdict

def get_data():
    with open('aoc2016_day10.txt', 'r') as input_file:
        instructions = input_file.read()
        bot_take = re.findall(r'value (\d+) goes to (\w+ \d+)', instructions)
        bot_instruct = {a: (b, c) for a, b, c in re.findall(r'(\w+ \d+) gives low to (\w+ \d+) and high to (\w+ \d+)', instructions)}
        return bot_instruct, bot_take

def move_chip(giver, taker, chip):
    '''
    Takes two strings giver and taker and an int chip.
    Giver is the bot (else 'bin') giving a chip to taker.
    If this then means the taker bot has two chips, we can then carry out it's instructions recursively.
    '''
    bots[taker].append(chip)
    if len(bots[taker]) > 1:
        b = bots[taker]
        chips = b.pop(b.index(min(b))), b.pop(b.index(max(b))) # pop min and max chips from taker (which is now the new giver)
        if chips == (17, 61):
            print('This bot is the answer to part one: {} ... (should equal bot 56)'.format(taker))
        move_chip(taker, bot_instruct[taker][0], chips[0])
        move_chip(taker, bot_instruct[taker][1], chips[1])

bot_instruct, bot_take = get_data()
bots = defaultdict(list)

for chip, bot_no in bot_take:
    move_chip('bin', bot_no, int(chip))

ans2 = bots['output 0'][0] * bots['output 1'][0] * bots['output 2'][0]
print('Part 2 answer: {} ... (should equal 7847)'.format(ans2))

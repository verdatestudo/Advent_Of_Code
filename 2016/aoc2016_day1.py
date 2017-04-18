
'''
Advent of Code - 2016 - Day 1
http://adventofcode.com/2016

Last Updated: 2016-Dec-26
First Created: 2016-Dec-26
Python 3.5
Chris

--- Day 1: No Time for a Taxicab ---

Santa's sleigh uses a very high-precision clock to guide its movements, and the clock's oscillator is regulated by stars.
Unfortunately, the stars have been stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the advent calendar;
the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", unfortunately, is as close as you can get -
the instructions on the Easter Bunny Recruiting Document the Elves intercepted start here, and nobody had time to work them out further.

The Document indicates that you should start at the given coordinates (where you just landed) and face North.
Then, follow the provided sequence: either turn left (L) or right (R) 90 degrees, then walk forward the given number of blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you take a moment and work out the destination.
Given that you can only walk on the street grid of the city, how far is the shortest path to the destination?

For example:

    Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
    R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
    R5, L5, R5, R3 leaves you 12 blocks away.

How many blocks away is Easter Bunny HQ?

--- Part Two ---

Then, you notice the instructions continue on the back of the Recruiting Document. Easter Bunny HQ is actually at the first location you visit twice.

For example, if your instructions are R8, R4, R4, R8, the first location you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?

'''

def easter_bunny_hq(input_string):
    '''
    See description above.
    (Better solution would be using complex numbers to rotate by 90, as per Norvig solution.)
    '''
    directions = {1: (0, 1), 2: (1, 0), 3: (0, -1), 4: (-1, 0)} # clockwise directions, 1 = N, 2 = E, 3 = S, 4 = W
    current_direction = 1 # start facing North

    input_directions = input_string.split(', ')

    final_position = [0, 0]

    for item in input_directions:
        if item[0] == 'L':
            current_direction -= 1
        else:
            current_direction += 1
        current_direction = (current_direction % 4) or 4

        move = list(map(lambda x: int(item[1:]) * x, directions[current_direction]))
        new_position = [sum(x) for x in zip(final_position, move)]

        final_position = new_position

    return (final_position, abs(final_position[0]) + abs(final_position[1]))

def easter_bunny_hq_2(input_string):
    '''
    See description above.
    '''
    directions = {1: (0, 1), 2: (1, 0), 3: (0, -1), 4: (-1, 0)} # clockwise directions, 1 = N, 2 = E, 3 = S, 4 = W
    current_direction = 1 # start facing North

    input_directions = input_string.strip().split(', ')

    final_position = [0, 0]
    visited = [[0, 0]]

    for item in input_directions:
        if item[0] == 'L':
            current_direction -= 1
        else:
            current_direction += 1
        current_direction = (current_direction % 4) or 4

        for _ in range(int(item[1:])):
            final_position = [sum(x) for x in zip(final_position, directions[current_direction])]
            if final_position not in visited:
                visited.append(final_position)
            else:
                return (final_position, abs(final_position[0]) + abs(final_position[1]))

    return 'No match'

def easter_bunny_hq_testing():
    '''
    Testing
    '''
    print(easter_bunny_hq('R2, L3'), 5)
    print(easter_bunny_hq('R2, R2, R2'), 2)
    print(easter_bunny_hq('R5, L5, R5, R3'), 12)

    print(easter_bunny_hq(input_string), 'Correct answer: 252')
    print(easter_bunny_hq_2(input_string), 'Correct answer: 143')

input_string = 'L3, R1, L4, L1, L2, R4, L3, L3, R2, R3, L5, R1, R3, L4, L1, L2, R2, R1, L4, L4, R2, L5, R3, R2, R1, L1, L2, R2, R2, '\
'L1, L1, R2, R1, L3, L5, R4, L3, R3, R3, L5, L190, L4, R4, R51, L4, R5, R5, R2, L1, L3, R1, R4, L3, R1, R3, L5, L4, R2, R5, R2, L1, '\
'L5, L1, L1, R78, L3, R2, L3, R5, L2, R2, R4, L1, L4, R1, R185, R3, L4, L1, L1, L3, R4, L4, L1, R5, L5, L1, R5, L1, R2, L5, L2, R4, '\
'R3, L2, R3, R1, L3, L5, L4, R3, L2, L4, L5, L4, R1, L1, R5, L2, R4, R2, R3, L1, L1, L4, L3, R4, L3, L5, R2, L5, L1, L1, R2, R3, L5, '\
'L3, L2, L1, L4, R4, R4, L2, R3, R1, L2, R1, L2, L2, R3, R3, L1, R4, L5, L3, R4, R4, R1, L2, L5, L3, R1, R4, L2, R5, R4, R2, L5, L3, '\
'R4, R1, L1, R5, L3, R1, R5, L2, R1, L5, L2, R2, L2, L3, R3, R3, R1'

easter_bunny_hq_testing()

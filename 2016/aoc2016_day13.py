'''
Advent of Code - 2016 - Day 13
http://adventofcode.com/2016

Last Updated: 2017-Feb-22
First Created: 2017-Feb-22
Python 3.5
Chris

--- Day 13: A Maze of Twisty Little Cubicles ---

You arrive at the first floor of this new building to discover a much less welcoming environment than the shiny atrium of the last one.
Instead, you are in a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative integers (x,y).
Each such coordinate is either a wall or an open space. You can't move diagonally.
The cube maze starts at 0,0 and seems to extend infinitely toward positive x and y;
negative values are invalid, as they represent a location outside the building.
You are in a small waiting area at 1,1.

While it seems chaotic, a nearby morale-boosting poster explains, the layout is actually quite logical.
You can determine whether a given x,y coordinate will be a wall or an open space using a simple system:

    Find x*x + 3*x + 2*x*y + y + y*y.
    Add the office designer's favorite number (your puzzle input).
    Find the binary representation of that sum; count the number of bits that are 1.
        If the number of bits that are 1 is even, it's an open space.
        If the number of bits that are 1 is odd, it's a wall.

For example, if the office designer's favorite number were 10, drawing walls as # and open spaces as .,
the corner of the building containing 0,0 would look like this:

  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###

Now, suppose you wanted to reach 7,4. The shortest route you could take is marked as O:

  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###

Thus, reaching 7,4 would take a minimum of 11 steps (starting from your current location, 1,1).

What is the fewest number of steps required for you to reach 31,39?

Your puzzle input is 1350.

Your puzzle answer was 92.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?

Your puzzle answer was 124.

Both parts of this puzzle are complete! They provide two gold stars: **
'''

import heapq

###

def Path(previous, s):
    return ([] if s is None else Path(previous, previous[s]) + [s])

def astar_search(start, h_func, moves_func):
    frontier = [(h_func(start), start)]
    previous = {start: None}
    path_cost = {start: 0}

    while frontier:
        f, s = heapq.heappop(frontier)
        if h_func(s) == 0:
            return Path(previous, s)
        else:
            for s2 in moves_func(s):
                new_cost = path_cost[s] + 1
                if s2 not in path_cost or new_cost < path_cost[s]:
                    heapq.heappush(frontier, (new_cost + h_func(s2), s2))
                    previous[s2] = s
                    path_cost[s2] = new_cost

    return False

###

def h_func(current_position):
    return sum(tuple(abs(a - b) for a, b in zip(current_position, GOAL_POSITION)))

def moves_func(current_position):
    moves = ((-1, 0), (1, 0), (0, 1), (0, -1))
    possible_moves = [tuple((a + b) for a, b in zip(current_position, move)) for move in moves]
    return [move for move in possible_moves if is_space(*move)]

def is_space(x, y):
    if x < 0 or y < 0:
        return False
    else:
        value = (x * x) + (3 * x) + (2 * x * y) + (y) + (y * y) + (PUZZLE_INPUT)
        return not bin(value).count('1') % 2

def gen_grid(size):
    return [[is_space(x, y) for y in range(size)] for x in range(size)]

def write_grid(grid):
    '''
    Function to write a visual representation of a grid to txt file.
    '''
    with open('aoc2016_day13_grid.txt', 'w') as f:
        for row in grid:
            f.write(' '.join(['@' if x else '#' for x in row]) + '\n')

###

### test start ###
PUZZLE_INPUT = 10
GOAL_POSITION = (7, 4)
start_pos = (1, 1)

ans = astar_search(start_pos, h_func, moves_func)
print(ans)
print('Number of moves: {}'.format(len(ans) - 1)) # don't include start position in moves.
### test end ###

### part one start ###
PUZZLE_INPUT = 1350
GOAL_POSITION = (31, 39)
start_pos = (1, 1)

ans = astar_search(start_pos, h_func, moves_func)
print(ans)
print('Number of moves: {}'.format(len(ans) - 1)) # don't include start position in moves.
### part one end ###

### part two start ###

PUZZLE_INPUT = 1350
start_pos = (1, 1)
goal_moves = 50

def goal_positions(start_pos, goal_moves):
    '''
    start_pos is a tuple of x, y start co-ordinates, goal_moves is the maximum
    number of moves allowed to reach a unique grid position.

    This generator function yields a *potential* goal position if it would take
    less than goal_moves to reach and the goal position is not a wall.

    For example with start_pos = (1, 1) and goal_moves = 10 then obviously (20, 10) cannot be reached.

    Note: second method is faster.
    '''
    for x in range(goal_moves + start_pos[1] + 1):
        for y in range(goal_moves + start_pos[0] + 1 - x):
            if is_space(x, y): yield(x, y)

results = []
for GOAL_POSITION in goal_positions(start_pos, goal_moves):
    ans = astar_search(start_pos, h_func, moves_func)
    if ans and len(ans) - 1 <= goal_moves: # don't include start position in steps
        results.append(GOAL_POSITION)

print(results)
print(len(results))

### part two end ###

### part two second method start ###

PUZZLE_INPUT = 1350
start_pos = (1, 1)
goal_moves = 50

def part_two(start, goal_moves, moves_func):
    '''
    Explore all neighbors of locations while traversing through grid.
    Only add to distance if not previously explored and it's less than goal moves. 
    '''
    frontier = [(start)]
    distance = {start: 0}
    while frontier:
        s = frontier.pop()
        if distance[s] < goal_moves:
            for s2 in moves_func(s):
                if s2 not in distance:
                    frontier.append(s2)
                    distance[s2] = distance[s] + 1
    print(distance)
    return(len(distance))

print(part_two(start_pos, goal_moves, moves_func))

### part two second method end ###

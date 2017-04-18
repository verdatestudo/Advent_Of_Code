'''

Advent of Code - 2016 - Day 24
http://adventofcode.com/2016

Last Updated: 2017-Apr-12
First Created: 2017-Apr-10
Python 3.6
Chris

--- Day 24: Air Duct Spelunking ---

You've finally met your match; the doors that provide access to the roof are locked tight,
and all of the controls and related electronics are inaccessible. You simply can't reach them.

The robot that cleans the air ducts, however, can.

It's not a very fast little robot, but you reconfigure it to be able to interface with some of the exposed wires that have been routed through the HVAC system.
If you can direct it to each of those locations, you should be able to bypass the security controls.

You extract the duct layout for this area from some blueprints you acquired and create a map with the relevant locations marked (your puzzle input).
0 is your current location, from which the cleaning robot embarks; the other numbers are (in no particular order) the locations the robot needs to visit at least once each.
Walls are marked as #, and open passages are marked as .. Numbers behave like open passages.

For example, suppose you have a map like the following:

###########
#0.1.....2#
#.#######.#
#4.......3#
###########

To reach all of the points of interest as quickly as possible, you would have the robot take the following path:

    0 to 4 (2 steps)
    4 to 1 (4 steps; it can't move diagonally)
    1 to 2 (6 steps)
    2 to 3 (2 steps)

Since the robot isn't very fast, you need to find it the shortest route.
This path is the fewest steps (in the above example, a total of 14) required to start at 0 and then visit every other location at least once.

Given your actual map, and starting from location 0, what is the fewest number of steps required to visit every non-0 number marked on the map at least once?

Your puzzle answer was 490.
--- Part Two ---

Of course, if you leave the cleaning robot somewhere weird, someone is bound to notice.

What is the fewest number of steps required to start at 0, visit every non-0 number marked on the map at least once, and then return to 0?

Your puzzle answer was 744.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

import heapq
from collections import namedtuple

def get_data(filename):
    conversion = {'#': 0, '.': 1}
    grid = []
    goal_locations = {}
    with open(filename) as f:
        for idx, line in enumerate(f):
            for col_no, item in enumerate(line.strip()):
                if item not in conversion:
                    goal_locations[item] = (idx, col_no)
            grid.append([conversion[x] if x in conversion else str(x) for x in line.strip()])
    return grid, goal_locations

def moves_func(state, grid):
    goal_locations = dict(state.goal_locations)
    moves = {(state.x + 1, state.y), (state.x - 1, state.y),
            (state.x, state.y + 1), (state.x, state.y - 1)
            }
    for x, y in moves:
        if grid[x][y]:
            if (x, y) in goal_locations.values():
                new_goal_locations = goal_locations.copy()
                new_goal_locations.pop(grid[x][y])
                yield(State(x, y, frozenset(new_goal_locations.items())))
            else:
                yield(State(x, y, state.goal_locations))

def h_func(state):
    goal_locations = dict(state.goal_locations)
    estimated_distance = sum([(abs(state.x - x) + abs(state.y - y)) \
                            for x, y in goal_locations.values()])
    return estimated_distance

def h_func_part_two(state):
    goal_locations = dict(state.goal_locations)
    estimated_distance = sum([(abs(state.x - x) + abs(state.y - y)) \
                            for x, y in goal_locations.values()]) \
                            + (abs(state.x - start_x) + abs(state.y - start_y))
    return estimated_distance

def Path(previous, state):
    return ([] if state is None else Path(previous, previous[state]) + [state])

def astar_search(start, h_func, moves_func, grid):
    frontier = [(h_func(start), start)]
    previous = {start: None}
    path_cost = {start: 0}

    answers = []

    while frontier:
        (f, s) = heapq.heappop(frontier)
        print('Distance to goal: {}'.format(h_func(s)))
        if h_func(s) == 0:
            answers.append(Path(previous, s))
        else:
            for s2 in moves_func(s, grid):
                new_cost = path_cost[s] + 1
                if s2 not in path_cost or new_cost < path_cost[s2]:
                    heapq.heappush(frontier, (h_func(s2) + new_cost, s2))
                    previous[s2] = s
                    path_cost[s2] = new_cost

    return answers # 'No path found'


# grid, goal_locations = get_data(filename='aoc2016_day24_test.txt')
grid, goal_locations = get_data('aoc2016_day24.txt')
State = namedtuple('State', ['x', 'y', 'goal_locations'])
start_x, start_y = goal_locations.pop('0')

# can freeze dict for hashing purposes, then unfreeze when need to access the data,
# then refreeze for hashing purposes, and so on.
start_state = State(start_x, start_y, frozenset(goal_locations.items()))

ans1 = astar_search(start_state, h_func, moves_func, grid)
ans1_len = len(min(ans1, key=len)) - 1 # remove starting square

ans2 = astar_search(start_state, h_func_part_two, moves_func, grid)
ans2_len = len(min(ans2, key=len)) - 1 # remove starting square

print(ans1_len, ans1_len == 490)
print(ans2_len, ans2_len == 744)

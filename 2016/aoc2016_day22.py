'''

Advent of Code - 2016 - Day 22
http://adventofcode.com/2016

Last Updated: 2017-Apr-18
First Created: 2017-Mar-13
Python 3.5
Chris

--- Day 22: Grid Computing ---

You gain access to a massive storage cluster arranged in a grid;
each storage node is only connected to the four nodes directly adjacent to it (three if the node is on an edge, two if it's in a corner).

You can directly access data only on node /dev/grid/node-x0-y0, but you can perform some limited actions on the other nodes:

    You can get the disk usage of all nodes (via df). The result of doing this is in your puzzle input.
    You can instruct a node to move (not copy) all of its data to an adjacent node (if the destination node has enough space to receive the data).
    The sending node is left empty after this operation.

Nodes are named by their position: the node named node-x10-y10 is adjacent to nodes node-x9-y10, node-x11-y10, node-x10-y9, and node-x10-y11.

Before you begin, you need to understand the arrangement of data on these nodes.
Even though you can only move data between directly connected nodes, you're going to need to rearrange a lot of the data to get access to the data you need.
Therefore, you need to work out how you might be able to shift data around.

To do this, you'd like to count the number of viable pairs of nodes. A viable pair is any two nodes (A,B), regardless of whether they are directly connected, such that:

    Node A is not empty (its Used is not zero).
    Nodes A and B are not the same node.
    The data on node A (its Used) would fit on node B (its Avail).

How many viable pairs of nodes are there?

Your puzzle answer was 955.

--- Part Two ---

Now that you have a better understanding of the grid, it's time to get to work.

Your goal is to gain access to the data which begins in the node with y=0 and the highest x (that is, the node in the top-right corner).

For example, suppose you have the following grid:

Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%

In this example, you have a storage grid 3 nodes wide and 3 nodes tall. The node you can access directly, node-x0-y0, is almost full. The node containing the data you want to access, node-x2-y0 (because it has y=0 and the highest x value), contains 6 terabytes of data - enough to fit on your node, if only you could make enough space to move it there.

Fortunately, node-x1-y1 looks like it has enough free space to enable you to move some of this data around. In fact, it seems like all of the nodes have enough space to hold any node's data (except node-x0-y2, which is much larger, very full, and not moving any time soon). So, initially, the grid's capacities and connections look like this:

( 8T/10T) --  7T/ 9T -- [ 6T/10T]
    |           |           |
  6T/11T  --  0T/ 8T --   8T/ 9T
    |           |           |
 28T/32T  --  7T/11T --   6T/ 9T

The node you can access directly is in parentheses; the data you want starts in the node marked by square brackets.

In this example, most of the nodes are interchangable: they're full enough that no other node's data would fit, but small enough that their data could be moved around. Let's draw these nodes as .. The exceptions are the empty node, which we'll draw as _, and the very large, very full node, which we'll draw as #. Let's also draw the goal data as G. Then, it looks like this:

(.) .  G
 .  _  .
 #  .  .

The goal is to move the data in the top right, G, to the node in parentheses. To do this, we can issue some commands to the grid and rearrange the data:

    Move data from node-y0-x1 to node-y1-x1, leaving node node-y0-x1 empty:

    (.) _  G
     .  .  .
     #  .  .

    Move the goal data from node-y0-x2 to node-y0-x1:

    (.) G  _
     .  .  .
     #  .  .

    At this point, we're quite close. However, we have no deletion command, so we have to move some more data around. So, next, we move the data from node-y1-x2 to node-y0-x2:

    (.) G  .
     .  .  _
     #  .  .

    Move the data from node-y1-x1 to node-y1-x2:

    (.) G  .
     .  _  .
     #  .  .

    Move the data from node-y1-x0 to node-y1-x1:

    (.) G  .
     _  .  .
     #  .  .

    Next, we can free up space on our node by moving the data from node-y0-x0 to node-y1-x0:

    (_) G  .
     .  .  .
     #  .  .

    Finally, we can access the goal data by moving the it from node-y0-x1 to node-y0-x0:

    (G) _  .
     .  .  .
     #  .  .

So, after 7 steps, we've accessed the data we want. Unfortunately, each of these moves takes time, and we need to be efficient:

What is the fewest number of steps required to move your goal data to node-x0-y0?

Your puzzle answer was 246.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

import re
from collections import namedtuple
import copy
import heapq
import csv

def get_data_part_one(filename='aoc2016_day22.txt'):
    Node_Data = namedtuple('Node_Data', ['x', 'y', 'size', 'used', 'avail', 'use_pct'])

    with open(filename, 'r') as f:
        nodes = [Node_Data(*[int(x) for x in re.findall(r'\d+', line)])
                for line in f
                if line.startswith('/dev')
                ]

    return nodes

def part_one(nodes):
    # solution one
    viable_count = sum([1 for nodeB in nodes for nodeA in nodes if nodeA != nodeB and 0 < nodeA.used <= nodeB.avail])
    return viable_count

    # solution two
    # used_nodes = sorted(nodes, key=lambda x: x.used)
    # avail_nodes = sorted(nodes, key=lambda x: x.avail, reverse=True)
    #
    # total_viable_nodes = sum([(0 < used_node.used <= avail_nodes[0].avail) for used_node in used_nodes])
    # return total_viable_nodes

    # solution three
    # used_nodes = sorted(nodes, key=lambda x: x.used)
    # avail_nodes = sorted(nodes, key=lambda x: x.avail, reverse=True)
    # total_viable_nodes = 0
    # for avail_node in avail_nodes:
    #     viable_nodes = sum([(0 < used_node.used <= avail_node.avail) for used_node in used_nodes])
    #
    #     # as lists are sorted, once we reach an avail node which has no room to take data from any nodes,
    #     # we can stop the iteration early.
    #     if viable_nodes:
    #         total_viable_nodes += viable_nodes
    #     else:
    #         break
    # return total_viable_nodes


def part_two(nodes):
    """
    Two parts to this solution.
    1: Move from starting position to position directly left of the very top-right (using Astar).
    2: Similar to a 15-puzzle, then repeat the same set of moves until moved to finishing position at top-left.

    (e.g we are at P, and T is our target - this is the set of five moves we can use repeatedly)

    x P T | x T P | x T x | x T x | x T x | P T x |
    x x x | x x x | x x P | x P x | P x x | x x x |

    """

    start_x, start_y = next(((node.x, node.y) for node in nodes if node.use_pct == 0), None)
    start_state = State(start_x, start_y)

    top_right_node = max(nodes, key=lambda k: k.x)
    goal_state = State(top_right_node.x - 1, 0) # we want the location to the left of the top-right, and y=0

    node_grid = {(node.x, node.y): 1 if node.use_pct < 90 else 0 for node in nodes}

    moves = astar_search(start_state, h_func, moves_func, node_grid, goal_state)

    moves_1 = len(moves) - 1 # minus one as we don't need to include start position in number of moves
    moves_2 = (goal_state.x * 5) + 1 # add one as we'll be at 0,0 and our target is at 1,0, so need to move the target to 0,0

    return moves_1 + moves_2

def Path(previous, state):
    return ([] if state is None else Path(previous, previous[state]) + [state])

def h_func(state, goal_state):
    return abs(state.x - goal_state.x) + abs(state.y - goal_state.y)

def moves_func(state, nodes):
    possible_neighbors = ((state.x - 1, state.y),
                          (state.x + 1, state.y),
                          (state.x, state.y - 1),
                          (state.x, state.y + 1),
                          )

    for nebor_x, nebor_y in possible_neighbors:
        if nodes.get((nebor_x, nebor_y), None):
            yield State(nebor_x, nebor_y)

def astar_search(start, h_func, moves_func, nodes, goal_state):
    frontier = [(h_func(start, goal_state), start)]
    previous = {start: None}
    path_cost = {start: 0}

    while frontier:
        (f, s) = heapq.heappop(frontier)
        if h_func(s, goal_state) == 0:
            return Path(previous, s)
        for s2 in moves_func(s, nodes):
            new_cost = path_cost[s] + 1
            if s2 not in path_cost or new_cost < path_cost[s2]:
                heapq.heappush(frontier, (h_func(s2, goal_state) + new_cost, s2))
                previous[s2] = s
                path_cost[s2] = new_cost

def write_to_grid(nodes):
    """ Create a visual representation of grid in csv file """

    max_x = max(nodes, key=lambda k: k.x).x
    max_y = max(nodes, key=lambda k: k.y).y

    file_grid = [['' for _ in range(max_x)] for _ in range(max_y)]

    for node in nodes:
        # y and x need to be flipped
        # position is passable if use_pct < 90, using 1 or 0
        file_grid[node.y - 1][node.x - 1] = int(node.use_pct < 90)

        # starting position
        if node.use_pct == 0:
            file_grid[node.y - 1][node.x - 1] = 9

    with open('day22_grid.csv','w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(file_grid)

    return None

nodes = get_data_part_one()

# write_to_grid(nodes)

ans1 = part_one(nodes)
print(ans1, ans1 == 955)

State = namedtuple('State', ['x', 'y'])

ans2 = part_two(nodes)
print(ans2, ans2 == 246)

'''
Advent of Code - 2016 - Day 17
http://adventofcode.com/2016

Last Updated: 2017-Feb-25
First Created: 2017-Feb-24
Python 3.5
Chris

--- Day 17: Two Steps Forward ---

You're trying to access a secure vault protected by a 4x4 grid of small rooms connected by doors.
You start in the top-left room (marked S), and you can access the vault (marked V) once you reach the bottom-right room:

#########
#S| | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | |
####### V

Fixed walls are marked with #, and doors are marked with - or |.

The doors in your current room are either open or closed (and locked) based on the hexadecimal MD5 hash of a passcode (your puzzle input)
followed by a sequence of uppercase characters representing the path you have taken so far (U for up, D for down, L for left, and R for right).

Only the first four characters of the hash are used; they represent, respectively, the doors up, down, left, and right from your current position.
Any b, c, d, e, or f means that the corresponding door is open;
any other character (any number or a) means that the corresponding door is closed and locked.

To access the vault, all you need to do is reach the bottom-right room; reaching this room opens the vault and all doors in the maze.

For example, suppose the passcode is hijkl.
Initially, you have taken no steps, and so your path is empty: you simply find the MD5 hash of hijkl alone.
The first four characters of this hash are ced9, which indicate that up is open (c), down is open (e), left is open (d), and right is closed and locked (9).
Because you start in the top-left corner, there are no "up" or "left" doors to be open, so your only choice is down.

Next, having gone only one step (down, or D), you find the hash of hijklD.
This produces f2bc, which indicates that you can go back up, left (but that's a wall), or right.
Going right means hashing hijklDR to get 5745 - all doors closed and locked.
However, going up instead is worthwhile: even though it returns you to the room you started in, your path would then be DU, opening a different set of doors.

After going DU (and then hashing hijklDU to get 528e), only the right door is open; after going DUR, all doors lock. (Fortunately, your actual passcode is not hijkl).

Passcodes actually used by Easter Bunny Vault Security do allow access to the vault if you know the right path. For example:

    If your passcode were ihgpwlah, the shortest path would be DDRRRD.
    With kglvqrro, the shortest path would be DDUDRLRRUDRD.
    With ulqzkmiv, the shortest would be DRURDRUDDLLDLUURRDULRLDUUDDDRR.

Given your vault's passcode, what is the shortest path (the actual path, not just the length) to reach the vault?

Your puzzle input is pxxbnzuo.

Your puzzle answer was RDULRDDRRD.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

You're curious how robust this security solution really is, and so you decide to find longer and longer paths which still provide access to the vault.
You remember that paths always end the first time they reach the bottom-right room (that is, they can never pass through it, only end in it).

For example:

    If your passcode were ihgpwlah, the longest path would take 370 steps.
    With kglvqrro, the longest path would be 492 steps long.
    With ulqzkmiv, the longest path would be 830 steps long.

What is the length of the longest path that reaches the vault?

Your puzzle answer was 752.

Both parts of this puzzle are complete! They provide two gold stars: **


'''
import hashlib
import heapq
from collections import namedtuple


def astar_search(start, h_func, moves_func):
    '''
    Checks ALL paths that reach goal state.
    Returns smallest path directions (e.g UURLDU) and longest path length (e.g 370).
    '''
    frontier = [(h_func(start), start)]
    path_cost = {start: 0}
    ans = []

    while frontier:
        f, s = heapq.heappop(frontier)
        if h_func(s) == 0:
            ans.append(s.data_hash[len(start.data_hash):])
        else:
            new_cost = path_cost[s] + 1
            for s2 in moves_func(s):
                if s2 not in path_cost or new_cost < path_cost[s2]:
                    heapq.heappush(frontier, (h_func(s2) + new_cost, s2))
                    path_cost[s2] = new_cost

    try:
        return min(ans, key=len), len(max(ans, key=len))
    except ValueError:
        return 'Fail'


def find_md5_hash(data):
    '''
    Find md5 hash of puzzle_input + moves_dict, and return first four chars.
    '''
    return hashlib.md5(data.encode('utf-8')).hexdigest()[:4]

def moves_func(state, grid_size=4):
    '''
    First four chars of hash represent UP DOWN LEFT RIGHT.
    If char is b, c, d, e, f AND fits within the walls (represented by 4x4 grid), door is open.
    '''
    open_door_digits = 'bcdef'
    directions = (('U', (0, -1)), ('D', (0, 1)), ('L', (-1, 0)), ('R', (1, 0)))

    new_data_hash = find_md5_hash(state.data_hash)

    for idx, digit in enumerate(new_data_hash):
        # x, y = state.position
        # dx, dy = directions[idx][1]
        # new_position = (x + dx, y + dy)
        new_position = tuple((sum(x) for x in zip(state.position, directions[idx][1])))
        if digit in open_door_digits and all(0 <= x < grid_size for x in new_position):
            yield State(new_position, state.data_hash + directions[idx][0])

def h_func(state, goal=(3, 3)):
    return sum(abs(x - y) for x, y in zip(state.position, goal))


State = namedtuple('State', ['position', 'data_hash'])

print(astar_search(State((0, 0), 'hijkl'), h_func, moves_func), 'Fail')
print(astar_search(State((0, 0), 'ihgpwlah'), h_func, moves_func), 'DDRRRD', 370)
print(astar_search(State((0, 0), 'kglvqrro'), h_func, moves_func), 'DDUDRLRRUDRD', 492)
print(astar_search(State((0, 0), 'ulqzkmiv'), h_func, moves_func), 'DRURDRUDDLLDLUURRDULRLDUUDDDRR', 830)
print(astar_search(State((0, 0), 'pxxbnzuo'), h_func, moves_func), 'RDULRDDRRD', 752)

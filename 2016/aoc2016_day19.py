'''
Advent of Code - 2016 - Day 19
http://adventofcode.com/2016

Last Updated: 2017-Mar-03
First Created: 2017-Feb-25
Python 3.5
Chris

--- Day 19: An Elephant Named Joseph ---

The Elves contact you over a highly secure emergency channel.
Back at the North Pole, the Elves are busy misunderstanding White Elephant parties.

Each Elf brings a present. They all sit in a circle, numbered starting with position 1.
Then, starting with the first Elf, they take turns stealing all the presents from the Elf to their left.
An Elf with no presents is removed from the circle and does not take turns.

For example, with five Elves (numbered 1 to 5):

  1
5   2
 4 3

    Elf 1 takes Elf 2's present.
    Elf 2 has no presents and is skipped.
    Elf 3 takes Elf 4's present.
    Elf 4 has no presents and is also skipped.
    Elf 5 takes Elf 1's two presents.
    Neither Elf 1 nor Elf 2 have any presents, so both are skipped.
    Elf 3 takes Elf 5's three presents.

So, with five Elves, the Elf that sits starting in position 3 gets all the presents.

With the number of Elves given in your puzzle input, which Elf gets all the presents?

Your puzzle input is 3018458.

Your puzzle answer was 1842613.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

Realizing the folly of their present-exchange rules, the Elves agree to instead steal presents from the Elf directly across the circle.
If two Elves are across the circle, the one on the left (from the perspective of the stealer) is stolen from.
The other rules remain unchanged: Elves with no presents are removed from the circle entirely, and the other elves move in slightly to keep the circle evenly spaced.

For example, with five Elves (again numbered 1 to 5):

    The Elves sit in a circle; Elf 1 goes first:

      1
    5   2
     4 3

    Elves 3 and 4 are across the circle; Elf 3's present is stolen, being the one to the left. Elf 3 leaves the circle, and the rest of the Elves move in:

      1           1
    5   2  -->  5   2
     4 -          4

    Elf 2 steals from the Elf directly across the circle, Elf 5:

      1         1
    -   2  -->     2
      4         4

    Next is Elf 4 who, choosing between Elves 1 and 2, steals from Elf 1:

     -          2
        2  -->
     4          4

    Finally, Elf 2 steals from Elf 4:

     2
        -->  2
     -

So, with five Elves, the Elf that sits starting in position 2 gets all the presents.

With the number of Elves given in your puzzle input, which Elf now gets all the presents?

Your puzzle answer was 1424135.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

from collections import deque
from timeit import default_timer as timer

def timedec(func):
    def timed(*args, **kwargs):
        start = timer()
        print(func(*args, **kwargs))
        end = timer()
        return 'Time taken: {}'.format(end - start)
    return timed

@timedec
def q1(num_elves):
    '''
    Use deque to store [elf_no, no. of presents].
    Note: in the end no. of presents wasn't needed for either part of the question.
    The leftmost elf is it's turn to steal, and the second leftmost elf is the one that will lose it's presents.

    http://stackoverflow.com/questions/23487307/python-deque-vs-list-performance-comparison
    Note: deque is MUCH faster than using a list (popleft is much quicker than pop(0))
    '''
    elves = deque((x + 1, 1) for x in range(num_elves))

    while len(elves) > 1:
        name, prez = elves.popleft()
        _, prez2 = elves.popleft()
        elves.append((name, prez + prez2))
        #print('Remaining elves: {}'.format(len(elves)))
    return 'Winner: {}'.format(elves)

@timedec
def q1_list(num_elves):
    '''
    Testing list speed vs original deque solution. (Note: it's slower)
    '''
    elves = [(x + 1, 1) for x in range(num_elves)]
    while len(elves) > 1:
        name, prez = elves.pop(0)
        _, prez2 = elves.pop(0)
        elves.append((name, prez + prez2))
        #print('Remaining elves: {}'.format(len(elves)))
    return 'Winner: {}'.format(elves)


def josephus_problem(num_elves):
    '''
    https://www.youtube.com/watch?v=uCsD3ZGzMgE

    if n = 2**a + L:
        the winner is 2L + 1

    A shortcut is to take the MSB and make it the LSB of a bin_elvesry representation of n.
    '''
    bin_elves = bin(num_elves)
    return 'Winner is {}'.format(int(bin_elves[:2] + bin_elves[3:] + bin_elves[2], 2))

def q2_basic(num_elves):
    elves = list(range(1, num_elves + 1))

    while len(elves) > 1:
        del elves[len(elves) // 2]
        elf = elves.pop(0)
        elves.append(elf)
        print(len(elves))

    return 'Winner: {}'.format(elves)

def q2_dual_deque(num_elves):
    '''
    Using two deques for better performance.
    First elf in L1 is the winner, first elf in L2 is the loser.
    Move winner to end of L2.
    If len of two deques becomes 2, move the next elf in L2 to the end of L1, so
    that the loser is always the middle (in terms of overall) remaining elf.
    '''
    L1 = deque(x + 1for x in range(num_elves // 2))
    L2 = deque((x + 1 + num_elves // 2) for x in range(num_elves - num_elves // 2))

    while L1:
        winner = L1.popleft()
        L2.popleft()
        L2.append(winner)

        if len(L2) - len(L1) == 2:
            L1.append(L2.popleft())

        print(len(L1) + len(L2))

    return L1, L2


# print(josephus_problem(5))
# print(josephus_problem(3018458))

# print(q1_list(50000))
# print(q1(50000))

# q1(5)
# q1(3018458)

# print(q2_dual_deque(10))
# print(q2_dual_deque(9))
# print(q2_dual_deque(3018458))

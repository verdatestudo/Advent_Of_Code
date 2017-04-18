'''
Advent of Code - 2016 - Day 20
http://adventofcode.com/2016

Last Updated: 2017-Mar-03
First Created: 2017-Mar-03
Python 3.5
Chris

--- Day 20: Firewall Rules ---

You'd like to set up a small hidden computer here so you can use it to get back into the network later.
However, the corporate firewall only allows communication with certain external IP addresses.

You've retrieved the list of blocked IPs from the firewall, but the list seems to be messy and poorly maintained, and it's not clear which IPs are allowed.
Also, rather than being written in dot-decimal notation, they are written as plain 32-bit integers, which can have any value from 0 through 4294967295, inclusive.

For example, suppose only the values 0 through 9 were valid, and that you retrieved the following blacklist:

5-8
0-2
4-7

The blacklist specifies ranges of IPs (inclusive of both the start and end value) that are not allowed.
Then, the only IPs that this firewall allows are 3 and 9, since those are the only numbers not in any range.

Given the list of blocked IPs you retrieved from the firewall (your puzzle input), what is the lowest-valued IP that is not blocked?

To begin, get your puzzle input.

Your puzzle answer was 22887907.

--- Part Two ---

How many IPs are allowed by the blacklist?

Your puzzle answer was 109.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

def get_data(filename='aoc2016_day20.txt'):
    with open(filename, 'r') as f:
        data = []
        for line in f:
            data.append([int(x) for x in line.strip('\n').split('-')])
    return data

def q20():
    '''
    After sorting, data is in the form [[0, 10], [11, 24], [18, 24]].
    For each item, if start is larger than the previously stored largest value,
    then that is a valid answer (i.e it's not in the range of illegal numbers).
    '''
    data = sorted(get_data())
    start, end = data[0]
    for next_start, next_end in data[1:]:
        for item in range(end + 1, next_start):
            yield item
        end = max(end, next_end)


ans = list(q20())
print(ans[0], len(ans))

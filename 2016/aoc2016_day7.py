
'''
Advent of Code - 2016 - Day 7
http://adventofcode.com/2016

Last Updated: 2017-Jan-07
First Created: 2017-Jan-07
Python 3.5
Chris

--- Day 7: Internet Protocol Version 7 ---

While snooping around the local network of EBHQ, you compile a list of IP addresses (they're IPv7, of course; IPv6 is much too limited).
You'd like to figure out which IPs support TLS (transport-layer snooping).

An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or ABBA. An ABBA is any four-character sequence which consists of a pair of two different characters
followed by the reverse of that pair, such as xyyx or abba. However, the IP also must not have an ABBA within any hypernet sequences, which are contained by square brackets.

For example:

    abba[mnop]qrst supports TLS (abba outside square brackets).
    abcd[bddb]xyyx does not support TLS (bddb is within square brackets, even though xyyx is outside square brackets).
    aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior characters must be different).
    ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets, even though it's within a larger string).

How many IPs in your puzzle input support TLS?

--- Part Two ---

You would also like to know which IPs support SSL (super-secret listening).

An IP supports SSL if it has an Area-Broadcast Accessor, or ABA, anywhere in the supernet sequences (outside any square bracketed sections),
and a corresponding Byte Allocation Block, or BAB, anywhere in the hypernet sequences.
An ABA is any three-character sequence which consists of the same character twice with a different character between them, such as xyx or aba.
A corresponding BAB is the same characters but in reversed positions: yxy and bab, respectively.

For example:

    aba[bab]xyz supports SSL (aba outside square brackets with corresponding bab within square brackets).
    xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
    aaa[kek]eke supports SSL (eke in supernet with corresponding kek in hypernet; the aaa sequence is not related, because the interior character must be different).
    zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz has a corresponding bzb, even though zaz and zbz overlap).

How many IPs in your puzzle input support SSL?

'''

import re

def get_data(filename):
    with open(filename, 'r') as input_file:
        return [line.strip('\n') for line in input_file]

def check_window_tls(line):
    flag = False
    for sec_idx, section in enumerate(line):
        inside = (sec_idx % 2 != 0)
        for idx, letter in enumerate(section[3:], 3):
            window = section[idx - 3: idx + 1]
            if window == window[::-1] and window[0] != window[1]:
                if inside:
                    return False
                else:
                    flag = True
    return flag

def valid_tls(filename):
    data = get_data(filename)
    items = [re.split(r'\[|\]', line) for line in data]
    count = sum([check_window_tls(line) for line in items])
    return count

def check_window_ssl(line):
    abas = []
    babs = []
    for sec_idx, section in enumerate(line):
        for idx, letter in enumerate(section[2:], 2):
            window = section[idx - 2: idx + 1]
            if window[0] == window[2] and window[0] != window[1]:
                if sec_idx % 2 == 0:
                    babs.append(window)
                else:
                    abas.append(window)
    for item in babs:
        if (item[1] + item[0] + item[1]) in abas:
            return True

    return False

def valid_ssl(filename):
    data = get_data(filename)
    # data = filename
    items = [re.split(r'\[|\]', line) for line in data]
    count = sum([check_window_ssl(line) for line in items])
    return count


# test_data_tls = ['abba[mnop]qrst', 'abcd[bddb]xyyx', 'aaaa[qwer]tyui', 'ioxxoj[asdfgh]zxcvbn', 'aaar[bbb]cccr[ddd]eeer']
# print(valid_tls(test_data_tls, 2))
print(valid_tls('aoc2016_day7.txt'), 118)

# test_data_ssl = ['aba[bab]xyz', 'xyx[xyx]xyx', 'aaa[kek]eke', 'zazbz[bzb]cdb']
# print(valid_ssl(test_data_ssl))
print(valid_ssl('aoc2016_day7.txt'), 260)

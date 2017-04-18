'''
Advent of Code - 2016 - Day 12
http://adventofcode.com/2016

Last Updated: 2017-Feb-22
First Created: 2017-Feb-21
Python 3.5
Chris

--- Day 12: Leonardo's Monorail ---

You finally reach the top floor of this building: a garden with a slanted glass ceiling. Looks like there are no more stars to be had.

While sitting on a nearby bench amidst some tiger lilies, you manage to decrypt some of the files you extracted from the servers downstairs.

According to these documents, Easter Bunny HQ isn't just this building - it's a collection of buildings in the nearby area.
They're all connected by a local monorail, and there's another building not far from here! Unfortunately, being night, the monorail is currently not operating.

You remotely connect to the monorail control systems and discover that the boot sequence expects a password.
The password-checking logic (your puzzle input) is easy to extract, but the code it uses is strange:
it's assembunny code designed for the new computer you just assembled. You'll have to execute the code and get the password.

The assembunny code you've extracted operates on four registers (a, b, c, and d) that start at 0 and can hold any integer. However, it seems to make use of only a few instructions:

    cpy x y copies x (either an integer or the value of a register) into register y.
    inc x increases the value of register x by one.
    dec x decreases the value of register x by one.
    jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.

The jnz instruction moves relative to itself: an offset of -1 would continue at the previous instruction, while an offset of 2 would skip over the next instruction.

For example:

cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a

The above code would set register a to 41, increase its value by 2, decrease its value by 1, and then skip the last dec
a (because a is not zero, so the jnz a 2 skips it), leaving register a at 42.
When you move past the last instruction, the program halts.

After executing the assembunny code in your puzzle input, what value is left in register a?

Your puzzle answer was 318020.

The first half of this puzzle is complete! It provides one gold star: *
--- Part Two ---

As you head down the fire escape to the monorail, you notice it didn't start; register c needs to be initialized to the position of the ignition key.

If you instead initialize register c to be 1, what value is now left in register a?

Although it hasn't changed, you can still get your puzzle input.

Your puzzle answer was 9227674.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_data(filename='aoc2016_day12.txt'):
    commands = []
    with open(filename) as f:
        for line in f:
            commands.append([x if x.isalpha() else int(x) for x in line.split()])
    return commands

commands = get_data()

vals = {'a': 0, 'b': 0, 'c': 0, 'd': 0} # part one
vals = {'a': 0, 'b': 0, 'c': 1, 'd': 0} # part two

idx = 0
moves_made = []

while idx < len(commands):
    command = commands[idx]
    cmd, x, y = command[0], command[1], command[-1]

    if cmd in ('inc', 'dec'):
        vals[x] += (cmd == 'inc') or -1 # if inc then this is 1, if it's dec then it's -1
    elif cmd == 'cpy':
        if is_int(x):
            vals[y] = x
        else:
            vals[y] = vals[x]
    elif cmd == 'jnz':
        if (is_int(x) and x > 0) or (not is_int(x) and vals[x] > 0):
            if y == -2:
                # there are several loops which involve increase 1, decrease 1
                # using this we do it in one go rather than repeating the same commands thousands of times.
                (cmd_a, val_a), (cmd_b, val_b) = moves_made[-2:] # get the last two moves before jnz 2, e.g (inc b, dec c)
                if cmd_a == 'dec':
                    vals[val_b] += vals[val_a]
                    vals[val_a] = 0
                else:
                    vals[val_a] += vals[val_b]
                    vals[val_b] = 0
            else:
                idx += y - 1
    else:
        print('unexpected command')

    moves_made.append(command)
    idx += 1

print(vals)

'''

Advent of Code - 2016 - Day 23
http://adventofcode.com/2016

Last Updated: 2017-Apr-12
First Created: 2017-Apr-07
Python 3.6
Chris

--- Day 23: Safe Cracking ---

This is one of the top floors of the nicest tower in EBHQ. The Easter Bunny's private office is here,
complete with a safe hidden behind a painting, and who wouldn't hide a star in a safe behind a painting?

The safe has a digital screen and keypad for code entry.
A sticky note attached to the safe has a password hint on it: "eggs".
The painting is of a large rabbit coloring some eggs. You see 7.

When you go to type the code, though, nothing appears on the display; instead, the keypad comes apart in your hands, apparently having been smashed.
Behind it is some kind of socket - one that matches a connector in your prototype computer!
You pull apart the smashed keypad and extract the logic circuit, plug it into your computer, and plug your computer into the safe.

Now, you just need to figure out what output the keypad would have sent to the safe. You extract the assembunny code from the logic chip (your puzzle input).

The code looks like it uses almost the same architecture and instruction set that the monorail computer used!
You should be able to use the same assembunny interpreter for this as you did there, but with one new instruction:

tgl x toggles the instruction x away (pointing at instructions like jnz does: positive means forward; negative means backward):

    For one-argument instructions, inc becomes dec, and all other one-argument instructions become inc.
    For two-argument instructions, jnz becomes cpy, and all other two-instructions become jnz.
    The arguments of a toggled instruction are not affected.
    If an attempt is made to toggle an instruction outside the program, nothing happens.
    If toggling produces an invalid instruction (like cpy 1 2) and an attempt is later made to execute that instruction, skip it instead.
    If tgl toggles itself (for example, if a is 0, tgl a would target itself and become inc a), the resulting instruction is not executed until the next time it is reached.

For example, given this program:

cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a

    cpy 2 a initializes register a to 2.
    The first tgl a toggles an instruction a (2) away from it, which changes the third tgl a into inc a.
    The second tgl a also modifies an instruction 2 away from it, which changes the cpy 1 a into jnz 1 a.
    The fourth line, which is now inc a, increments a to 3.
    Finally, the fifth line, which is now jnz 1 a, jumps a (3) instructions ahead, skipping the dec a instructions.

In this example, the final value in register a is 3.

The rest of the electronics seem to place the keypad entry (the number of eggs, 7) in register a, run the code, and then send the value left in register a to the safe.

What value should be sent to the safe?

To begin, get your puzzle input.

Your puzzle answer was 14160.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---

The safe doesn't open, but it does make several angry noises to express its frustration.

You're quite sure your logic is working correctly, so the only other thing is... you check the painting again.
s it turns out, colored eggs are still eggs. Now you count 12.

As you run the program with this new input, the prototype computer begins to overheat.
You wonder what's taking so long, and whether the lack of any instruction more powerful than "add one" has anything to do with it.
Don't bunnies usually multiply?

Anyway, what value should actually be sent to the safe?

Your puzzle answer was 479010720.

Both parts of this puzzle are complete! They provide two gold stars: **

'''

import time

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def get_data(filename):
    commands = []
    with open(filename) as f:
        for line in f:
            commands.append([x if x.isalpha() else int(x) for x in line.split()])
    return commands

def tgl_cmd(command):
    cmd, x, y = command[0], command[1], command[-1]
    if x == y: # check this works for differing one argument from two arguments
        if cmd == 'inc':
            cmd = 'dec'
        else:
            cmd = 'inc'
        return [cmd, x]
    else:
        if cmd == 'jnz':
            cmd = 'cpy'
        else:
            cmd = 'jnz'
        return [cmd, x, y]

def multiply_commands(moves_made):
    pass

def day23(commands, vals):
    idx = 0
    moves_made = []
    debug = []

    while idx < len(commands):
        debug.append('{} {} {} \n'.format(idx, commands[idx], vals))
        print(idx, commands[idx], vals)

        command = commands[idx]
        cmd, x, y = command[0], command[1], command[-1]

        if cmd == 'inc': vals[x] += 1
        elif cmd == 'dec': vals[x] -= 1
        elif cmd == 'cpy':
            if not is_int(y):
                if is_int(x):
                    vals[y] = x
                else:
                    vals[y] = vals[x]
        elif cmd == 'jnz':
            if (is_int(x) and x > 0) or (not is_int(x) and vals[x] > 0):
                if y == -5 and idx != 25:
                    vals['a'] += (vals['b'] * vals['d'])
                    vals['d'] = 0
                    continue
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
                    if is_int(y): # y - 1 because we auto-increment idx after each move later.
                        idx += y - 1
                    else:
                        idx += vals[y] - 1

        elif cmd == 'tgl':
            if idx + vals[x] < len(commands):
                commands[idx + vals[x]] = tgl_cmd(commands[idx + vals[x]])
        else:
            print('unexpected command')

        moves_made.append(command)
        idx += 1

    with open('aoc2016_day23_debug.txt', 'w') as txt_file:
        txt_file.write('\n'.join(debug))

    return vals



# starting vals
part_one = {'a': 7, 'b': 0, 'c': 0, 'd': 0}
part_two = {'a': 12, 'b': 0, 'c': 0, 'd': 0}

commands = get_data('aoc2016_day23.txt')
ans_part_one = day23(commands, part_one)
commands = get_data('aoc2016_day23.txt')
ans_part_two = day23(commands, part_two)

print('\n', ans_part_one, ans_part_one['a'] == 14160)
print('\n', ans_part_two, ans_part_two['a'] == 479010720)

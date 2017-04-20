'''

Advent of Code - 2016 - Day 25
http://adventofcode.com/2016

Last Updated: 2017-Apr-18
First Created: 2017-Apr-11
Python 3.6
Chris

--- Day 25: Clock Signal ---

You open the door and find yourself on the roof. The city sprawls away from you for miles and miles.
There's not much time now - it's already Christmas, but you're nowhere near the North Pole, much too far to deliver these stars to the sleigh in time.

However, maybe the huge antenna up here can offer a solution. After all, the sleigh doesn't need the stars, exactly;
it needs the timing data they provide, and you happen to have a massive signal generator right here.

You connect the stars you have to your prototype computer, connect that to the antenna, and begin the transmission.
Nothing happens.

You call the service number printed on the side of the antenna and quickly explain the situation.
"I'm not sure what kind of equipment you have connected over there," he says, "but you need a clock signal."
You try to explain that this is a signal for a clock.

"No, no, a clock signal - timing information so the antenna computer knows how to read the data you're sending it.
An endless, alternating pattern of 0, 1, 0, 1, 0, 1, 0, 1, 0, 1...." He trails off.

You ask if the antenna can handle a clock signal at the frequency you would need to use for the data from the stars. "There's no way it can!
The only antenna we've installed capable of that is on top of a top-secret Easter Bunny installation, and you're definitely not-" You hang up the phone.

You've extracted the antenna's clock signal generation assembunny code (your puzzle input); it looks mostly compatible with code you worked on just recently.

This antenna code, being a signal generator, uses one extra instruction:

    out x transmits x (either an integer or the value of a register) as the next value for the clock signal.

The code takes a value (via register a) that describes the signal to generate, but you're not sure how it's used.
You'll have to find the input to produce the right signal through experimentation.

What is the lowest positive integer that can be used to initialize register a and cause the code to output a clock signal of 0, 1, 0, 1... repeating forever?

Your puzzle answer was 158.
--- Part Two ---

The antenna is ready. Now, all you need is the fifty stars required to generate the signal for the sleigh, but you don't have enough.

You look toward the sky in desperation... suddenly noticing that a lone star has been installed at the top of the antenna! Only 49 more to go.

If you like, you can retransmit the signal.

Both parts of this puzzle are complete! They provide two gold stars: **

At this point, all that is left is for you to admire your advent calendar.


You activate all fifty stars and transmit the signal. The star atop the antenna begins to glow.
Suddenly, you see the sleigh fly past you!

Looks like Santa was already waiting for your signal.

Congratulations! You've finished every puzzle in Advent of Code 2016! I hope you had as much fun solving them as I had making them for you.
I'd love to hear about your adventure; you can get in touch with me via contact info on my website or through Twitter.

If you'd like to see more things like this in the future, please consider supporting Advent of Code and sharing it with others.

To hear about future projects, you can follow me on Twitter.

I've highlighted the easter eggs in each puzzle, just in case you missed any. Hover your mouse over them, and the easter egg will appear.

'''

import time

def get_data(filename='aoc2016_day25.txt'):
    commands = []
    with open(filename) as f:
        for line in f:
            commands.append([x if x.isalpha() else int(x) for x in line.split()])
    return commands

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

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

def part_one():
    for attempt in range(10000):
        vals = {'a': attempt, 'b': 0, 'c': 0, 'd': 0}
        idx = 0
        moves_made = []

        ans = 0
        repeat_count = 0

        while idx < len(commands) and repeat_count < 100:
            if len(vals) > 4:
                break
            # debug.append('{} {} {} \n'.format(idx, commands[idx], vals))

            command = commands[idx]
            cmd, x, y = command[0], command[1], command[-1]

            if cmd in ('inc', 'dec'):
                vals[x] += (cmd == 'inc') or -1 # if inc then this is 1, if it's dec then it's -1
            elif cmd == 'cpy':
                if is_int(y):
                    pass
                else:
                    if is_int(x):
                        vals[y] = x
                    else:
                        vals[y] = vals[x]
            elif cmd == 'jnz':
                if (is_int(x) and x > 0) or (not is_int(x) and vals[x] > 0):
                    try:
                        idx += y - 1
                    except TypeError:
                        idx += vals[y] - 1

            elif cmd == 'tgl':
                val = vals[x]
                if idx + val < len(commands):
                    commands[idx + val] = tgl_cmd(commands[idx + val])
            elif cmd == 'out':
                if vals[x] == ans:
                    ans = (ans + 1) % 2
                    repeat_count += 1
                else:
                    break
            else:
                print('unexpected command')

            moves_made.append(command)
            idx += 1

        if repeat_count == 100:
            break
        else:
            print(attempt, repeat_count)


    print('attempt success:', attempt, repeat_count)


commands = get_data()
part_one()

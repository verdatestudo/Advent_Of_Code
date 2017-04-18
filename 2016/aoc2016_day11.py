
'''
Advent of Code - 2016 - Day 11
http://adventofcode.com/2016

Last Updated: 2017-Feb-21
First Created: 2017-Feb-03
Python 3.5
Chris

--- Day 11: Radioisotope Thermoelectric Generators ---

You come upon a column of four floors that have been entirely sealed off from the rest of the building except for a small dedicated lobby.
There are some radiation warnings and a big sign which reads "Radioisotope Testing Facility".

According to the project status board, this facility is currently being used to experiment with Radioisotope Thermoelectric Generators (RTGs, or simply "generators")
that are designed to be paired with specially-constructed microchips. Basically, an RTG is a highly radioactive rock that generates electricity through heat.

The experimental RTGs have poor radiation containment, so they're dangerously radioactive.
The chips are prototypes and don't have normal radiation shielding, but they do have the ability to generate an electromagnetic radiation shield when powered.
Unfortunately, they can only be powered by their corresponding RTG. An RTG powering a microchip is still dangerous to other microchips.

In other words, if a chip is ever left in the same area as another RTG, and it's not connected to its own RTG, the chip will be fried.
Therefore, it is assumed that you will follow procedure and keep chips connected to their corresponding RTG when they're in the same room, and away from other RTGs otherwise.

These microchips sound very interesting and useful to your current activities, and you'd like to try to retrieve them.
The fourth floor of the facility has an assembling machine which can make a self-contained, shielded computer for you to take with you - that is, if you can bring it all of the RTGs and microchips.

Within the radiation-shielded part of the facility (in which it's safe to have these pre-assembly RTGs), there is an elevator that can move between the four floors.
Its capacity rating means it can carry at most yourself and two RTGs or microchips in any combination. (They're rigged to some heavy diagnostic equipment - the assembling machine will detach it for you.)
As a security measure, the elevator will only function if it contains at least one RTG or microchip.
The elevator always stops on each floor to recharge, and this takes long enough that the items within it and the items on that floor can irradiate each other.
(You can prevent this if a Microchip and its Generator end up on the same floor in this way, as they can be connected while the elevator is recharging.)

You make some notes of the locations of each component of interest (your puzzle input).
Before you don a hazmat suit and start moving things around, you'd like to have an idea of what you need to do.

When you enter the containment area, you and the elevator will start on the first floor.

For example, suppose the isolated area has the following arrangement:

The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.

As a diagram (F# for a Floor number, E for Elevator, H for Hydrogen, L for Lithium, M for Microchip, and G for Generator), the initial state looks like this:

F4 .  .  .  .  .
F3 .  .  .  LG .
F2 .  HG .  .  .
F1 E  .  HM .  LM

Then, to get everything up to the assembling machine on the fourth floor, the following steps could be taken:

    Bring the Hydrogen-compatible Microchip to the second floor, which is safe because it can get power from the Hydrogen Generator:

    F4 .  .  .  .  .
    F3 .  .  .  LG .
    F2 E  HG HM .  .
    F1 .  .  .  .  LM

    Bring both Hydrogen-related items to the third floor, which is safe because the Hydrogen-compatible microchip is getting power from its generator:

    F4 .  .  .  .  .
    F3 E  HG HM LG .
    F2 .  .  .  .  .
    F1 .  .  .  .  LM

    Leave the Hydrogen Generator on floor three, but bring the Hydrogen-compatible Microchip back down with you so you can still use the elevator:

    F4 .  .  .  .  .
    F3 .  HG .  LG .
    F2 E  .  HM .  .
    F1 .  .  .  .  LM

    At the first floor, grab the Lithium-compatible Microchip, which is safe because Microchips don't affect each other:

    F4 .  .  .  .  .
    F3 .  HG .  LG .
    F2 .  .  .  .  .
    F1 E  .  HM .  LM

    Bring both Microchips up one floor, where there is nothing to fry them:

    F4 .  .  .  .  .
    F3 .  HG .  LG .
    F2 E  .  HM .  LM
    F1 .  .  .  .  .

    Bring both Microchips up again to floor three, where they can be temporarily connected to their corresponding generators while the elevator recharges, preventing either of them from being fried:

    F4 .  .  .  .  .
    F3 E  HG HM LG LM
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring both Microchips to the fourth floor:

    F4 E  .  HM .  LM
    F3 .  HG .  LG .
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Leave the Lithium-compatible microchip on the fourth floor, but bring the Hydrogen-compatible one so you can still use the elevator; this is safe because although the Lithium Generator is on the destination floor, you can connect Hydrogen-compatible microchip to the Hydrogen Generator there:

    F4 .  .  .  .  LM
    F3 E  HG HM LG .
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring both Generators up to the fourth floor, which is safe because you can connect the Lithium-compatible Microchip to the Lithium Generator upon arrival:

    F4 E  HG .  LG LM
    F3 .  .  HM .  .
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring the Lithium Microchip with you to the third floor so you can use the elevator:

    F4 .  HG .  LG .
    F3 E  .  HM .  LM
    F2 .  .  .  .  .
    F1 .  .  .  .  .

    Bring both Microchips to the fourth floor:

    F4 E  HG HM LG LM
    F3 .  .  .  .  .
    F2 .  .  .  .  .
    F1 .  .  .  .  .

In this arrangement, it takes 11 steps to collect all of the objects at the fourth floor for assembly. (Each elevator stop counts as one step, even if nothing is added to or removed from it.)

In your situation, what is the minimum number of steps required to bring all of the objects to the fourth floor?

Your puzzle answer was 33.

--- Part Two ---

You step into the cleanroom separating the lobby from the isolated area and put on the hazmat suit.

Upon entering the isolated containment area, however, you notice some extra parts on the first floor that weren't listed on the record outside:

    An elerium generator.
    An elerium-compatible microchip.
    A dilithium generator.
    A dilithium-compatible microchip.

These work just like the other generators and microchips. You'll have to get them up to assembly as well.

What is the minimum number of steps required to bring all of the objects, including these four new ones, to the fourth floor?

Your puzzle answer was 57.

(Borrowed heavily from Peter Norvig's solution)

'''

import heapq
import math
from collections import namedtuple, defaultdict
from itertools import chain, combinations
import re
from timeit import default_timer as timer

### basic Astar start ***

def Path(previous, state):
    return ([] if state is None else Path(previous, previous[state]) + [state])

def astar_search(start, h_func, moves_func, materials):
    frontier = [(h_func(start), start)]
    previous = {start: None}
    path_cost = {start: 0}
    unique_states = set()
    unique_items_state(start, unique_states, materials)

    while frontier:
        (f, s) = heapq.heappop(frontier)
        print('Distance to goal: {}, No. of States: {}'.format(h_func(s), len(unique_states)))
        if h_func(s) == 0:
            return Path(previous, s)
        for s2 in moves_func(s):
            new_cost = path_cost[s] + 1
            if unique_items_state(s2, unique_states, materials): # added this to speed up Q11 part 2
            #if s2 not in path_cost or new_cost < path_cost[s2]:
                heapq.heappush(frontier, (h_func(s2) + new_cost, s2))
                previous[s2] = s
                path_cost[s2] = new_cost

    return previous # if fail to find a path

### basic Astar end ###

def unique_items_state(state, unique_states, materials):
    '''
    Takes a state and checks it is unique.
    For example State(0, {aG, aM}, {}, {tM}, {tG}) is the same as State(0, {tG, tM}, {}, {aM}, {aG}),
    therefore we only want to include one of these paths.
    '''
    # in the format material: [G_floor, M_floor] e.g Cobalt = [0, 2], Titanium = [1, 3]
    material_pairs = {material: [0, 0] for material in materials}

    for idx, floor in enumerate(state.floors):
        for item in floor:
            material, is_chip = item[:-1], item[-1] == 'M' # is_chip = 0 for G, 1 for M
            material_pairs[material][is_chip] = idx

    # per example in docs, both States would result in (0, (0, 0), (3, 2)).
    mat_pairs = tuple([state.elevator] + sorted(tuple(x) for x in material_pairs.values()))

    if mat_pairs in unique_states:
        return False
    else:
        unique_states.add(mat_pairs)
        return True

def q11():
    State = namedtuple('State', ['elevator', 'floors'])
    legal_floors = {0, 1, 2, 3}

    def fs(*items): return frozenset(items)

    def combos(items):
        for combo in chain(combinations(items, 1), combinations(items, 2)):
            yield fs(*combo)

    def legal_floor(floor):
        gens = any(item.endswith('G') for item in floor)
        chips = [item[:-1] for item in floor if item.endswith('M')]
        return not gens or all(c + 'G' in floor for c in chips)

    def h_to_top(state):
        total = sum(len(floor) * i for i, floor in enumerate(reversed(state.floors)))
        return math.ceil(total / 2)

    def moves(state):
        L, floors = state
        for L2 in {L-1, L+1} & legal_floors:
            for stuff in combos(floors[L]):
                newfloors = tuple((s | stuff if i == L2 else
                                   s - stuff if i == state.elevator else
                                   s)
                                  for (i, s) in enumerate(state.floors))
                if legal_floor(newfloors[L]) and legal_floor(newfloors[L2]):
                    yield State(L2, newfloors)

    def parse(filename):
        floors = []
        materials = set()
        with open(filename, 'r') as f:
            for line in f:
                items = re.findall(r'(\w+) generator|(\w+)-compatible microchip', line) # returns (gen_material, '') or ('', chip_material)
                materials.update(material for material, _ in items if material)
                floors.append(frozenset([gen+'G' if gen else chip+'M' for gen, chip in items]))

                # old code
                #gens = [gen + 'G' for gen in re.findall(r'(\w+) generator', line)]
                #chips = [chip + 'M' for chip in re.findall(r'(\w+)-compatible microchip', line)]
        return State(0, tuple(floors)), materials

    def time_func(func):
        def timed():
            start = timer()
            func()
            end = timer()
            print(end - start)
            return end - start
        return timed

    @time_func
    def solve():
        # part_one, materials = parse('aoc2016_day11.txt')
        part_two, materials = parse('aoc2016_day11_part_two.txt')

        ans = astar_search(part_two, h_to_top, moves, materials)
        for step in ans:
            print(step)
        print('no. of moves: {}'.format(len(ans) - 1))

    def test():
        easy = State(0, (fs('RG'), frozenset(), fs('RM'), fs('LG', 'LM')))
        easy = State(0, (fs('TM'), fs('RM'), fs('RG'), fs('LG', 'LM', 'TG')))
        materials = set(['R', 'L', 'T'])

        ans = astar_search(easy, h_to_top, moves, materials)
        for step in ans:
            print(step)

    solve()

q11()

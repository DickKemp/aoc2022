from dataclasses import dataclass

@dataclass
class Elf:
    energy: list[int]
    def get_sum(self):
        return sum(self.energy)

filename = "1/p1_input.txt"

def consume_elves_input(inp):
    elves = []
    numbers = []
    for line in inp:
        # try to convert the line to an integer
        try:
            # if the conversion succeeds, collect the int value for thsi elf
            numbers.append(int(line))
        except ValueError:
            # if the conversion fails, we hit a line, so gather all the numbers and form an elf
            # and save it into the elves list
            elves.append(Elf(numbers))
            numbers = []
            continue
    # collect the last set of numbers
    elves.append(Elf(numbers))
    return elves

with open(filename, "r") as file:
    elves = consume_elves_input(file)
    allsums = [e.get_sum() for e in elves]
    print(max(allsums))
    sorted_allsums = sorted(allsums, reverse=True)
    print(sum(sorted_allsums[0:3]))






import os
# define the name of the file to read from
filename = "1/p1_input.txt"
print(os.getcwd())
# initialize an empty list to store the integers from the file
numbers = []
sums = []

with open(filename, "r") as file:
    # read each line of the file
    for line in file:
        # try to convert the line to an integer
        try:
            # if the conversion succeeds, append the integer to the list
            numbers.append(int(line))
        except ValueError:
            # if the conversion fails, skip the line
            # and sum all the lines collected so far
            sums.append(sum(numbers))
            numbers = []
            continue
sums.append(sum(numbers))

# print(sums)
print(max(sums))


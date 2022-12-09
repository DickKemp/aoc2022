this puzzle is a little bit more involved than any of the prior puzzles to date.
solving this will involve:
1. parse the puzzle input to extract the commands that were executed along with the command output
2. "execute" the list of commands and outputs to build up the data structures that 
represent the tree of directories
3. traverse the tree in a way that enumerate the directories as well as calculates their size, probably a recursive search of the tree (depth first), and then calculating the directory sizes on the way back up the recursion
4. filter this list of directories for those that are less than size 10000 and then sum it all up

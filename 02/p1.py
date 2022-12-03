from dataclasses import dataclass

@dataclass
class Round:
    your_move: str
    opponent_move: str
    """
    A or X is Rock
    B or Y is Paper
    C or Z is Sissors
    
    """
    @staticmethod
    def get_score(you, opp):
        score = 0
        if you == 'R':
            score += 1
            if opp == 'S':
                score += 6
            elif opp == 'R':
                score += 3
        if you == 'P':
            score += 2
            if opp == 'R':
                score += 6
            elif opp == 'P':
                score += 3
        if you == 'S':            
            score += 3
            if opp == 'P':
                score += 6
            elif opp == 'S':
                score += 3
        return score

        """Anyway, the second column says how the round needs to end: 
        X means you need to lose, 
        Y means you need to end the round in a draw, and 
        Z means you need to win. Good luck!
        """

# filename = "2/test_p1_input.txt"
filename = "2/p1_input.txt"

def decrypt(xyz):
    if xyz == 'A' or xyz == 'X':
        return 'R'
    if xyz == 'B' or xyz == 'Y':
        return 'P'
    if xyz == 'C' or xyz == 'Z':
        return 'S'

def calc_wining_move(x):
    if x == 'R':
        return 'P'
    if x == 'P':
        return 'S'
    if x == 'S':
        return 'R'
def calc_draw_move(x):
    if x == 'R':
        return 'R'
    if x == 'P':
        return 'P'
    if x == 'S':
        return 'S'
def calc_losing_move(x):
    if x == 'R':
        return 'S'
    if x == 'P':
        return 'R'
    if x == 'S':
        return 'P'

def consume_strategy_pt1_input(inp):
    rounds = []
    for line in inp:
        s = line.split()
        opp = decrypt(s[0])
        you = decrypt(s[1])
        rounds.append(Round(you, opp))
    return rounds

def consume_strategy_pt2_input(inp):
    rounds = []
    for line in inp:
        s = line.split()
        opp = decrypt(s[0])
        outcome = decrypt(s[1])
        if outcome == 'R':
            # should lose
            you = calc_losing_move(opp)
        elif outcome == 'P':
            # should draw
            you = calc_draw_move(opp)
        elif outcome == 'S':            
            # should win
            you = calc_wining_move(opp)

        rounds.append(Round(you, opp))
    return rounds

with open(filename, "r") as file:
    # pt1
    # rounds = consume_strategy_pt1_input(file)
    # pt2
    rounds = consume_strategy_pt2_input(file)
    allscores = [Round.get_score(s.your_move, s.opponent_move) for s in rounds]
    print(sum(allscores))


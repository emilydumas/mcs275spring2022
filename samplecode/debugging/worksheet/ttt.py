"""Broken tic-tac-toe game"""

# MCS 275 Spring 2022 - David Dumas

# Inspired by an example from https://github.com/satwikkansal/wtfpython#-a-tic-tac-toe-where-x-wins-in-the-first-attempt
# Warning: link above contains major spoilers, as well as some crude language.
# You don't need to look at that link at all, and *definitely* shouldn't look
# until after you're done.

def winner(b):
    """Given a TTT board `b`, determine who has won and return.  If no one has won,
    return None"""
    # Row of three
    for row in b:
        if row[0] == " ":
            # First row entry is blank; ignore!
            continue
        if row[0]==row[1] and row[1]==row[2]:
            return row[0]
    # Column of three
    for i in range(3):
        if b[0][i] == " ":
            # First column entry is blank; ignore!
            continue
        if b[0][i]==b[1][i] and b[1][i]==b[2][i]:
            return b[0][i]
    # Diagonals
    if b[1][1] != " ":
        # Middle entry not blank, so diagonal win 
        # is a possibility.
        if b[0][0] == b[1][1] and b[1][1]==b[2][2]:
            return b[0][0]
        if b[0][2] == b[1][1] and b[1][1]==b[2][0]:
            return b[0][2]
    # implicit return None


def print_board(b):
    """Show the board with 1-based coordinates"""
    print("  A|B|C")
    for i,r in enumerate(b):
        print("{}".format(i+1),"|".join(r))
        if i<2:
            print("---+-+-")


COLS = ["a","b","c"]

def apply_move(b,player,move):
    """Modify board b (list of lists) to account for move in string `move`.
    If the move is illegal, raises an exception."""
    move = move.strip().lower()
    if len(move)!=2:
        raise Exception("Valid move is two characters (e.g. A2 or B3)")
    if move[0] not in COLS:
        move = move[::-1]
    if move[0] not in COLS:
        raise Exception("No column spec found")
    j = COLS.index(move[0])
    i = int(move[1])-1
    if b[i][j] != " ":
        raise Exception("Another move already filled that position")
    b[i][j] = player


if __name__=="__main__":
    print("Tic-tac-toe: enter moves by coordinates (e.g. A1 or B3)")
    print()
    empty_row = [" "] * 3  # create a row of blanks
    board = [ empty_row ] * 3 # create empty 3x3 grid
    cur,other = "X","O"
    while True:
        print_board(board)
        print()
        w = winner(board)
        if w:
            print("+----------------+")
            print("| Player {} wins! |".format(w))
            print("+----------------+")
            break
        print("It is {}'s turn.".format(cur,other))
        m = input("Move? ")
        print()
        try:
            apply_move(board,cur,m)
        except Exception:
            print("That move was not recognized, or not possible.\n")
            continue
        # switch active player
        cur,other = other,cur

from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# A knight is true
# A knave is false

# Puzzle 0
# A says "I am both a knight and a knave."
    # I cannot be both
    # therefore I am lying 
knowledge0 = And(
    # A can't be both a Knight and Knave
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    
    # Implication if A is a Knight, then A's statement is true
    Implication(AKnight, And(AKnight, AKnave)),

    # Implication if A is a Knave, then A's statement is false
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
    # A or B can't be both a Knight and Knave
    # if A is a knave, A is lying, therefore B must be a knight
    # if A is a Knight, A is true, therefore A can't be a Knave
    # if B is a Knave, A's statement is true, therefore B would disagree

knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # if A is a knight the statement is true but it leads to a contradiction
    Implication(AKnight, And(AKnave, BKnave)),

    # if A if a Knave then A is lying and the statement is false
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
    # A or B can't be both a Knight and Knave
    # If A is a knight, A is true, both are the same
    # If A is a knave, A flase, then A and B are different
    # if B is a knight, B is true, then A and B are different
    # if B is a knave, B is false, both are the same
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Implication(AKnight, Biconditional(AKnight, BKnight)),
    Implication(AKnave, Not(Biconditional(AKnight, BKnight))),

    Implication(BKnight, Not(Biconditional(AKnight, BKnight))),
    Implication(BKnave, Biconditional(AKnave, BKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
    # A or B can't be both a Knight and Knave
    # A is either a Knight or a Knave

knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # if B is a Knight, then both of the following must be true:
        # if A is a knight, then A must be a knave (contradiction)
        # if A is a Knave then A must not be a knave (contradiction)
    Implication(BKnight, And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    )),
    
    # if B is a knave, then one of the following must be false:
        # if A is a knight, then A must be a knave
        # if A is a Knave then A must not be a knave
    Implication(BKnave, Not(And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    ))),

    # if B is a knight, true, C is a knave
    # if B is a Knave, lie, C is a Knight
    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),
    
    # if C is knight, true, A is a Knight
    # if C is a Knave, lie, A is a Knave
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave)
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

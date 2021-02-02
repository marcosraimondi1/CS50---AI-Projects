from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is knight if and only if A is not a Knave
    Biconditional(AKnight, Not(AKnave)),
    # If A is a Knight, then A is both Knight and Knave
    Implication(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A is knight if and only if A is not a Knave
    Biconditional(AKnight, Not(AKnave)),
    # B is knight if and only if B is not a Knave
    Biconditional(BKnight, Not(BKnave)),
    # if A is knight then both are knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # if A is knave then only one of them is Knave not Both
    Implication(AKnave, And(AKnave, Not(BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is knight if and only if A is not a Knave
    Biconditional(AKnight, Not(AKnave)),
    # B is knight if and only if B is not a Knave
    Biconditional(BKnight, Not(BKnave)),
    # A Knight then both Knights
    Implication(AKnight, And(AKnight, BKnight)),
    # A Knave then they are not same kind
    Implication(AKnave, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    # B Knight then AKnave
    Implication(BKnight, AKnave),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A is knight if and only if A is not a Knave
    Biconditional(AKnight, Not(AKnave)),
    # B is knight if and only if B is not a Knave
    Biconditional(BKnight, Not(BKnave)),

    # if B Knight then A said 'I am a knave' and C is a Knave
    Implication(BKnight, And(CKnave,
                             # If A Knight --> AKnave
                             Implication(AKnight, AKnave))),

    # if B Knave then A said 'I am a knight' and C is a Knight
    Implication(BKnave, And(CKnight,
                            # If A Knight --> AKnight
                            Implication(AKnight, AKnight))),

    # if C is Knave then A is not Knight:
    Implication(CKnave, Not(AKnave)),

    # if C is Knight then A is Knight:
    Implication(CKnight, AKnight)
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

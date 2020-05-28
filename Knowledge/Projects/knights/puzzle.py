from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
game_rules = And(
                #one player can be a knight or a knave, not both
                Or(
                    And(
                        AKnight, Not(AKnave)
                    ),
                    And(
                        Not(AKnight), AKnave
                    )
                ),
                #a player cannot be both a knight and a knave
                Not(And(AKnight, AKnave)),
                Or(
                    And(
                        BKnight, Not(BKnave)
                    ),
                    And(
                        Not(BKnight), BKnave
                    )
                ),
                #a player cannot be both a knight and a knave
                Not(And(BKnight, BKnave)),
                Or(
                    And(
                        CKnight, Not(CKnave)
                    ),
                    And(
                        Not(CKnight), CKnave
                    )
                ),
                #a player cannot be both a knight and a knave
                Not(And(CKnight, CKnave))

            )

knowledge0 = And(
    #game rules
    game_rules,
    #if a knight, then what they said is true
    Implication(AKnight, And(AKnight, AKnave)),
    #if a knave, then what they said is false
    Implication(AKnave, Not(And(AKnight, AKnave)))
    #And(AKnight, AKnave)

    
    
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    game_rules,
    #a says we are both knaves
    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))

)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    game_rules,
    #same kind (aknight and bknight) or (aknave and bknave)
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    #diff kinds (aknight and bknave) or (aknave and bknight)
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Not(Or(And(AKnight, BKnave), And(AKnave, BKnight))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    game_rules,

    #if C is a knight, then A is a knight
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),
    #if B is knight, then C is a knave
    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),
    #if B is a knight, then ((if A is a knight, then A is a knight) & (if A is a knave, then A is not a knight))
    Implication(BKnight, And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))),
    Implication(BKnave, Not(And(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave))))),
    
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
            print("fuck")
            for symbol in symbols:
                if model_check(knowledge, symbol):

                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

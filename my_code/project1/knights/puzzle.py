from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")



Box = [[AKnight, AKnave], [BKnight, BKnave], [CKnight, CKnave]]
Word = [None, None, None] # What A, B, C says

# Construct knowledge base
def ConstructKnowledge(personCount):
    knowledge = And()
    for i in range(personCount):
        # A person must have one identity
        knowledge.add(Or(Box[i][0], Box[i][1]))
        # A person cannot have both identity
        knowledge.add(Implication(Box[i][0], Not(Box[i][1])))
        knowledge.add(Implication(Box[i][1], Not(Box[i][0])))
        if Word[i] != None:
            if isinstance(Word[i], list): # if the person says multiple words, we use list to store them
                for w in Word[i]:
                    # A knight says true word
                    knowledge.add(Implication(Box[i][0], w))
                    # A knave says false word
                    knowledge.add(Implication(Box[i][1], Not(w)))
            else: # the person only says one word
                # A knight says true word
                knowledge.add(Implication(Box[i][0], Word[i]))
                # A knave says false word
                knowledge.add(Implication(Box[i][1], Not(Word[i])))
    return knowledge



# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
)
Word[0] = And(AKnight, AKnave)
knowledge0 = ConstructKnowledge(1)



# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
)
Word[0] = And(AKnave, BKnave)
Word[1] = None
knowledge1 = ConstructKnowledge(2)



# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
)
Word[0] = Or(And(AKnight, BKnight), And(AKnave, BKnave))
Word[1] = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = ConstructKnowledge(2)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
)
AWord1 = Symbol("A said:\"I am a knight\"")
AWord2 = Symbol("A said:\"I am a knave\"")

Word[0] = None # we have no idea what A says right now
Word[1] = [AWord2, CKnave]
Word[2] = AKnight

knowledge3 = ConstructKnowledge(3)

# A says either one
knowledge3.add(Or(AWord1, AWord2))
knowledge3.add(Implication(AWord1, Not(AWord2)))
knowledge3.add(Implication(AWord2, Not(AWord1)))
# if A is a Knight, he says true word
knowledge3.add(Implication(And(AWord1, AKnight), AKnight))
knowledge3.add(Implication(And(AWord2, AKnight), AKnave))
# if A is a Knave, he says false word
knowledge3.add(Implication(And(AWord1, AKnave), Not(AKnight)))
knowledge3.add(Implication(And(AWord2, AKnave), Not(AKnave)))




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

import termcolor

from logic import *

#define the initial symbols
mustard = Symbol("ColMustard")
plum = Symbol("ProfPlum")
scarlet = Symbol("MsScarlet")
characters = [mustard, plum, scarlet]

ballroom = Symbol("ballroom")
kitchen = Symbol("kitchen")
library = Symbol("library")
rooms = [ballroom, kitchen, library]

knife = Symbol("knife")
revolver = Symbol("revolver")
wrench = Symbol("wrench")
weapons = [knife, revolver, wrench]

symbols = characters + rooms + weapons


def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            print(f"{symbol}:YES:::::::::::::::::::::::::::::::::::::::::::")
        #not sure the symbol is false (not sure if it's contained in the envelope)
        #does the model not contain the symbol? (second not)
        #are we not sure? (first not)
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: MAYBE")
        else:
            print(f"{symbol}: No")

#initial knowledge
# There must be a person, room, and weapon.
knowledge = And(
    Or(mustard, plum, scarlet),
    Or(ballroom, kitchen, library),
    Or(knife, revolver, wrench)
)

#we know it's not the mustard card, revolver, kitchen
knowledge.add(Not(mustard))
knowledge.add(Not(revolver))
knowledge.add(Not(kitchen))

#someone made a guess (assume not completely random)
#so we know that at least one card is not the envelope
knowledge.add(Or(
    Not(scarlet), Not(library), Not(wrench)
))

#someone shows me the plum card
knowledge.add(Not(plum))
knowledge.add(Not(ballroom))

check_knowledge(knowledge)

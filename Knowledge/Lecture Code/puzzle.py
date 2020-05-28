from logic import *

people = ["Gilderoy", "Pomona", "Minerva", "Horace"]
houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

symbols = []

#starts defining all logic statements

knowledge = And()

#create unique symbols
for person in people:
    for house in houses:
        symbols.append(Symbol(f"{person}{house}"))

# Each person belongs to a house.
# so they either belong to gryff, huffle, ravenclaw or Slytheron
for person in people:
    knowledge.add(Or(
        Symbol(f"{person}Gryffindor"),
        Symbol(f"{person}Hufflepuff"),
        Symbol(f"{person}Ravenclaw"),
        Symbol(f"{person}Slytherin")
    ))

# Only one house per person.
for person in people:
    for h1 in houses:
        for h2 in houses:
            if h1 != h2:
                knowledge.add(
                    # if they are in house 1, then they are not in house 2
                    Implication(Symbol(f"{person}{h1}"), Not(Symbol(f"{person}{h2}")))
                )

# Only one person per house.
for house in houses:
    for p1 in people:
        for p2 in people:
            if p1 != p2:
                knowledge.add(
                    # if a person is in this house, no one else can be in this house
                    Implication(Symbol(f"{p1}{house}"), Not(Symbol(f"{p2}{house}")))
                )








#gilderoy is either in Gryffindor or ravenclaw
knowledge.add(Or(
    Symbol("GilderoyGryffindor"), 
    Symbol("GilderoyRavenclaw")     
))

#pomona does not belong in slytherin
knowledge.add(Not(
    Symbol("PomonaSlytherin")
))

#minerva belongs to gryffindor
knowledge.add(Symbol("MinervaGryffindor"))













#displays who is in what house
for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)

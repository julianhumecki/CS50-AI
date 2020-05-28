import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        #maps a variable to all the words it can have
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        #rint("Before node consistency...")
        #self.print_domains()
        self.enforce_node_consistency()
        #print("After node-consistency, before ac3...")
        #self.print_domains()

        self.ac3()
        #print("After ac3 ....")
        #self.print_domains()

        return self.backtrack(dict())
        #return None
    def print_domains(self):
        for domain in self.domains:
            print(f" Var: {domain} Domain: {self.domains[domain]}")
        return 
    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        #eliminate words that do not equal our variable's length

        for var in self.crossword.variables:
            domains = self.domains[var].copy()
            for word in domains:
                if not var.length == len(word):
                    self.domains[var].remove(word)

        return

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        #for all possible words
        domains = self.domains[x].copy()
        for X in domains:
            failed_overlaps = 0
            for Y in self.domains[y]:
            #find the overlap of the two variables
               # print(f"X: {X}")
                #print(f"Y: {Y}")
                overlap = self.crossword.overlaps[x, y] 
                #if there is an overlap
                if not overlap == None:
                    #if there is a conflict
                    #print("Overlap...")   
                    if not X[overlap[0]] == Y[overlap[1]]:
                        # remove word X from x's domain of words
                        #print("No overlap yet")
                        failed_overlaps = failed_overlaps + 1
                    else:
                        #print("Successful overlap")
                        break
            #if in x's domain works with y's domain 
            #no possible value works
            #remove it
            if failed_overlaps == len(self.domains[y]):
                self.domains[x].remove(X)
                revised = True
                #print("Overlaps: None")

        return revised
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        all_arcs = list()
        #assign arcs properly
        if arcs == None:
            all_arcs = self.get_all_arcs()
        else:
            all_arcs = arcs.copy()

        all_arcs = list(all_arcs)
        #print(f"All arcs: {all_arcs}")
        #print(f"All Arcs Len: {len(all_arcs)}")
        while not len(all_arcs) == 0:
            #print(type(all_arcs))
            (x,y) = all_arcs.pop(0)
            #print(f"X: {x}, Y: {y}")

            if self.revise(x, y):
                #print("Revised...")
                #print(f"X's domain: {self.domains[x]}")
                #if size of x domains is 0
                if len(self.domains[x]) == 0:
                    #print("Here..")
                    return False

                neighbors = self.crossword.neighbors(x)
                neighbors.remove(y) 
                for z in neighbors:
                    #print(f"Appended: {z,x}")
                    #avoid duplicate conditions
                    if not (z,x) in all_arcs:
                        all_arcs.append((z, x))
            #else:
                #print("No revision")

        return True

    def get_all_arcs(self):

        all_arcs = set()
        #loop over all pairs of variables
        #check if they overlap
        #if they do, get that pair's intersection and add it to the set
        for var1 in self.crossword.variables:
            for var2 in self.crossword.variables:
                #if they don't equal each other
                if not var1 == var2:
                    value = self.crossword.overlaps[var1, var2]
                    if not value == None:
                        #if not (var1, var2) in all_arcs and not (var2, var1) in all_arcs:
                        all_arcs.add((var1, var2))
                        

        return all_arcs


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.domains)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #loop over all variables
        for var in assignment:
            for var2 in assignment:
                #check for overlap
                if not var == var2:
                    overlap = self.crossword.overlaps[var, var2]
                    if not overlap == None:
                        #if the letters conflict
                        #make sure the letters dont conflict
                        # if the overlapping characters don't match
                        #return False
                        if not assignment[var][overlap[0]] == assignment[var2][overlap[1]]:
                            return False
                    if assignment[var] == assignment[var2]:
                        #no duplicate assignments allowed
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        list_vars_domain = list()
        
        mapping = dict()
        #print(f"Var: {var}")
        #if variable not assigned already
        if not var in assignment:
            #all possible values of the variable
            all_options = self.domains[var].copy()
            
            for option in all_options:
                #print(f"Options: {option}")
                count = 0
                #loop over all unassigned vars
                for var2 in self.domains:
                    #if var doesnt equal var2 and
                    #var2 is unassigned
                    if not var == var2 and not var2 in assignment:
                        #if var's option is included in var2's domain, increase the count
                        if option in self.domains[var2]:
                            #increase count of removed
                            count += 1
                #insert the option
                #print(f"Count {count}")
                mapping[option] = count
        #sorted dictionary in list form by lowest values

        
        #print(f"Mapping: {mapping}")
        sorted_tuples = sorted(mapping.items(), key=lambda x: x[1])
        for i, j in sorted_tuples:
            list_vars_domain.append(i)
        #print(f"Var: {var} Var domain: {list_vars_domain}")
        return list_vars_domain

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        min_domains = []
        min_len = 10000
        for var in self.domains:
            #if not a part of assignment
            if not var in assignment:
                options = self.order_domain_values(var, assignment)
                if len(options) < min_len:
                    min_domains = []
                    min_domains.append(var)
                    min_len = len(options)
                #if there's a tie
                elif len(options) == min_len:
                    min_domains.append(var)
        #now you have a list of all the minimum length domain values
        if len(min_domains) == 1:
            return min_domains[0]

        #loop over all options and return the one with the most neighbours
        most_neighbors = -1
        most_var = []
        for var in min_domains:
            neighbor_count = len(self.crossword.neighbors(var))
            if neighbor_count > most_neighbors:
                most_var = var
                most_neighbors = neighbor_count

        #print(f"Most var: {most_var}")
        return most_var


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        #base case of the assignments being completed
        if self.assignment_complete(assignment):
            return assignment
        #get an unassigned variable
        var = self.select_unassigned_variable(assignment)
        #get all values in our domain
        for value in self.domains[var]:
            assignment_copy = assignment.copy()
            assignment_copy[var] = value
            #if there are no violations
            if self.consistent(assignment_copy):
                result = self.backtrack(assignment_copy)
                if not result == None:
                    return result

        return None 


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

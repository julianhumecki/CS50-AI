import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        new_set = set()
        #print("In known_mines: ")
        #if count == set.length, then all cells are mines
        if self.count == len(self.cells):
            #print(f"Not empty: len: {len(self.cells)}")
            return self.cells
        
        #print("EMpty")
        return new_set

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        new_set = set()
        if self.count == 0:
            return self.cells
        else:
            return new_set

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count = self.count - 1
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #when adding new info about the sentences, loop over them all
        self.moves_made.add(cell)
        self.safes.add(cell)

        print(f"Moves made: {self.moves_made}")
        print(f"Mines Known Before: {self.mines}")
        print(f"Safes Before: {self.safes}")
        print(f"Knowledge len {len(self.knowledge)}")

        set_cells = set()
        count_copy = count
        #check to see if on board and if surrounding cells have not been played yet
        #first add a set of all the surrounding positions and a count, then loop over all sets
        #and check if any of the base cases are met, ie known_safes and known_mines, can also implement deductions
        
        #bottom right
        if (cell[0] + 1) < self.width and (cell[1] + 1) < self.height:
            if not (cell[0] + 1, cell[1] + 1) in self.moves_made:
                #already known to be a mine
                if not (cell[0] + 1, cell[1] + 1) in self.mines:
                    #print(f"Bottom right: {(cell[0] + 1, cell[1] + 1)}")
                    set_cells.add((cell[0] + 1, cell[1] + 1))
                    #count_copy -= 1
        #top right            
        if (cell[0] + 1) < self.width and (cell[1] - 1) >= 0:
            if not (cell[0] + 1, cell[1] - 1) in self.moves_made:
                if not (cell[0] + 1, cell[1] - 1) in self.mines:
                    #print(f"bottom left: {(cell[0] + 1, cell[1] - 1)}")
                    set_cells.add((cell[0] + 1, cell[1] - 1))
                    #count_copy -= 1

        #bottom left
        if (cell[0] - 1) >= 0 and (cell[1] + 1) < self.height:
            if not (cell[0] - 1, cell[1] + 1) in self.moves_made:
                if not (cell[0] - 1, cell[1] + 1) in self.mines:
                    #print(f"top right:{(cell[0] - 1, cell[1] + 1)}")
                    set_cells.add((cell[0] - 1, cell[1] + 1))
                    #count_copy -= 1
        #top left
        if (cell[0] - 1) >= 0 and (cell[1] - 1) >= 0:
            if not (cell[0] - 1, cell[1] - 1) in self.moves_made:
                if not (cell[0] - 1, cell[1] - 1) in self.mines:
                   # print(f"Top left:{(cell[0] - 1, cell[1] - 1)}")
                    set_cells.add((cell[0] - 1, cell[1] - 1))
                    #count_copy -= 1
        #right
        if (cell[0] + 1) < self.width:
            if not (cell[0] + 1, cell[1]) in self.moves_made:
                if not (cell[0] + 1, cell[1]) in self.mines:
                    #print(f"bottom{(cell[0] + 1, cell[1])}:")
                    set_cells.add((cell[0] + 1, cell[1]))
                    #count_copy -= 1
        #left            
        if (cell[0] - 1) >= 0:
            if not (cell[0] - 1, cell[1]) in self.moves_made:
                if not (cell[0] - 1, cell[1]) in self.mines:
                    #print(f"top: {(cell[0] - 1, cell[1])}")
                    set_cells.add((cell[0] - 1, cell[1]))
                    #count_copy -= 1
        #bottom
        if (cell[1] + 1) < self.height:
            if not (cell[0], cell[1] + 1) in self.moves_made:
                if not (cell[0], cell[1] + 1) in self.mines:
                   # print(f"right: {(cell[0] , cell[1]+1)}")
                    set_cells.add((cell[0], cell[1] + 1))
                    #count_copy -= 1
        #top
        if (cell[1] - 1) >= 0:
            if not (cell[0], cell[1] - 1) in self.moves_made:
                if not (cell[0], cell[1] - 1) in self.mines:
                    #print(f"left: {(cell[0], cell[1] - 1)}")
                    set_cells.add((cell[0], cell[1] - 1))
                    #count_copy -= 1

    
        #sentence has been added
        sentence_added = Sentence(set_cells, count)
        #print(f"Sentence added: {sentence_added}")
        self.knowledge.append(sentence_added)
        #mark any addition cells as safe or as mines
        sentence_added_mines = sentence_added.known_mines()
        sentence_added_safes = sentence_added.known_safes()

        if not sentence_added_safes == None:
            #print(f"Safe sets: {sentence_added_safes}")
            
            for safe in sentence_added_safes:
                #if safe is not yet inclued in safes, add it
                if not safe in self.safes:
                    self.safes.add(safe)
                    self.mark_safe(safe)

        if not sentence_added_mines == None:
            #print(f"Mines: {sentence_added_mines}")

            for mine in sentence_added_mines:
                #if mine is not yet inclued in mines, add it
                if not mine in self.mines:
                    self.mines.add(mine)

        #draw additional info
        
        temp = []
        print(f"Len: {len(self.knowledge)}");
        
        for i in range(len(self.knowledge)):
            for j in range(i+1, len(self.knowledge)):

                #get both set differences
                #check if non zero len and add to knowledge base 
                
                

                #print(f"I Set: {self.knowledge[i].cells}")
                #print(f"J Set: {self.knowledge[j].cells}")
                diff1 = set()
                count = -1
               # print(f"Knowledge i count: {self.knowledge[i].count}")
               # print(f"Knowledge j count: {self.knowledge[j].count}")

                if len(self.knowledge[i].cells) >= len(self.knowledge[j].cells):
                    #print("I is superioir")
                    if (self.knowledge[j].cells).issubset(self.knowledge[i].cells):
                        diff1 = self.knowledge[i].cells.difference(self.knowledge[j].cells)
                        count = self.knowledge[i].count - self.knowledge[j].count
                else:
                    #print("J is superior")
                    if (self.knowledge[i].cells).issubset(self.knowledge[j].cells):
                        diff1 =  self.knowledge[j].cells.difference(self.knowledge[i].cells)
                        count = self.knowledge[j].count - self.knowledge[i].count

                if (not count == -1) and (not diff1 == set()):
                    #diff2 = self.knowledge[j].cells.difference(self.knowledge[i].cells)
                    #len2 = self.knowledge[j].count - self.knowledge[i].count
                    #print(f"Diff1: {diff1}")
                    #print(f"Diff2: {diff2}")
                    #print(f"Len1: {count}")
                    #print(f"Len2: {len2}")
                    if len(diff1) > 0:
                        sentence = Sentence(diff1, count)
                        #self.knowledge.append(sentence)
                        if not sentence in temp:
                            #print("hey---------------------------------------")
                            temp.append(sentence)
                            new_safes = sentence.known_safes()
                            new_mines = sentence.known_mines()
                            #add new entries
                            # print(f"safe spots: {new_safes}")
                            # print(f"mines: {new_mines}")
                            # print(f"count: {sentence.count}")
                            for safe in new_safes:
                                #if safe is not yet inclued in safes, add it
                                if not safe in self.safes:
                                    self.safes.add(safe)

                            for mine in new_mines:
                                #if mine is not yet inclued in mines, add it
                                if not mine in self.mines:
                                    self.mines.add(mine)



        #filters out duplicates
        length = len(self.knowledge)

        for t in temp:
            has = False
            for i in range(length):
                #print(f"Temp cells: {t.cells}")
                if t.cells == self.knowledge[i].cells: 
                    has = True
                    break
            if not has:        
                self.knowledge.append(t)


        

        

        #filter all mines that are played
        # for mine in self.mines:
        #     if mine in self.moves_made:
        #         self.mines.remove(mine)

        # #filter out mines from knowledge base
        # for mine in self.mines:
        #     for i in range(len(self.knowledge)):
        #         if mine in self.knowledge[i].cells:
        #             print(f"Mine gone: {mine}")
        #             self.knowledge[i].cells.remove(mine)
        #             self.knowledge[i].count = self.knowledge[i].count - 1


        # #filter the safe moves from mine moves
        # for mine in self.mines:
        #     for safe in self.safes:
        #         if mine in safe:
        #             self.safes.remove(mine)

        #self.knowledge = self.knowledge + temp

        print("knowledge: ----------------------")
        for k in self.knowledge:
            print(f"Cells: {k.cells}")
            print(f"Count: {k.count}")

        #filter the played tiles from our knowledge base
        # for i in range(len(self.knowledge)):
        #     if cell in self.knowledge[i].cells:
        #         #filter out the played tiles
        #         self.knowledge[i].cells.remove(cell)

  #       for i in range(len(self.knowledge)):
  #           for valid in self.safes:
  #               if valid in self.knowledge[i].cells:

  #               #filter out the played tiles
  #                   self.knowledge[i].cells.remove(valid)

  # #filter out mines from knowledge base
  #       for mine in self.mines:
  #           for i in range(len(self.knowledge)):
  #               if mine in self.knowledge[i].cells:
  #                   print(f"Mine gone: {mine}")
  #                   self.knowledge[i].cells.remove(mine)
  #                   self.knowledge[i].count = self.knowledge[i].count - 1

        print(f"Mines Known After: {self.mines}")
        print(f"Safe After: {self.safes}")
        
        return 
                    
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        print("In safe move -------------------")
        for safe in self.safes:
            if not safe in self.moves_made:
                print(f"Safe move: {safe}")
                print()
                print()
                return safe

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        print("In random move: ----------------------------")
        for i in range(self.width):
            for j in range(self.height):
                #move hasn't been made yet
                if not (i, j) in self.moves_made:
                    #unknown if a mine or not
                    if not (i,j) in self.mines:
                        print(f"Random Move: {(i,j)}")
                        return (i, j)

        return None  


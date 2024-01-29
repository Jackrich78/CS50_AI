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
        if len(self.cells) == self.count:
            # if cells = count of mines all cells are mines
            return set(self.cells)
        else:
            # not enough information to say if a cell is a mine
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        
        # check to see if cell is included in the sentence
        if cell in self.cells:
            # remove the cell from the sentence
            self.cells.remove(cell)
        
            # decrement number of mines left in the sentence
            self.count -= 1

            """
            # potentially part of minisweeper class
            # mark safe cells
            if self.count == 0:
                mark_safe(self.cells)

            # if cell = count then it's a mine
            if len(self.cells) == self.count:
                self.cells.remove(cell)
            """
        
        # if cell is not in the sentence then no action needed
        else:
            return 

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # check to see if cell is included in the sentence
        if cell in self.cells:
            # remove the cell from the sentence
            self.cells.remove(cell)
        
        # if cell is not in the sentence then no action needed
        else:
            return 
"""
# TESTING BLOCK
sentence = Sentence({(0, 0), (0, 1), (1,0)}, 1)

print(f"Before: {sentence}")

# sentence.mark_mine((0, 0))
sentence.mark_safe((0, 1))

print(f"After: {sentence}")
assert (0 , 1) not in sentence.cells
assert sentence.count == 1
"""

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
        # mark cell as a move made
        self.moves_made.add(cell)

        # mark cell as safe
        self.safes.add(cell)
        for sentence in self.knowledge:
            #debugging
            print(f"Object type: {type(sentence)}")  # Should output: <class '__main__.Sentence'>
            print(f"Does object have 'mark_safe'? {'mark_safe' in dir(sentence)}")  # Should output: True
            sentence.mark_safe(cell)

        # add sentence to knowledge base
        neighbours = set()
        i, j = cell

        # nexted loop to get positions around the cell
        for dif_i in [-1, 0, 1]:
            for dif_j in [-1, 0, 1]:
                # skip cell itself
                if dif_i == 0 and dif_j == 0:
                    continue
                ni, nj = dif_i + i ,dif_j + j
            
                # if cell is within the board bounds:
                if ni < self.height and nj < self.width:
                    #if position is not in self.safes or self.mines:
                    if (ni, nj) not in self.safes and (ni, nj) not in self.mines:
                        neighbours.add((ni, nj))
            
        # add new sentence with neighbours and count
        if neighbours:
            new_sentence = Sentence(neighbours, count)
            # add new sentence to self.knowledge
            self.knowledge.append(new_sentence)

        # set a changed variable to true
        changed = True

        # Update the new knowledge
        while changed is True:
            #set to false but iterate of this if any changed are made
            changed = False

            for sentence in self.knowledge:
                # if count = 0 no mines therfore mark safe
                if sentence.count == 0:
                    for cell in set(sentence.cells):
                        self.mark_safe(cell)
                        changed = True

                # if number of cells = count therefore all mines, mark mines    
                elif len(sentence.cells) == sentence.count:
                    for cell in set(sentence.cells):
                        self.mark_mine(cell)
                        changed = True

                # update sentences in knowledge base
                # Infer new sentences from current ones
                for sentence1 in self.knowledge:
                    for sentence2 in self.knowledge:
                        if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                            #find delta between sentence 1 and 2
                            new_cells = sentence2.cells - sentence1.cells
                            new_count = sentence2.count - sentence1.count

                            #if there are new cells add to the knolwedge base
                            if new_cells:
                                new_sentence = Sentence(new_cells, new_count)
                                if new_sentence not in self.knowledge:
                                    self.knowledge.append(new_sentence)
                                    changed = True

                
                # remove any empty sentences still in the knowledge base
                self.knowledge = [s for s in self.knowledge if len(s.cells) > 0]
        

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # return a safe cell and not already explored
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell

        # if no safe moves return none
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # create a set of all possible moves
        all_cells = set((i, j) for i in range(self.height) for j in range(self.width))

        # exclude already chosen, mines and safe cells
        possible_moves = all_cells - set.moves_made - self.mines - self.safes

        # if there are possible moves choose one at random
        if possible_moves:
            return random.choice(list(possible_moves))

        #else return None
        return None                
    

# Test for MinesweeperAI

# Initialize the AI
ai = MinesweeperAI()

# Scenario 1: Simulate the AI knowing a cell is safe and updating knowledge
print("Scenario 1: Adding knowledge about a safe cell with 1 neighboring mine.")
ai.add_knowledge((1, 1), 1)

# Expected: AI should recognize surrounding cells and infer one is a mine
print("AI Knowledge after Scenario 1:")
for sentence in ai.knowledge:
    print(sentence)

print("AI Knowledge before assert:")
for sentence in ai.knowledge:
    print(sentence)

# Verify the results
assert any(s == Sentence({(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}, 1) for s in ai.knowledge), "Knowledge should contain the sentence with 8 neighbors and 1 mine."

# Scenario 2: Simulate the AI finding another safe cell that allows it to infer a mine
print("\nScenario 2: Adding knowledge about another safe cell that helps infer a mine.")
ai.add_knowledge((0, 0), 0)

# Expected: AI should mark cells around (0, 0) as safe and infer mines based on previous knowledge
print("AI Knowledge after Scenario 2:")
for sentence in ai.knowledge:
    print(sentence)
print("AI Safe cells:", ai.safes)
print("AI Mines:", ai.mines)

# Add more scenarios as needed, especially edge cases and complex situations

# Reminder to validate the changes and ensure the results match expectations
# Assert statements or manual checks can be used to verify the AI's internal state

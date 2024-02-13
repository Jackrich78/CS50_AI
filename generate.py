import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # check length of word variable
        for variable in self.domains:
        
            # initialise set to hold words to be removed
            words_to_remove = set()

            # check each word in variable
            for word in self.domains[variable]:
                # if word doesn't match variable length
                if len(word) != variable.length:
                    words_to_remove.add(word)

            # Remove word
            for word in words_to_remove:
                self.domains[variable].remove(word)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        revised = False
        overlap = self.crossword.overlaps[x, y]


        # find word variables that overlap
        if overlap is not None:
            i, j  = overlap  # i is index x, j is index y
            words_to_remove = set()

            for word_x in self.domains[x]:
                # check if a word in y matches
                if not any(word_x[i] == word_y[j] for word_y in self.domains[y]):
                    words_to_remove.add(word_x)
                
               
            # Remove words fromx's domain for arc consistency
            if words_to_remove:
                revised = True
                for word in words_to_remove:
                    self.domains[x].remove(word)

        return revised    


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        # create a list of arcs
        if arcs is None:
            arcs = []
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    arcs.append((x, y))
        
        while arcs:
            x, y = arcs.pop(0)   # remove first arc from queue
            
            if self.revise(x, y):
                if not self.domains[x]:  # if x is empty return false
                    return False
                for z in self.crossword.neighbors(x) - {y}:  # exclude y from neighbours to avoid adding it back
                    arcs.append((z, x))
        #  return true if all variables are arc consistent
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        # iterate through every variable in the crossword
        for variable in self.crossword.variables:
            # check if variable is not in assignemnt or doesn't exist
            if variable not in assignment or assignment[variable] is None:
                return False
        # assignment complete
        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # check for distinct words
        if len(set(assignment.values())) < len(assignment):
            return False
        
        # check variable in assignment
        for variable, word in assignment.items():
            # check length
            if len(word) != variable.length:
                return False
            
            # check overlap consistency with neighbours
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    # get overlapping  characters
                    overlap = self.crossword.overlaps[variable, neighbor]
                    if overlap is not None:
                        i, j = overlap

                        # if overlap chars doesn't match
                        if word[i] != assignment[neighbor][j]:
                            return False
                        
        # if all checks pass the assignment is consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        def count_constraints(value):
            # intialise constraint count
            constraint_count = 0

            for neighbor in self.crossword.neighbors(var) - set(assignment.keys()):
                overlap = self.crossword.overlaps[var,neighbor]
                if overlap:
                    i, j = overlap
                    # iterate through values in neighbours domain
                    for neighbor_value in self.domains[neighbor]:
                        # if the values at the overlap dont match, increment count
                        if value[i] != neighbor_value[j]:
                            constraint_count += 1
            return constraint_count
    
        # initialise a list
        value_constraints = []

        # create a list of tuples (value, constraint, count)
        for value in self.domains[var]:
            constraint_count = count_constraints(value)
            value_constraints.append((value, constraint_count))
        
        # sort the list by constraint count in assending order
        value_constraints.sort(key=lambda x: x[1])

        # return return just ordered values
        return [value for value, _ in value_constraints]
    

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # initialise list of unassigned variables
        unassigned_vars = []

        # create a list of variables that haven't been assigned a value  yet
        for var in self.crossword.variables:
            if var not in assignment:
                unassigned_vars.append(var)

        # create list of variables based on minimum number of remaining values
        vars_data = []
        for var in unassigned_vars:
            # calculate the number of possible values remaining
            number_remaining_values = len(self.domains[var])
            # calulcated number fo neighbours for the variable
            degree = len(self.crossword.neighbors(var))
            # add to the tuple list
            vars_data.append((var, number_remaining_values, degree))

        # sort variables by MRV then degree
        # sort list byt number of remaining values (asc) then by degree (desc)
        vars_data.sort(key=lambda item: (item[1], -item[2]))

        # return the best variable
        if vars_data:
            best_var = vars_data[0][0]
            return best_var
        else:
            # if there are no unassigned variables left
            return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        # check for complete assignment
        if self.assignment_complete(assignment):
            return assignment  # because a complete assignment is found
        
        # select an unassigned variable
        var = self.select_unassigned_variable(assignment)

        # loop through the variables domain values
        for value in self.order_domain_values(var, assignment):
            # create a copy 
            temp_assignment = assignment.copy()
            temp_assignment[var] = value

            # check if value is consistent with the assignment
            if self.consistent(temp_assignment):
                # recursively call backtrack
                result = self.backtrack(temp_assignment)
                if result is not None:
                    # pass the solution upwards
                    return result
                
            # if not consistent it should automatically backtrack
        
        # return none if no solution found
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
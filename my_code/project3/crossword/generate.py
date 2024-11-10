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
        
        for var, words in self.domains.items():
            remove = set()
            
            # Scrap the words inconsistent with the length of the variable
            for word in words:
                if len(word) != var.length:
                    remove.add(word)
            self.domains[var] -= remove

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        # Get overlap of x & y
        # Overlap represents as (a, b), meaning character indexed a in x and indexed b in y should be eqivalent
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False
        else:
            fix = False
            remove = set()
            
            for x_word in self.domains[x]:
                consistent = False
                for y_word in self.domains[y]:
                    # If there is a choice in y's domain that is consistent with x, then we say it consistent
                    # We just exit the loop because we have found one alternative choice
                    if x_word[overlap[0]] == y_word[overlap[1]]:
                        consistent = True
                        break
                
                # If no alternative choice in y's domain is found, then x_word is not consistent
                # We need to eliminate it from x's domain
                if not consistent:
                    remove.add(x_word)
                
            self.domains[x] -= remove
            # Return `True` if x's domain is revised, otherwise return `False`
            if len(remove) != 0:
                return True
            else:
                return False
            
            
            

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        # Maintain a queue for revise
        queue = list()
        if arcs is None:
            queue = [(x, y) for x in self.crossword.variables for y in (self.crossword.variables - {x}) if x != y and self.crossword.overlaps[x, y] is not None]
        else:
            queue = arcs
        
        # Revise any arcs in queue
        while len(queue) != 0:
            arc = queue[0]
            queue.pop(0)
            if self.revise(*arc):
                # No values remains in domain means no solve for the problem, return `False`
                if len(self.domains[arc[0]]) == 0:
                    return False
                
                # Add all arcs connected to x to queue (except the arc which we're just revising, and arcs already added to queue)
                x = arc[0]
                [queue.append((y, x)) for y in (self.crossword.variables - {x, arc[1]})
                 if self.crossword.overlaps[y, x] is not None and (y, x) not in queue]
                
        return True
                
        
            

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        if len(assignment) == len(self.crossword.variables):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        for var, value in assignment.items():
            # Check length of word
            if len(value) != var.length:
                return False
            
            # Check conflict with neighbor variables (ignore variables not assigned yet)
            neighbors = [neighbor for neighbor in (self.crossword.variables - {var})
                         if neighbor in assignment and self.crossword.overlaps[var, neighbor] is not None]
            
            for neighbor in neighbors:
                x_index, y_index = self.crossword.overlaps[var, neighbor]
                # Check the very crossed character
                if value[x_index] != assignment[neighbor][y_index]:
                    return False
            
            # Check repeated words
            # Utilize the feature of set: set only retains one of repeated values
            if len(set(assignment.values())) != len(assignment):
                return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        # A dict -- key: values in var's domain; value: how many choices ruled out
        values = {value:0 for value in self.domains[var]}
        
        # Neighbors of var, except those already assigned
        neighbors = {neighbor for neighbor in (self.crossword.variables - {var} - set(assignment.keys()))
                     if self.crossword.overlaps[var, neighbor] is not None}
        
        # Calculate the values in dict `values`
        for value in values:
            count = 0
            for neighbor in neighbors:
                if value in self.domains[neighbor]:
                    count += 1
            values[value] = count
        
        # Sort the list of value
        templist = [(k, v) for k, v in values.items()]
        takeSecond = lambda elem: elem[1]
        templist.sort(key=takeSecond)
        
        result = [item[0] for item in templist]
        
        return result
                

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        vars_to_select = list()
        min_value = sys.maxsize
        
        # Search for variable that has the least values in its domain
        for var in (self.crossword.variables - set(assignment.keys())):
            value_count = len(self.domains[var])
            
            if value_count < min_value:
                vars_to_select.clear()
                vars_to_select.append(var)
                min_value = value_count
            
            # If there are multiple variables that have the same size of domains, then just retain them for choosing
            elif value_count == min_value:
                vars_to_select.append(var)
        
        if len(vars_to_select) == 1:
            return vars_to_select[0]
        
        '''If there are multiple variables left for choosing, then conduct degree heuristic algorithm'''
        max_degree_var = (None, -1)
        for var in vars_to_select:
            degree_count = 0
            # Count how many degrees there are
            for v in self.crossword.variables - {var}:
                if self.crossword.overlaps[var, v] is not None:
                    degree_count += 1
            
            # Update if (the degree counted) is more than (the degree recorded)
            if degree_count > max_degree_var[1]:
                max_degree_var = (var, degree_count)
        
        return max_degree_var[0]
            


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment.pop(var)
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

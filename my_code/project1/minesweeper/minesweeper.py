import itertools
import random
import copy

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
        
        # if the amount of cells == count, then we assert all these cells are mines 
        if len(self.cells) == self.count:
            return self.cells
        else:
            return set()
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        
        # if count == 0, then we assert all these cells are safe
        if self.count == 0:
            return self.cells
        else:
            return set()
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        
        # if a cell is known to be a mine, then we remove it from the set and decrease the count
        # if there's only ONE cell in cells, then we ignore it, because we don't want to produce void sentence
        if cell in self.cells and len(self.cells) > 1:
            self.cells.remove(cell)        
            self.count -= 1
        return
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        
        # if a cell is known to be safe, then I simply remove it from the set
        # if there's only ONE cell in cells, then we ignore it, because I don't want to produce void sentence
        if cell in self.cells and len(self.cells) > 1:
            self.cells.remove(cell)
        return
        raise NotImplementedError


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
        
        # Add known mine to knowledge
        self.knowledge.append(Sentence({cell}, 1))

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
            
        # Add known safe to knowledge
        self.knowledge.append(Sentence({cell}, 0))

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
        
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        # 2) mark the cell as safe
        self.mark_safe(cell)
        
        # 3)
        cells = self.surrounding_cells(cell)
        newSentence = Sentence(cells, count)
        self.knowledge.append(newSentence)
        
        # 5) Here I switch the order of `4)` and `5)`
        #    I want it to figure out new safe and mine cells firstly, and mark them subsequently
        newInfers = list()
        newNewinfers = list()
        tempCells = set()

        # If new-added sentence is easily known(all safes or all mines), then simply tear it apart as infers
        if len(newSentence.known_mines()) > 0:
            tempCells = newSentence.known_mines().copy()
            for tempCell in tempCells:
                self.mark_mine(tempCell)
                newInfers.append(Sentence({tempCell}, 1))
        elif len(newSentence.known_safes()) > 0:
            tempCells = newSentence.known_safes().copy()
            for tempCell in tempCells:
                self.mark_safe(tempCell)
                newInfers.append(Sentence({tempCell}, 0))
        else:
            # Use new-added sentence to infer new sentences
            newInfers = self.infer_sentence(newSentence)
        
        # If newInfer is new to knowledge, then add it to knowledge
        for newInfer in newInfers:
            if not newInfer in self.knowledge:
                self.knowledge.append(newInfer)
        
        # Arrange knowledge before starting deep exploration
        self.unique_knowledge()
        
        # Conduct second infer to explore deeper
        # Use newly-inferred sentences to infer new sentences
        for i in range(8):
            for ni in newInfers:
                newNewinfers = self.infer_sentence(ni)
                
                for newInfer in newNewinfers:
                    if not newInfer in self.knowledge:
                        self.knowledge.append(newInfer)
            newInfers = copy.deepcopy(newNewinfers)
        
        # Arrange knowledge before marking cells
        self.unique_knowledge()
        
        # 4)
        safeCells = set()
        mineCells = set()
        
        # Loop to find all known mines and safes
        for sentence in self.knowledge:
            tempCells = sentence.known_mines()
            if len(tempCells) != 0:
                mineCells |= tempCells
            
            tempCells = sentence.known_safes()
            if len(tempCells) != 0:
                safeCells |= tempCells
        
        # Mark all mines and safes
        for c in mineCells:
            self.mark_mine(c)
        for c in safeCells:
            self.mark_safe(c)
            
        # Delete repetitive sentences from knowledge
        self.unique_knowledge()
        
        return
                
        raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        
        # Get a set of cells, which is a safe cell and has not been made a move
        targetCells = self.safes - self.moves_made
        
        # if there is no certain cells, then return None
        if len(targetCells) == 0:
            return None
        
        # Pick a cell arbitrarily, and make a move on it
        return targetCells.pop()
        
        raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        
        # Get a set of cells, which is NOT a mine cell and has not been made a move
        allCells = set([(x, y) for x in range(self.height) for y in range(self.width)])
        targetCells = allCells - self.moves_made - self.mines
        
        # if there is no certain cells, then return None
        if len(targetCells) == 0:
            return None
        
        # Pick a cell arbitrarily, and make a move on it
        randomCell = (random.randrange(self.height), random.randrange(self.width))
        while(not randomCell in targetCells):
            randomCell = (random.randrange(self.height), random.randrange(self.width))
        return randomCell
    
        raise NotImplementedError

    def surrounding_cells(self, cell):
        """
        Returns a set of cells that surround `cell`
        """
        cells = set()
        x = cell[0]; y = cell[1]
        
        # Recognize valid cells and add them to the set
        for i in range(3):
            if (x - 1 + i) < 0 or (x - 1 + i) > self.height - 1:
                continue
            for j in range(3):
                if (y - 1 + j) < 0 or (y - 1 + j) > self.width - 1:
                    continue
                
                # Ignore the cell itself
                if i == 1 and j == 1:
                    continue
                
                # Add surrouding cells to set
                cells.add((x - 1 + i, y - 1 + j))
        
        return cells
    
    def infer_sentence(self, sentence):
        newSentences = list()

        # if one sentence is a subset of another sentence, then we can infer new sentence
        for s in self.knowledge:
            if s.cells < sentence.cells:
                newSentences.append(Sentence(sentence.cells - s.cells, sentence.count - s.count))
            elif sentence.cells < s.cells:
                newSentences.append(Sentence(s.cells - sentence.cells, s.count - sentence.count))

        return newSentences
    
    def unique_knowledge(self):
        """
        Make the knowledge unique
        """
        uniqueKnowledge = list()
        [uniqueKnowledge.append(item) for item in self.knowledge if item not in uniqueKnowledge]
        self.knowledge = copy.deepcopy(uniqueKnowledge)
    
    
'''def main():
    safe = {(0, 0), (0, 1)}
    explored = {(0, 0), (1, 0)}
    
    to_explore = safe - explored
    print(len(to_explore)) 
if __name__ == "__main__":
    main()'''
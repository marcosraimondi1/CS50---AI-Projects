import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=10, width=10, mines=15):

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
        if len(self.cells) == self.count and self.count != 0:
            return self.cells

        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if len(self.cells) != 0 and self.count == 0:
            return self.cells

        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=10, width=10):

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

    def inRange(self, C):
        x, y = C
        if x >= self.height or y >= self.width:
            return False
        elif x < 0 or y < 0:
            return False
        else:
            return True

    def checkKnown(self):
        #print("Knolwledge: ")
        for sentence in self.knowledge:
            #print("Sentence: ", sentence)
            safes = sentence.known_safes()
            mines = sentence.known_mines()

            s = copy.deepcopy(safes)
            m = copy.deepcopy(mines)
            #print("Safes: ", s)
            #print("Mines: ", m)
            for safe in s:
                self.mark_safe(safe)

            for mine in m:
                self.mark_mine(mine)

        new_knowledge = list(filter(
            lambda sentence: len(sentence.cells) != 0, self.knowledge
        ))
        self.knowledge = new_knowledge
        # print("Safes: ", self.safes)
        # print("Mines: ", self.mines)

    def combinatory(self):
        new_knowledge = []
        for set1 in self.knowledge:
            # print(set1)
            for set2 in self.knowledge:
                # problem!!!
                if set1.cells != set2.cells:
                    if set1.cells.issubset(set2.cells):

                        #print("Set1: ", set1)
                        #print("Set2: ", set2)

                        newer_sentence = Sentence(
                            set2.cells - set1.cells, set2.count - set1.count)

                        #print("NEW SENTENCE: ", newer_sentence)
                        if newer_sentence not in self.knowledge and newer_sentence not in self.knowledge:
                            new_knowledge.append(newer_sentence)

        self.knowledge = self.knowledge + new_knowledge

        # re-check knowns
        self.checkKnown()

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
               Any time we have two sentences set1 = count1 and set2 = count2 
               where set1 is a subset of set2, then we can construct the new sentence
                set2 - set1 = count2 - count1.
        """
        # 1)
        self.moves_made.add(cell)

        # 2)
        self.mark_safe(cell)

        # 3)
        x, y = cell

        cells = set()

        for i in range(-1, 2):
            for j in range(-1, 2):
                C = (x+i, y+j)
                if C in self.mines:
                    count -= 1
                if self.inRange(C) and C != cell and C not in self.safes and C not in self.mines:
                    cells.add(C)
                    # print(C)

        if len(cells) != 0:
            new_sentence = Sentence(cells, count)

            #print("New Sentence: ", new_sentence)
            self.knowledge.append(new_sentence)

        # 4) Check sentences for known safes or mines
        self.checkKnown()

        # 5) Combinatory
        self.combinatory()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.moves_made:
                return safe

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        #print("Mines: ", self.mines)
        for i in range(1000):
            i = random.randint(0, self.height -1)
            j = random.randint(0, self.width -1)
            C = (i,j)
            if C not in self.moves_made and C not in self.mines:
                        return C
        
        for i in range(self.height):
            for j in range(self.width):
                C = (i, j)
                if C not in self.moves_made and C not in self.mines:
                    return C

        return None

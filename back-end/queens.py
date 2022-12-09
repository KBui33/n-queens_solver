import random
import math


class nQueens:
    def __init__(self, n):
        self.n = n
        self.population = []

    def isAttacking(self, pos1, pos2, board):
        # check up, down, left, right, d-left, d-right, u-left, u-right
        # down
        p = (pos1[0]+1, pos1[1])
        while (p[0] < len(board)):
            if (board[p[0]][p[1]] == "Q"):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]+1, p[1])
        # up
        p = (pos1[0]-1, pos1[1])
        while (p[0] >= 0):
            if (board[p[0]][p[1]] == "Q"):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]-1, p[1])
        # left
        p = (pos1[0], pos1[1]-1)
        while (p[1] >= 0):
            if (board[p[0]][p[1]] == "Q"):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0], p[1] - 1)
        # right
        p = (pos1[0], pos1[1] + 1)
        while (p[1] < len(board[p[0]])):
            if (board[p[0]][p[1]] == "Q"):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0], p[1]+1)
        # ul
        p = (pos1[0]-1, pos1[1]-1)
        while (p[0] >= 0 and p[1] >= 0):
            if (board[p[0]][p[1]] == "Q"):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]-1, p[1]-1)
        # ur
        p = (pos1[0]-1, pos1[1] + 1)
        while (p[0] >= 0 and p[1] < len(board[p[0]])):
            if (board[p[0]][p[1]] == "Q"):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]-1, p[1]+1)
        # dl
        p = (pos1[0]+1, pos1[1]-1)
        while (p[0] < len(board) and p[1] >= 0):
            if (board[p[0]][p[1]] == "Q"):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]+1, p[1]-1)
        # dr
        p = (pos1[0]+1, pos1[1] + 1)
        while (p[0] < len(board) and p[1] < len(board[p[0]])):
            if (board[p[0]][p[1]] == "Q"):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]+1, p[1] + 1)
        return False

    def fitness(self, x):
        # x - bit strings of the current board
        # fitness of a board is defined by the number of

        # fitness is defined as the total number of nonattacking pairs
        board = self.boardFromString(x)
        # for every queen, check if they are attacking every other queen
        notattackingpairs = 0
        for i in range(0, len(x)):
            q1 = x[i]
            for j in range(0, len(x)):
                q2 = x[j]
                if (q1 == q2):
                    continue
                if (not self.isAttacking((int(q1), i), (int(q2), j), board)):
                    notattackingpairs += 1
        return notattackingpairs

    def genetic(self, x, y):
        # x, y - bitstring representation of a board

        if (len(x) != len(y)):
            return None
        child = ""
        for i in range(0, len(x)):
            rng = random.randint(0, 9)
            if (rng < 5):
                child += x[i]
            else:
                child += y[i]
        return child

    def mutation(self, x):
        z = random.randint(0, len(x) - 1)
        val = str(random.randint(0, self.n - 1))

        mutated = list(x)
        mutated[z] = val
        return "".join(mutated)

    def boardFromString(self, x):
        # return a list [][] which is the board associated with bitstring x
        board = [[" " for _ in range(self.n)] for _ in range(self.n)]
        # init board

        for i in range(0, len(x)):
            board[int(x[i])][i] = "Q"
        return board

    def boardToString(self, board):
        # Returns a string representation of the board
        bitString = ""
        for i in range(len(board)):
            for j in range(len(board[i])):
                value = board[j][i]
                if (value == "Q"):
                    bitString += str(j)

        return bitString

    def initPopulation(self, size):
        # Initalizes a population

        for _ in range(size):
            initBoard = [[" " for _ in range(self.n)] for _ in range(self.n)]

            for j in range(self.n):
                row = random.randrange(self.n)
                initBoard[row][j] = "Q"

            boardStr = self.boardToString(initBoard)
            self.population.append((boardStr, self.fitness(boardStr)))
        return

    def selectParent(self, pop):
        # for each element in self.population compute and store x=(1, ..., n+1) of w(x) = 2^(-x)
        # Calcs the probability of a population being used for combo
        probabilities = []
        x = 1
        for (k, v) in pop:
            probabilities.append(((k, v), 2**(-x)))
            x += 1
        lottery = random.random()
        prevEntry = None
        for ((k, v), w) in probabilities:
            if (lottery < w):
                if (prevEntry == None):
                    prevEntry = ((k, v), w)
                return prevEntry[0]
            else:
                prevEntry = ((k, v), w)
        return prevEntry[0]

    def solve(self, m):
        # This is the genetic algorithm

        # init population
        self.initPopulation(m)
        op = 0

        while True:
            for (k, v) in self.population:
                if (v == self.n*(self.n-1)):
                    return k
            # selecting the parents should have a higher probability to select higher fitness values
            # we can map each population item to a % change that they will be chosen
            # choose parents based on the above mentioned odds

            # print(f"Current len of pop: {len(self.population)}")

            for i in range(0, m):
                parent1Key = self.selectParent(self.population)[0]
                parent2Key = self.selectParent(self.population)[0]

                # Create the new child from combining the 2 parents
                child = self.mutation(self.genetic(parent1Key, parent2Key))

                # add this child to the population
                self.population.append((child, self.fitness(child)))

            # kill off some k number of entries in the population
            # sorted by highest fitness value first

            k = 0
            sortedDict = sorted(self.population, key=lambda item: item[1])

            for i in range(len(sortedDict)):
                toRemove = sortedDict[i]
                self.population.remove(toRemove)
                print(f"Popped {toRemove}: current list: {self.population}")
                k += 1
                if (k == m):
                    break
            op += 1
            print(f"Finished itr {op}")

        return False


class WallNQueens(nQueens):

    def __init__(self, n, rightWalls, bottomWalls):
        super().__init__(n)
        self.rightWalls = rightWalls
        self.bottomWalls = bottomWalls

    def isAttacking(self, pos1, pos2, board):
        # check up, down, left, right, d-left, d-right, u-left, u-right
        # down
        p = (pos1[0], pos1[1])
        while (p[0] < len(board)):
            if (board[p[0]][p[1]] == "Q" and p != pos1):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            elif (p[0] < len(self.bottomWalls) and self.bottomWalls[p[0]][p[1]] == 1):
                # The queen hits a wall, stop going this direction
                break
            else:
                pass
            p = (p[0]+1, p[1])
        # up
        p = (pos1[0], pos1[1])
        while (p[0] >= 0):
            if (board[p[0]][p[1]] == "Q" and p != pos1):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            elif (p[0] - 1 >= 0 and self.bottomWalls[p[0] - 1][p[1]] == 1):
                # The queen hits a wall, stop going this direction
                break
            else:
                pass
            p = (p[0]-1, p[1])
        # left
        p = (pos1[0], pos1[1])
        while (p[1] >= 0):
            if (board[p[0]][p[1]] == "Q" and p != pos1):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            elif (p[1] - 1 >= 0 and p[1] - 1 < len(self.rightWalls[0]) and self.rightWalls[p[0]][p[1] - 1] == 1):
                # The queen hits a wall, stop going this direction
                break
            else:
                pass
            p = (p[0], p[1] - 1)
        # right
        p = (pos1[0], pos1[1])
        while (p[1] < len(board[p[0]])):
            if (board[p[0]][p[1]] == "Q" and p != pos1):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            elif (p[1] < len(self.rightWalls[0]) and self.rightWalls[p[0]][p[1]] == 1):
                # The queen hits a wall, stop going this direction
                break
            else:
                pass
            p = (p[0], p[1]+1)
        # ul
        p = (pos1[0], pos1[1])
        while (p[0] >= 0 and p[1] >= 0):
            if (board[p[0]][p[1]] == "Q" and p != pos1):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            elif (p[0] - 1 >= 0 and p[1] - 1 >= 0):
                # The queen hits a wall, stop going this direction
                if (self.bottomWalls[p[0] - 1][p[1]] == 1 and
                   self.rightWalls[p[0]][p[1] - 1] == 1):
                   # ┏
                    break
                if (self.bottomWalls[p[0] - 1][p[1]] == 1 and
                   self.bottomWalls[p[0] - 1][p[1] - 1] == 1):
                   # --
                    break
                if (self.rightWalls[p[0]][p[1] - 1] == 1 and
                   self.rightWalls[p[0] - 1][p[1] - 1] == 1):
                   # |
                    break
                if (self.bottomWalls[p[0] - 1][p[1] - 1] == 1 and
                   self.rightWalls[p[0] - 1][p[1] - 1] == 1):
                   # ┙
                    break
            else:
                pass
            p = (p[0]-1, p[1]-1)
        # ur
        p = (pos1[0], pos1[1])
        while (p[0] >= 0 and p[1] < len(board[p[0]])):
            if (board[p[0]][p[1]] == "Q" and p != pos1):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            elif (p[0] - 1 >= 0 and p[1] + 1 < len(self.rightWalls[0])):
                # The queen hits a wall, stop going this direction

                if (self.bottomWalls[p[0] - 1][p[1]] == 1 and
                   self.rightWalls[p[0]][p[1] + 1] == 1):
                   # ┑
                    break
                if (self.bottomWalls[p[0] - 1][p[1]] == 1 and
                   self.bottomWalls[p[0] - 1][p[1] + 1] == 1):
                   # --
                    break
                if (self.rightWalls[p[0]][p[1]] == 1 and
                   self.rightWalls[p[0] - 1][p[1]] == 1):
                   # |
                    break
                if (self.bottomWalls[p[0] - 1][p[1] + 1] == 1 and
                   self.rightWalls[p[0] - 1][p[1]] == 1):
                   # └
                    break
            else:
                pass
            p = (p[0]-1, p[1]+1)
        # dl
        p = (pos1[0], pos1[1])
        while (p[0] < len(board) and p[1] >= 0):
            if (board[p[0]][p[1]] == "Q" and p != pos1):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            elif (p[0] + 1 < len(board) and p[1] - 1 >= 0):
                # The queen hits a wall, stop going this direction
                if (self.bottomWalls[p[0]][p[1]] == 1 and
                   self.rightWalls[p[0]][p[1] - 1] == 1):
                   # └
                    break
                if (self.bottomWalls[p[0]][p[1]] == 1 and
                   self.bottomWalls[p[0]][p[1] - 1] == 1):
                   # --
                    break
                if (self.rightWalls[p[0]][p[1] - 1] == 1 and
                   self.rightWalls[p[0] + 1][p[1] - 1] == 1):
                   # |
                    break
                if (self.bottomWalls[p[0]][p[1] - 1] == 1 and
                   self.rightWalls[p[0] + 1][p[1] - 1] == 1):
                   # ┐
                    break
            else:
                pass
            p = (p[0]+1, p[1]-1)
        # dr
        p = (pos1[0], pos1[1])
        while (p[0] < len(board) and p[1] < len(board[p[0]])):
            if (board[p[0]][p[1]] == "Q" and p != pos1):
                if (p == pos2):
                    return True
                else:
                    # this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            elif (p[0] + 1 < len(board) and p[1] + 1 < len(board[p[0]])):
                # The queen hits a wall, stop going this direction
                if (self.bottomWalls[p[0]][p[1]] == 1 and
                   self.rightWalls[p[0]][p[1]] == 1):
                   # ┙
                    break
                if (self.bottomWalls[p[0]][p[1]] == 1 and
                   self.bottomWalls[p[0]][p[1] + 1] == 1):
                   # --
                    break
                if (self.rightWalls[p[0]][p[1]] == 1 and
                   self.rightWalls[p[0] + 1][p[1]] == 1):
                   # |
                    break
                if (self.bottomWalls[p[0]][p[1] + 1] == 1 and
                   self.rightWalls[p[0] + 1][p[1]] == 1):
                   # ┏
                    break
            else:
                pass
            p = (p[0]+1, p[1] + 1)
        return False

    def fitness(self, x):
        # x - bit strings of the current board
        # fitness of a board is defined by the number of

        # fitness is defined as the total number of nonattacking pairs
        board = self.boardFromString(x)

        # for every queen, check if they are attacking every other queen
        notattackingpairs = 0
        for i in range(0, len(x)):
            q1 = x[i]
            for j in range(0, len(x)):
                q2 = x[j]
                if (not self.isAttacking((int(q1), i), (int(q2), j), board)):
                    notattackingpairs += 1
        return notattackingpairs

    def solve(self, m):
        # init population
        self.initPopulation(m)
        op = 0

        while True:
            for (k, v) in self.population:
                if (v == self.n**2):
                    print(k)
                    return k

            # selecting the parents should have a higher probability to select higher fitness values
            # we can map each population item to a % change that they will be chosen
            # choose parents based on the above mentioned odds
            print(f"Current pop: {self.population}")

            for i in range(0, m):
                parent1Key = self.selectParent(self.population)[0]
                parent2Key = self.selectParent(self.population)[0]

                # Create the new child from combining the 2 parents
                child = self.mutation(self.genetic(parent1Key, parent2Key))

                # add this child to the population
                self.population.append((child, self.fitness(child)))

            # kill off some k number of entries in the population
            # sorted by highest fitness value first

            k = 0
            sortedDict = sorted(self.population, key=lambda item: item[1])

            for i in range(len(sortedDict)):
                toRemove = sortedDict[i]
                self.population.remove(toRemove)
                k += 1
                if (k == m):
                    break

            op += 1
            print(f"Finished itr {op}")

        return False
    pass

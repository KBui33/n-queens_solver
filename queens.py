import random 
import math

class nQueens:
    def __init__(self, n):
        self.n = n
        self.population = []
        self.fitnessPop = {}
        pass
    
    def isAttacking(self, pos1, pos2, board):
        #check up, down, left, right, d-left, d-right, u-left, u-right
        #down
        p = (pos1[0]+1, pos1[1])
        while(p[0] < len(board)):
           # print("down")
            if(board[p[0]][p[1]] == "Q"):
                if(p == pos2):
                    return True
                else:
                    #this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]+1, p[1])
        #up
        p = (pos1[0]-1, pos1[1])
        while(p[0] >= 0):
            # print('up')
            if(board[p[0]][p[1]] == "Q"):
                if(p == pos2):
                    return True
                else:
                    #this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]-1, p[1])
        #left
        p = (pos1[0], pos1[1]-1)
        while(p[1] >= 0):
            # print("left")
            if(board[p[0]][p[1]] == "Q"):
                if(p == pos2):
                    return True
                else:
                    #this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0], p[1] - 1)
        #right
        p = (pos1[0], pos1[1] + 1)
        while(p[1] < len(board[p[0]])):
            # print("right")
            if(board[p[0]][p[1]] == "Q"):
                if(p == pos2):
                    return True
                else:
                    #this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0], p[1]+1)
        #ul
        p = (pos1[0]-1, pos1[1]-1)
        while(p[0] >= 0 and p[1] >= 0):
            # print("ul")
            if(board[p[0]][p[1]] == "Q"):
                if(p == pos2):
                    return True
                else:
                    #this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]-1, p[1]-1)
        #ur
        p = (pos1[0]-1 , pos1[1] + 1)
        while(p[0] >= 0 and p[1] < len(board[p[0]])):
            # print("ur")
            if(board[p[0]][p[1]] == "Q"):
                if(p == pos2):
                    return True
                else:
                    #this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]-1, p[1]+1)
        #dl
        p = (pos1[0]+1,pos1[1]-1)
        while(p[0] < len(board) and p[1] >= 0):
            #print("dl")
            if(board[p[0]][p[1]] == "Q"):
                if(p == pos2):
                    return True
                else:
                    #this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]+1, p[1]-1)
        #dr
        p = (pos1[0]+1, pos1[1] + 1)
        while(p[0] < len(board) and p[1] < len(board[p[0]])):
            #print("dr")
            if(board[p[0]][p[1]] == "Q"):
                if(p == pos2):
                    return True
                else:
                    #this is a different queen blocking this direction, as such stop iterating in this direction
                    break
            else:
                pass
            p = (p[0]+1, p[1] + 1)
        return False
    
    def fitness(self, x):
        # x - bit strings of the current board 
        # fitness of a board is defined by the number of 
 
        #fitness is defined as the total number of nonattacking pairs
        board = self.boardFromString(x)
        #for every queen, check if they are attacking every other queen
        notattackingpairs = 0
        for i in range(0, len(x)):
            q1 = x[i]
            for j in range(0, len(x)):
                q2 = x[j]
                if(q1 == q2):
                    continue
                if(not self.isAttacking((int(q1), i), (int(q2), j), board)):
                    notattackingpairs +=1
        return notattackingpairs

    def genetic(self, x, y):
        #x, y - bitstring representation of a board
        
        if(len(x) != len(y)):
            return None
        child = ""
        for i in range(0, len(x)):
            rng = random.randint(0, 9)
            if(rng < 5):
                child += x[i]
            else:
                child += y[i]
        return child


    def mutation(self, x):
        z = random.randint(0, len(x) - 2)
        val = str(random.randint(0, self.n - 1))
        # mutated = x[:z] + str(val) + x[z+1:]
        mutated = list(x)
        mutated[z] = val
        return "".join(mutated)
    
    
    def boardFromString(self, x):
        #return a list [][] which is the board associated with bitstring x
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
                if(value == "Q"):
                    bitString += str(j)
                    
        return bitString
        
    def initPopulation(self, size):
        # Initalizes a population 

        for _ in range(size):
            initBoard = [["0" for _ in range(self.n)] for _ in range(self.n)]

            for j in range(self.n):
                row = random.randrange(self.n)
                initBoard[row][j] = "Q"
                
            # print('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in initBoard]))
            boardStr = self.boardToString(initBoard)
            print(boardStr)
            self.population.append((boardStr, self.fitness(boardStr)))
        return 

    def selectParent(self, pop):
        #for each element in self.population compute and store x=(1, ..., n+1) of w(x) = 2^(-x)
        # Calcs the probability of a population being used for combo
        probabilities =[]
        x=1
        for (k, v) in pop:
            probabilities.append(((k, v), 2**(-x)))
            x+=1
        lottery = random.random()
        prevEntry = None
        for ((k, v), w) in probabilities:
            if(lottery < w):
                if(prevEntry == None):
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
                
        #m = self.population.items()
        while True: 
            for (k, v) in self.population:
                if(v == self.n*(self.n-1)):
                    return k
            #selecting the parents should have a higher probability to select higher fitness values
            #we can map each population item to a % change that they will be chosen
            #choose parents based on the above mentioned odds
            #for i in range(0, m) self.population[i][0], self.population[i][1]

            # print(f"Current len of pop: {len(self.population)}")

            for i in range(0, m):
                parent1Key = self.selectParent(self.population)[0]
                parent2Key = self.selectParent(self.population)[0]
                #[0.5*f1, 0.25*f2, 0.1225*f3, 0.6121*f4, ...] = 1
                # print(f"Parent 1: {parent1Key}, Parent 2: {parent2Key}")
                
                # Create the new child from combining the 2 parents 
                child = self.mutation(self.genetic(parent1Key, parent2Key))
                
                # print(f"New Child: {child}")
                #add this child to the population
                self.population.append((child, self.fitness(child)))
    
            #kill off some k number of entries in the population
            #sorted by highest fitness value first
            # print(f"New pop len: {len(self.population)}")
            # print(f"Population inside: ${self.population}")

            k = 0
            sortedDict = sorted(self.population, key=lambda item: item[1])
            # print(sortedDict)


            for i in range(len(sortedDict)):
                toRemove = sortedDict[i]
                self.population.remove(toRemove)
                print(f"Popped {toRemove}: current list: {self.population}")
                k+= 1
                if(k == m): break
            op += 1
            print(f"Finished itr {op}")

        return False 


print(f"FINAL ANS: {nQueens(10).solve(5)}")
# n=20
# m= 4 # inital population size
# make random bitstrings at size n, with rajndom queens in them 
# M = [12320312031231, (), (), ()]

# n=4
# 0000, 0001, 0002, 0003
# 1/4, 1/3, 1/3, 1/3
# n = 4
# choose n/2 elements in M and perform genetic()
# pop+= m(g(0002, 0001))
# pop+= m(g(0002, 0003))

# kill the n/2 least fit in population

""""
Q000
00Q0
0Q00
000Q

d[0][0] attacks d[1][1]
d[1][1] attacks d[0][0]
d[1][1] attacks d[2][2]
d[2][2] attacks d[1][1]
d[2][2] attacks d[3][3]
d[3][3] attacks d[2][2]

0123
1221 

| if the sum of this string is 0, then we have a true solution

if f[x] == '0000':
    add to true solutions
    
    
00000
00000
00000
00000
00000

"""""
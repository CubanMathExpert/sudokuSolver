from aima3.search import *
import random

class Sudoku(Problem):
    def __init__(self, initConflictCount, goal=None):
        self.initConflictCount = initConflictCount
    
    def actions(self, state):
        actions_possibles = []
        #pick random box in state
        randBox = random.choice(state)
        def swap(box, p1, p2):
            #p1,p2 are indices of boxes
            while p1 == p2:
                p2 = random.randint(0,8)
            temp = box[p1]
            box[p1] = box[p2]
            box[p2] = temp
        swap(randBox, random.randint(0,8), random.randint(0,8))
        actions_possibles = state
        return actions_possibles

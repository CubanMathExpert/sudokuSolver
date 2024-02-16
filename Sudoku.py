from aima3.search import *
import random
import copy

class Sudoku(Problem):
    def __init__(self, initConflictCount, goal=None):
        self.initConflictCount = initConflictCount #amount of conflicts at the begining
    
    def actions(self, state, initial_empty_puzzle):
        actions_possibles = []
        potential_state = copy.deepcopy(state)
        def swap(current_state, box,  s1, s2):
            temp = current_state[box][s1]
            current_state[box][s1] = current_state[box][s2]
            current_state[box][s2] = temp
        for b in range(0,9):#for all the boxes
            for i in range(0, 9):#square 1 index
                for j in range(0,9):#square 2 index
                    if i >= j:
                        continue
                    if (potential_state[b][i] == initial_empty_puzzle[b][i] or
                        potential_state[b][j] == initial_empty_puzzle[b][j]):
                        continue
                    else:
                        swap(potential_state, b, i , j)
                        actions_possibles.append(potential_state)
                        potential_state = copy.deepcopy(state)
        return actions_possibles
    
    def result(self, state, action):
        return action


                                
            

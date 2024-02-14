from aima3.search import *

class Sudoku(Problem):
    def __init__(self, initial, goal=None):
        self.initial = initial
    
    def actions(self, state):
        return super().actions(state)
from aima3.search import *
import copy

class Sudoku(Problem):
    def __init__(self, empty_initial_problem, goal=None):
        super().__init__(list([None] * 9))
        self.empty_initial_problem = empty_initial_problem
    
    def actions(self, state): #initial empty puzzle contient le puzzle sans le random fill
        actions_possibles = []
        potential_state = copy.deepcopy(state)
        
        for b in range(0,9):#for all the boxes
            for i in range(0, 9):#square 1 index
                for j in range(0,9):#square 2 index
                    if i >= j:
                        continue
                    if (potential_state[b][i] == self.empty_initial_problem[b][i] or
                        potential_state[b][j] == self.empty_initial_problem[b][j]):
                        continue
                    else:
                        actions_possibles.append((b,i,j))
        return actions_possibles
    
    def result(self, state, action):
        #no need to extract from state action alreayd takes into consideration
        #all possible next states for state
        new_state = copy.deepcopy(state)
        box, id1, id2 = action[0], action[1], action[2]
        def swap(current_state, box,  s1, s2):
            temp = current_state[box][s1]
            current_state[box][s1] = current_state[box][s2]
            current_state[box][s2] = temp
        
        swap(new_state, box, id1, id2)

        return new_state
    
    def goal_test(self, state):
        if any(0 in row for row in state):
            return False
        for i in range(0,9):
            if len(set(state[i])) != 9 or len(set(state[i][j] for j in range(0,0))) != 9:
                return False
        return True

    def value(self, state):
        #check all the conflicts in the grid for current state
        result = 0
        current_state = copy.deepcopy(state)
        all_row_container = [
            current_state[0][0:3] + current_state[1][0:3] + current_state[2][0:3],
            current_state[0][3:6] + current_state[1][3:6] + current_state[2][3:6],
            current_state[0][6:9] + current_state[1][6:9] + current_state[2][6:9],
            current_state[3][0:3] + current_state[4][0:3] + current_state[5][0:3],
            current_state[3][3:6] + current_state[4][3:6] + current_state[5][3:6],
            current_state[3][6:9] + current_state[4][6:9] + current_state[5][6:9],
            current_state[6][0:3] + current_state[7][0:3] + current_state[8][0:3],
            current_state[6][3:6] + current_state[7][3:6] + current_state[8][3:6],
            current_state[6][6:9] + current_state[7][6:9] + current_state[8][6:9]
        ]

        
        all_col_container = [] #contains all the columns
        for col in range(0,9):
            column = []
            for row in all_row_container:
                column.append(row[col])
            all_col_container.append(column)
            column = []

        def check_conflicts(container):
            result = 0
            for row in container:
                s = set()
                for num in row:
                    if num in s:
                        result += 1
                    else: s.add(num)
            return result
        #check for conflicts in rows and columns
        result += check_conflicts(all_col_container)
        result += check_conflicts(all_row_container)
        return -result




        

        


                                
            

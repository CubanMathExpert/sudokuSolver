from aima3.search import *
from Sudoku import Sudoku

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

digits   = '123456789'
rows     = 'ABCDEFGHI'
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])
units = dict((s, [u for u in unitlist if s in u])
            for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
            for s in squares)

################ Unit Tests ################

def test():
    "A set of tests that must pass."
    assert len(squares) == 81
    assert len(unitlist) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                               ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                               ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                                   'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                                   'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')

################ Parse a Grid ################

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False ## (Fail if we can't assign d to square s.)
    return values

def parse_grid_list(grid):
    reorganizedGrid = [grid[0:3]+grid[9:12]+grid[18:21],
                       grid[3:6]+grid[12:15]+grid[21:24],
                       grid[6:9]+grid[15:18]+grid[24:27],
                       grid[27:30]+grid[36:39]+grid[45:48],
                       grid[30:33]+grid[39:42]+grid[48:51],
                       grid[33:36]+grid[42:45]+grid[51:54],
                       grid[54:57]+grid[63:66]+grid[72:75],
                       grid[57:60]+grid[66:69]+grid[75:78],
                       grid[60:63]+grid[69:72]+grid[78:81]]
    return reorganizedGrid

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    #assert len(chars) == 81
    return dict(zip(squares, chars))

################ Constraint Propagation ################

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                 return False
    return values

################ Display as 2-D grid ################

def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else ''))
                      for c in cols)
        if r in 'CF': print(line)

################ Search ################

def solve(grid): 
    return search(parse_grid(grid))

def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    #n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    #return some(search(assign(values.copy(), s, d)) for d in values[s])
    
    #random square and digits-------------
    s = random.choice(squares)
    return some(search(assign(values.copy(), s, random.choice(values[s]))) for d in values[s])

################ heuristics ################


        

################ hill climbing search ################

#fill the 3x3 squares with random numbers to start
def random_fill_generator(values):
    allSquareGroups = unitlist[18:27]
    allSquareGroupsValues = []
    for g in allSquareGroups:
        groupValues = []
        l = [str(i) for i in range(1,10)]
        #first put all initial values
        for s in g:
            if len(values[s]) == 1:
                groupValues.append(values[s])
                l.remove(values[s])
            elif len(values[s]) != 1:
                groupValues.append('')
        # now fill the values that havn't been assigned
        for i in range(0,9):
            if groupValues[i] == '':
                groupValues[i] = random.choice(l)
                l.remove(groupValues[i])
        allSquareGroupsValues.append(groupValues)
    return allSquareGroupsValues

################ Utilities ################

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

def from_file(filename, sep='\n'):
    with open(filename, 'r') as file:
        return file.read().strip().split(sep)

def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq

################ System test ################

import time, random

def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def time_solve(grid):
        start = time.process_time()
        values = solve(grid)
        t = time.process_time()-start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print ('(%.2f seconds)\n' % t)
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print ("Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times)))

def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)

def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    values = dict((s, digits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
    return random_puzzle(N) ## Give up and make a new puzzle

def main():

    grid1 = '48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....'
    initial_empty = parse_grid_list(grid1)

    max_iteration = 1
    valeurs_etats_finales = []
    solutions = []
    
    #HILL_CLIMBING
    """for i in range(0,max_iteration):
        sudokuProblem = Sudoku(initial_empty)
        sudokuProblem.initial = random_fill_generator(parse_grid(grid1))
        #etat_final = hill_climbing(sudokuProblem)
        etat_final = simulated_annealing(sudokuProblem, exp_schedule(10, 0.99, 1000))

        valeur = sudokuProblem.value(etat_final)
        valeurs_etats_finales.append(valeur)
        
        if valeur == 0:
            solutions.append(etat_final)"""
    
    # ANNEALING
    sudokuProblem = Sudoku(initial_empty)
    sudokuProblem.initial = random_fill_generator(parse_grid(grid1))
    etat_final = simulated_annealing(sudokuProblem, exp_schedule(10, 0.99, 1000))

    valeur = sudokuProblem.value(etat_final)
    valeurs_etats_finales.append(valeur)
        
    if valeur == 0:
        solutions.append(etat_final)



    print(f"Apres {max_iteration} essaies, nous avons trouve {len(solutions)} solutions, et le max des valeurs"
          f" obtenues a ete {max(valeurs_etats_finales)}.")
    #parse into boxes

    

    #print(squares)
    

    #solve_all(from_file('100sudoku.txt'), '100sudokus', None)
    #solve_all(from_file('hard.txt'), 'hard', None)
    #solve_all(from_file('top95.txt'), 'top95', None)
    #solve_all([random_puzzle() for _ in range(16000)], 'Rando', 201)


if __name__ == '__main__':
    main()

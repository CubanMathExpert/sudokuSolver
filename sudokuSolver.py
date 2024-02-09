from aima3.search import *

#columns 1-9, rows A-I, unit is (row,col,box)
#peers of a square are all squares in
#its unit

def cross(A, B):
    #Cross product of elements in A and elements in B
    return [a+b for a in A for b in B]

#-----------------------------
def test():
    "A set of unit tests."
    assert len(squares) == 81
    assert len(unitList) == 27
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 20 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print('All tests pass.')

digits = '123456789'
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitList = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs,cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])

#unitList contains all col, row and box
#units is the square with all his peers 
units = dict((s, [u for u in unitList if s in u]) for s in squares)
peers = dict((s, set(sum(units[s],[])) - set([s])) for s in squares)

def parse_grid(grid):
    #convert grid to a dict of possible values {square : digits}
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    return values

def grid_values(grid):
    #convert grid into a dict of {square: char} with '0' or '.' for empties
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))

#def assign(values, s, d):
    #

def main():
    #print(squares)
    #print(units)
    #print(peers)
    test()


if __name__ == '__main__':
    main()

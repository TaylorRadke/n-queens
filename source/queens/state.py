from random import randrange

class Queen(tuple):
    """A class inherited from tuple to redefine how tuples are compared to only check for queen row, column and not if moved"""
    def __init__(self,tup):
        super().__init__()
    
    def __eq__(self,other):
        return (self[0] == other[0] and self[1] == other[1])

class STATE(object):
    """STATE is a class used to hold states of the n-queens positions
    stored as tuple derived queen piece (row,column,moved) on n * n board"""

    def __init__(self,n,initial_state):
        self.n = n
        self.state = initial_state
        self.actions = []
        if self.state == None:
            self.state = []
            self.create_random_initial_state()
    
        self.queen_state_space = self.enumerate_queen_state_space()
        self.state_space = self.enumerate_state_space()
        self.state_row_map, self.state_col_map, self.queen_row_map, self.queen_col_map = self.map_states() 

    def __eq__(self,other):
        return self.state in all(other.get_state())

    def print_state(self):
        q_state = self.queen_state_space
        for i in range(self.n):
            for j in range(self.n):
                if Queen((i,j)) in q_state:
                    print("Q",end=" ")
                else:
                    print("_",end=" ")
                if j == self.n-1:
                    print("\n")

    def get_state(self):
        return self.state
    
    def set_state(self,new_state):
        self.state = new_state
        self.enumerate_queen_state_space()

    def get_n(self):
        return self.n

    def create_random_initial_state(self):
        if len(self.state) == self.n:
            return self.enumerate_queen_state_space()

        row = randrange(0,self.n)
        column = randrange(0,self.n)

        if (row,column,False) not in self.state:
            self.state.append((row,column,False))

        self.create_random_initial_state()

    def enumerate_state_space(self):
        state_space = []
        n = self.n
        #generate n * n of queens from (0,0) to (n,n)
        for i in range(n):
            for j in range(n):
                # Don't add a state where a queen already is
                if Queen((i,j)) not in self.queen_state_space:
                    state_space.append((i,j))
        return state_space

    def enumerate_queen_state_space(self):
        return [Queen(i) for i in self.state]

    def map_states(self):
        states = self.state_space
        queens = self.state

        map_state_space_rows = [[] for i in range(self.n)]
        map_state_space_cols = [[] for i in range(self.n)]

        map_queen_rows = [[] for i in range(self.n)]
        map_queen_cols = [[] for i in range(self.n)]

        for i in states:
            map_state_space_rows[i[0]].append(i[1])
            map_state_space_cols[i[1]].append(i[0])

        for i in queens:
            map_queen_rows[i[0]].append(i[1])
            map_queen_cols[i[1]].append(i[0])

        return map_state_space_rows,map_state_space_cols,map_queen_rows,map_queen_cols

    def queens_diagonal(self,a,b):
            row_diff = abs(a[0] - b[0])
            col_diff = abs(a[1] - b[1])

            if row_diff == col_diff:
                return True
            else:
                return False

    def state_in_conflict(self):
        """Check if self state in conflict, returns True when any queen 
        can attack any other, otherwise returns False(goal reached)"""

        # Check rows/columns in conflict

        for i in range(0,len(self.state)-1):
            for j in range(i+1,len(self.state)):
                #Check Rows in conflict
                if self.state[i][0] == self.state[j][0]:
                    return True
                #Check Columns in conflict
                elif self.state[i][1] == self.state[j][1]:
                    return True
                #Check Diagonals in conflict
                else:
                    if self.queens_diagonal(self.state[i],self.state[j]):
                        return True
        return False

    def row_move_blocked(self,row,curr_col,new_col):
        """Check if left or right move is blocked by another queen"""
        for i in self.queen_row_map[row]:
            # Left move blocked
            if i > new_col and i < curr_col:
                print("Blocked left")
                return True
            # Right move blocked
            elif i < new_col and i > curr_col:
                print("Blocked right")
                return True
        return False

    def col_move_blocked(self,col,curr_row,new_row):
        """Check if new up or down move is blocked by another queen"""

        for i in self.queen_col_map[col]:
            # Down move blocked
            if i > new_row and i < curr_row:
                return True
            # Up move blocked
            elif i < new_row and i > curr_row:
                return True
        return False

    def enumerate_legal_successor_states(self):
        """
        Finds all possible legal moves for each queen on the board
        """

        queens = self.state
        states = self.state_space

        for queen in queens[0:1]:
            print(queen)
            transitions = []
            for state in states:
                #Add transition if on same row
                if state[0] == queen[0]:
                    if not self.row_move_blocked(queen[0],queen[1],state[1]):
                        transitions.append(state)
                #Add transition if in same column
                elif state[1] == queen[1]:
                    if not self.col_move_blocked(queen[1],queen[0],state[0]):
                        transitions.append(state)
                #Add transition if diagonal
                # elif self.queens_diagonal(queen,state):
                #     transitions.append(state)
            

            

                
                
                        



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

    def __init__(self,n):
        self.n = n
        self.state = []
        self.state_space = self.enumerate_state_space()
        self.queen_state_space = None

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
        states = []
        n = self.n
        #generate n * n of queens from (0,0) to (n,n)
        for i in range(n):
            for j in range(n):
                states.append((i,j))
        return states

    def enumerate_queen_state_space(self):
        self.queen_state_space = [Queen(i) for i in self.state]
        
    def state_in_conflict(self):
        """Check if self state in conflict, returns True when any queen 
        can attack any other, otherwise returns False(goal reached)"""

        # Check rows/columns in conflict
        def diagonal_difference(a,b):
            row_diff = abs(a[0] - b[0])
            col_diff = abs(a[1] - b[1])

            if row_diff == col_diff:
                return True
            else:
                return False

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
                    if diagonal_difference(self.state[i],self.state[j]):
                        return True
        return False

    def enumerate_legal_successor_states(self):
        current_state = self.state
        for queen in current_state:
            # Remove all actions where there is currently a queen
            for i in self.state_space:
                pass
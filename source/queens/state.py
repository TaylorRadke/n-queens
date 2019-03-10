from random import randrange

class State(object):
    """STATE is a class used to hold states of the n-queens positions
    stored as tuple derived queen piece (row,column,moved) on n * n board"""

    def __init__(self,n,initial_state=None):
        self.n = n
        self.state = initial_state

        if self.state == None:
            self.state = []
            self.create_random_initial_state()

        self.state_space = [(i,j) for i in range(self.n) \
            for j in range(self.n) if (i,j) not in self.state]

    def print_state(self):
        for i in range(self.n):
            for j in range(self.n):
                if (i,j) in self.state:
                    print("Q",end=" ")
                else:
                    print("-",end=" ")
                if j == self.n-1:
                    print("\n")

    def get_state(self):
        return self.state

    def create_random_initial_state(self):
        if len(self.state) == self.n:
            return
        row = randrange(0,self.n)
        column = randrange(0,self.n)

        if (row,column) not in self.state:
            self.state.append((row,column))
        self.create_random_initial_state()

    def state_in_conflict(self):
        """Check if self state in conflict, returns True when any queen 
        can attack any other, otherwise returns False(goal reached)"""
        for i in range(0,self.n-1):
            for j in range(i+1,self.n):
                if self.not_legal_transition(self.state[i],self.state[j]):
                    return True   
        return False

    def not_legal_transition(self,a,b):
        row_diff = a[0] - b[0]
        col_diff = a[1] - b[1]
        return row_diff == 0 or col_diff == 0 or abs(row_diff) == abs(col_diff)

    def enumerate_actions(self):
        """
        Finds all possible legal moves for each queen on the board
        """
        for queen in self.state:
            for state in self.state_space.copy():
                #Replace state with new state
                if self.not_legal_transition(queen,state):
                    new_state = self.state.copy()
                    new_state.pop(new_state.index(queen))
                    new_state.append((state[0],state[1]))
                    yield new_state
        
            

            

                
                
                        



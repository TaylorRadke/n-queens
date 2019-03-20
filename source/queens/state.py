from random import randrange

class State(object):
    """STATE is a class used to hold states of the n-queens positions
    stored as tuple derived queen piece (row,column,moved) on n * n board"""

    def __init__(self,n,initial_state=None):
        self.n = n
        self.state = initial_state

        self.state = initial_state

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
        state = []
        for col in range(self.n):
            row = randrange(0,self.n)
            state.append((row,col))
        return state
    

    def transition_in_conflict(self,curr_state,new_state):
        row_diff = curr_state[0] - new_state[0]
        col_diff = curr_state[1] - new_state[1]
        return row_diff == 0 or col_diff == 0 or abs(row_diff) == abs(col_diff)

    def in_conflict(self):
        """Check if self state in conflict, returns True when any queen 
        can attack any other, otherwise returns False(goal reached)"""
        states_in_conflict = 0
        for i in range(self.n-1):
            for j in range(i+1,self.n):
                if self.transition_in_conflict(self.state[i],self.state[j]):
                    states_in_conflict += 1   
        return states_in_conflict

    def enumerate_actions(self): 
        """
        Finds all possible legal moves for each queen on the board
        """
        for queen in self.state:
            for i in range(self.n):
                if i != queen[0]:
                    state = self.state.copy()
                    state.pop(state.index(queen))
                    state.append((i,queen[1]))
                    yield state



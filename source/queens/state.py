from random import randrange
import sys

class State(object):
    """STATE is a class used to hold states of the n-queens positions
    stored as tuple derived queen piece (row,column,moved) on n * n board"""

    def __init__(self,n,initial_state=None):
        self.n = n
        self.state = initial_state

        if self.state == None:  self.create_random_initial_state()

        #All transitions on board except any that are occupied by other queens
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
        self.state = []

        while len(self.state) != self.n:
            rand_row = randrange(0,self.n)
            rand_col = randrange(0,self.n)
            if (rand_row,rand_col) not in self.state:  self.state.append((rand_row,rand_col))
        print(sys.getsizeof(self.state))
    

    def transition_in_conflict(self,curr_state,new_state):
        row_diff = curr_state[0] - new_state[0]
        col_diff = curr_state[1] - new_state[1]
        return row_diff == 0 or col_diff == 0 or abs(row_diff) == abs(col_diff)

    def state_in_conflict(self):
        """Check if self state in conflict, returns True when any queen 
        can attack any other, otherwise returns False(goal reached)"""
        for i in range(self.n-1):
            for j in range(i+1,self.n):
                if self.transition_in_conflict(self.state[i],self.state[j]):
                    return True   
        return False

    def move_blocked(self,curr_state,new_state):
        #Check same row
        if curr_state[0] == new_state[0]:
            for i in self.state:
                if i[0] == curr_state[0]:
                    if (i[1] > curr_state[1] and i[1] < new_state[1]) or (i[1] < curr_state[1] and i[1] > new_state[1]):
                        return True
        #Check same column     
        elif curr_state[1] == new_state[1]:
            for i in self.state:
                if i[1] == curr_state[1]:
                    if (i[0] > curr_state[0] and i[0] < new_state[1]) or (i[0] < curr_state[0] and i[0] > new_state[0]):
                        return True
        else:
            for i in self.state:
                curr_i_diag, curr_i_row, curr_i_col = self.diagonal(curr_state,i)
                curr_new_diag, curr_new_row, curr_new_col = self.diagonal(curr_state,new_state)

                if curr_i_diag and curr_new_diag:
                        print(curr_state, "->",new_state, i)
                        State(self.n,[curr_state,new_state,i]).print_state()
                        print('-'*90)
                return True
        return False


    def diagonal(self,a,b):
        row_diff = a[0] - b[0]
        col_diff = a[1] - b[1]
        return abs(row_diff)==abs(col_diff),row_diff,col_diff

    def enumerate_actions(self): 
        """
        Finds all possible legal moves for each queen on the board
        """
        for queen in self.state:
            for state in self.state_space:
                #Replace Queen's current pos
                # ition with it's new position
                if self.transition_in_conflict(queen,state):
                    if not self.move_blocked(queen,state):
                        new_state = self.state.copy()
                        new_state.pop(new_state.index(queen))
                        new_state.append(state)
                        yield new_state
                    
                        



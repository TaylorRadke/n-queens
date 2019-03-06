import queue
from random import randrange

#Tree contains data about the search tree
class QUEENSEARCHTREE(object):
    def __init__(self,initial_state):
        self.frontier = queue.Queue()
        self.frontier.put(initial_state)
        self.goal_reached = False
        self.explored = set({})
    
    def enqueue_frontier(self,state):
        self.frontier.put(state)

    def dequeue_frontier(self):
        return self.frontier.get()

    def add_explored(self,state):
        self.explored.add(state)

    def state_in_explored(self,state):
        return state in self.explored

    def is_goal_reached(self):
        return self.goal_reached


class LEAF(object):
    def __init__(self,parent,state):
        self.parent = parent
        self.state = state
        self.actions = {}

# Board is a class used to hold states of the n-queens positions
# stored as tuple (row,column) on n * n board
# As in:
#       0   1    2   3  ...  n
#   0  (0,0)                (0,n)
#   1       (1,1)
#   2           (2,2)
#   3               (3,3)
#   ...                 (...)
#   n  (n,0)                (n,n)
class BOARD_STATE(object):
    def __init__(self,n):
        self.n = n
        self.state = []

    def __eq__(self,other):
        return self.state == other.get_state()
    def get_state(self):
        return self.state
    
    def set_state(self,new_state):
        if len(new_state) == self.n:
            self.state = new_state
            return True
        return False

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

def main():
    n = 10
    state1 = BOARD_STATE(n)
    state2 = BOARD_STATE(n)
    
    state1.create_random_initial_state()
    state2.create_random_initial_state()

    print(state1.get_state())
    print(state2.get_state())
    
    print(state1.state_in_conflict())
    print(state2.state_in_conflict())

if __name__ == "__main__":
    main()

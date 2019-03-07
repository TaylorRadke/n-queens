from random import randrange
import queue

class BOARDSTATE(object):
# Board is a class used to hold states of the n-queens positions
# stored as tuple (row,column,moved) on n * n board
# As in:
#       0   1    2   3  ...  n
#   0  (0,0)                (0,n)
#   1       (1,1)
#   2           (2,2)
#   3               (3,3)
#   ...                 (...)
#   n  (n,0)                (n,n)

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

    def get_n(self):
        return self.n

    def create_random_initial_state(self):
        if len(self.state) == self.n:
            return

        row = randrange(0,self.n)
        column = randrange(0,self.n)

        if (row,column,False) not in self.state:
            self.state.append((row,column,False))

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
    
class LEAFNODE(object):
    def __init__(self,parent,state):
        self.parent = parent
        self.state = state
        self.actions = []

    def legal_state_actions(self):
        for queens in self.state.get_state():
            if queens[2] == False: #Queen hasn't moved yet
                row = queens[0]
                column = queens[1]

                while row != 0:
                    if (row-1,column) not in self.state.get_state():
                        self.actions.append({queens:(row-1,column,True)})
                        row -= 1
                    else:
                        break
                row = queens[0]
                while row != self.state.get_n():
                    if (row+1,column) not in self.state.get_state():
                        self.actions.append({queens:(row+1,column,True)})
                        row += 1
                    else:
                        break
        print(self.actions)

    def get_actions(self):
        return self.actions
    


#Tree contains data about the search tree
class SEARCHTREE(object):
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
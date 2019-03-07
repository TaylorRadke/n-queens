from random import randrange
import queue
import collections



class Queen(tuple):
    def __init__(self,i):
        super().__init__()
    
    def __eq__(self,other):
        return (self[0] == other[0] and self[1] == other[1])

class BOARDSTATE(object):
    """Board is a class used to hold states of the n-queens positions
    stored as tuple derived queen piece (row,column,moved) on n * n board"""

    def __init__(self,n):
        self.n = n
        self.state = []

    def print_state(self):
        for i in range(self.n):
            for j in range(self.n):
                if (i,j) in self.state:
                    print("Q",end=" ")
                else:
                    print("I",end=" ")
                if j == self.n-1:
                    print("\n")

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
    #    self.state_space = []

    # def enumerate_state_space(self):
    #     states = []
    #     n = self.state.get_n()
    #     #generate n * n of queens
    #     for i in range(n):
    #         for j in range(n):
    #             states.append((i,j))
        
    #     return states

    # def get_state_space(self):
    #     return self.state_space
    
    # def enumarate_legal_state_action(self):
    #     n = self.state.get_n()
    #     current_state = self.state.get_state()
    #     for queen in current_state:
    #         # Remove all actions where there is currently a queen
    #         for i in self.state_space:
    #             pass



    def enumerate_legal_state_actions(self):
        state = self.state.get_state()
        queen_state = [Queen(i) for i in state]
        n = self.state.get_n()
        
        for queens in self.state.get_state():
            if queens[2] == False: #Queen hasn't moved yet
                row = queens[0]
                column = queens[1]
                #Find legal moves to left
                while row != 0: 
                    if Queen((row-1,column)) not in queen_state:
                        self.actions.append({queens:(row-1,column,True)})
                        row -= 1
                    else:
                        break

                row = queens[0]
                #Find legal moves to right
                while row != n-1:
                    if (row+1,column) not in queen_state:
                        self.actions.append({queens:(row+1,column,True)})
                        row += 1
                    else:
                        break
                row = queens[0]
                #Find legal moves up
                while column != 0:
                    if (row,column-1) not in queen_state:
                        self.actions.append({queens:(row,column-1,True)})
                        column -= 1
                    else:
                        break

                #Find legal moves down
                column = queens[1]
                while column != n-1:
                    if (row,column+1) not in queen_state:
                        self.actions.append({queens:(row,column+1,True)})
                        column += 1
                    else:
                        break

                #Find legal diagonal moves up and left
                row = queens[0]
                columns = queens[1]
                while row != 0 and column != 0:
                    if (row-1,column-1) not in queen_state:
                        self.actions.append({queens:(row-1,column-1,True)})
                        row -= 1
                        column -= 1
                    else:
                        break

                row = queens[0]
                columns = queens[1]
                #Find legal diagonal moves up and right
                while row != 0 and column != n-1:
                    if (row-1,column+1) not in queen_state:
                        self.actions.append({queens:(row-1,column+1,True)})
                        row -= 1
                        column += 1
                    else:
                        break
                
                #Find legal diagonal moves down and left
                row = queens[0]
                column = queens[1]
                while row != n-1 and column != 0:
                    if (row+1,column-1) not in queen_state:
                        self.actions.append({queens:(row+1,column-1,True)})
                        row += 1
                        column -=1
                    else:
                        break

                #Find legal diagonal moves down and right
                row = queens[0]
                column = queens[1]
                while row != n-1 and column != n-1:
                    if  (row+1,column+1) not in queen_state:
                        self.actions.append({queens:(row+1,column+1,True)})
                        row += 1
                        column += 1
                    else:
                        break

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
import sys
from random import randrange,random
from math import e
from time import time
from queue import Queue

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

class BFS(object):
    def __init__(self,n,initial_state=None):
        self.n = n
        self.initial_state = State(self.n).create_random_initial_state()
        self.explored = set({})
        self.frontier = Queue()
        self.solutions = 0
        self.frontier.put(self.initial_state)

    #Add hash of state to explored
    def add_explored_state(self,action):
        self.explored.add(hash(frozenset(action)))

    #Check if hash of state in explored
    def state_explored(self,state):
        return hash(frozenset(state)) in self.explored
    
    def solution_found(self,solution):
        self.solutions += 1
        print('\n\n')
        State(self.n,solution).print_state()
        print("-"*90,'\n') 

    def get_actions(self,parent,ds_push):
       for action in list(State(self.n,parent).enumerate_actions()):
            #Check if state has already been explored
            if not self.state_explored(action):
                #Add state to explored
                self.add_explored_state(action)
                
                #Add state to frontier
                ds_push(action)
    
    def search(self):
        """Performs the breadth-first to find a solution to the initial state"""
        start = time()

        while not self.frontier.empty():
            print("n = {}, Solutions found: {}, States Checked: {}/{}, States Queued: {}"
            .format(self.n,self.solutions,len(self.explored),pow(self.n,self.n),self.frontier._qsize()),end='\r')
            state = self.frontier.get()

            if not State(self.n,state).in_conflict():
                self.solution_found(state)
            self.add_explored_state(state)

            self.get_actions(state,self.frontier.put)

        search_time = time() - start
        print("Search Time: {} seconds, States explored: {}, Solutions Found: {}"
            .format(search_time,len(self.explored),self.solutions))
        
class HillClimb(object):
    def __init__(self,n):
        self.n = n
        self.state = State(n).create_random_initial_state()
        self.cost = State(n,self.state).in_conflict()
        self.solution_found = False
        self.restarts = 0

    def restart(self):
        self.state = State(self.n).create_random_initial_state()
        self.cost = State(self.n,self.state).in_conflict()
        self.restarts+=1

    def search(self):
        start = time()

        while not self.solution_found:
            print("Restarts: {}".format(self.restarts),end='\r')
            old_cost = self.cost
            if bool(State(self.n,self.state).in_conflict()):
                for action in list(State(self.n,self.state).enumerate_actions()):
                    cost = State(self.n,action).in_conflict()
                    if cost < self.cost:
                        self.cost = cost
                        self.state = action
                if old_cost == self.cost:
                    self.restart()
            else:
                self.solution_found = True
                State(self.n,self.state).print_state()
        print("Time taken: {}".format(time()-start))

class SimulatedAnnealing(object):
    def __init__(self,n):
        self.n = n
        self.state = State(self.n).create_random_initial_state()
        self.k = 1000
        self.temp = self.k
        self.cost = None
        self.solution_found = False

    
    def random_select_neighbour(self):
        states = [action for action in list(State(self.n,self.state).enumerate_actions())]
        return states[randrange(0,len(states))]

    def temp_func(self,n):
        return pow(0.99,n)

    def search(self):
        n = 0
        while not self.solution_found:
            print("Temp: {}".format(self.temp),end='\r')
            for _ in range(self.k):
                self.cost = State(self.n,self.state).in_conflict()
                if bool(self.cost):
                    random_neighbour = self.random_select_neighbour()
                    random_neighbour_cost = State(self.n,random_neighbour).in_conflict()

                    if random_neighbour_cost <= self.cost:
                        self.state = random_neighbour
                        self.cost = random_neighbour_cost
                    else:
                        p = pow(e,-(self.cost - random_neighbour_cost)/self.temp) 
                        if p > random():
                            self.state = random_neighbour
                            self.cost = random_neighbour_cost
                else:
                    self.solution_found = True
                    State(self.n,self.state).print_state()
                    break
            self.temp -= self.temp_func(n)
            n+=1
def main():
    n = int(sys.argv[1])
    SimulatedAnnealing(n).search()
        
if __name__ == "__main__":
    main() 
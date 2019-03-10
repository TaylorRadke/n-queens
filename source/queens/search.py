from queue import Queue
from queens.state import State
from time import time
from math import factorial

class Search(object):
    def __init__(self,n,initial_state=None):
        self.n = n
        self.initial_state = State(self.n,initial_state)
        self.explored = set({})
        self.frontier = None
        self.solutions = 0

    #Add hash of state to explored
    def add_explored_state(self,action):
        self.explored.add(hash(frozenset(action)))

    #Check if hash of state in explored
    def state_explored(self,state):
        return hash(frozenset(state)) in self.explored
    
    #Get number of combinations possible for an n * n board
    # nCr(n) = (n^2)! / n!(n^2 - n)!
    def n_combinations(self):
        n = self.n*self.n
        r = self.n
        return factorial(n) / factorial(r) / factorial(n-r)

    def solution_found(self,solution):
        self.solutions += 1
        print('\n\n')
        State(self.n,solution).print_state()
        print("-"*100,'\n') 

    def get_actions(self,parent,ds_push):
        self.add_explored_state(parent)

        #Check if parent is a goal state
        if not State(self.n,parent).state_in_conflict():    self.solution_found(parent)

        for action in list(State(self.n,parent).enumerate_actions()):
            #Check if state has already been explored
            if not self.state_explored(action):
                #Add state to explored
                self.add_explored_state(action)
                
                #Add state to frontier
                ds_push(action)

class BFS(Search):
    """Breadth first search is a tree search which implements a queue to find a solution"""

    def __init__(self,n,initial_state=None):
        super().__init__(n,initial_state)
        self.frontier = Queue()

        #Push inital state to the queue
        self.frontier.put(self.initial_state.get_state())

    def search(self):
        """Performs the breadth-first to find a solution to the initial state"""
        start = time()
        combinations = int(self.n_combinations())

        while not self.frontier.empty():
            print("n = {},   Solutions found: {}, States Checked: {}/{}, States Queued: {}"
            .format(self.n,self.solutions,len(self.explored),combinations,self.frontier._qsize()),end='\r')

            self.get_actions(self.frontier.get(),self.frontier.put)

        search_time = time() - start
        print("Search Time: {} seconds, States explored: {}, Solutions Found: {}"
            .format(search_time,len(self.explored),self.solutions))
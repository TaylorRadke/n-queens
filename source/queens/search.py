from queue import Queue
from queens.state import State
from time import time
import datetime
import sys

class Search(object):
    a = None
    def __init__(self,n,initial_state=None,logger=None):
        self.n = n
        self.logger = logger
        self.initial_state = State(self.n,initial_state)

        self.goal_reached = False
        self.explored = set({})
        self.frontier = None
        self.solution = None

    def add_explored_state(self,state):
        self.explored.add(hash(frozenset(state)))

    #Check if hash of state in explored
    def state_explored(self,state):
        if hash(frozenset(state)) not in self.explored:
            return False
        return True

    def map_new_state(self,parent,ds_push):
        for action in list(State(self.n,parent).enumerate_actions()):
            #Check if action is a goal state
            if not State(self.n,action).state_in_conflict():
                self.goal_reached = True
                self.solution = action

            elif not self.state_explored(action):
            #Add new state to data structure (queue,stack...etc)
                ds_push(action)

        
                        

class BFS(Search):
    """Breadth first search is a tree search which implements a queue to find a solution"""

    def __init__(self,n,initial_state=None,logger=None):
        super().__init__(n,initial_state,logger)
        self.frontier = Queue()
        self.frontier.put(self.initial_state.get_state())
    
    
    def search(self):
        """Performs the breadth-first to find a solution to the initial state"""
        print("n = ", self.n)
        print("Initial State:   ")
        self.initial_state.print_state()
        start = time()
        print("Search Started:  ",datetime.datetime.now())
        while not self.goal_reached and not self.frontier.empty():
            state = self.frontier.get()
            self.add_explored_state(state)
            self.map_new_state(state,self.frontier.put)

        search_time = time()-start
        if self.frontier.empty():
            print("No solution")
        else:
            print("Solution found:")
            State(self.n,self.solution).print_state()
        print()
        print("Search Finished: ", datetime.datetime.now())
        print("Time taken: {} seconds".format(search_time))
        print()
        print("="*50)
        print()

        if not self.solution:
            self.solution = "None"

        if self.logger:
            self.logger.writerow([self.n,search_time,len(self.explored),\
                self.initial_state.get_state(),self.solution])
        del self
from queue import Queue
from queens.state import State
from time import time
import datetime
import sys

class Search(object):
    def __init__(self,n,initial_state=None,logger=None):
        self.n = n
        self.logger = logger
        self.initial_state = State(self.n,initial_state)

        self.goal_reached = False
        self.explored = set({})
        self.frontier = None
        self.solutions = 0

    def add_explored_state(self,action):
        self.explored.add(hash(frozenset(action)))

    #Check if hash of state in explored
    def state_explored(self,state):
        if hash(frozenset(state)) not in self.explored:
            return False
        return True

    def map_new_state(self,parent,ds_push):
        for action in list(State(self.n,parent).enumerate_actions()):
            #Check if action is a goal state
            if not self.state_explored(action):
                if not State(self.n,action).state_in_conflict():
                    self.solutions +=1
                    self.add_explored_state(action)
                    print()
                    State(self.n,action).print_state()
                    print("="*50)
                else:
                    #Add new unexplored and non-goal state to data structure (queue,stack...etc)
                    ds_push(action)

class BFS(Search):
    """Breadth first search is a tree search which implements a queue to find a solution"""

    def __init__(self,n,initial_state=None,logger=None):
        super().__init__(n,initial_state,logger)
        self.frontier = Queue()
        self.frontier.put(self.initial_state.get_state())
    
    def search(self):
        """Performs the breadth-first to find a solution to the initial state"""
        start = time()
        while not self.frontier.empty():
            print("n = {},   Solutions found: {},    States Checked: {}".format(self.n,self.solutions,len(self.explored)),end='\r')
            state = self.frontier.get()
            self.add_explored_state(state)
            self.map_new_state(state,self.frontier.put)

        if self.logger:
            self.logger.writerow([self.n,time()-start,len(self.explored),\
                self.solutions,self.initial_state.get_state()])
        del self
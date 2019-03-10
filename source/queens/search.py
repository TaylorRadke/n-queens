from queue import Queue
from queens.state import State
from time import time
import datetime

class Search(object):
    def __init__(self,n,initial_state=None,logging=None):
        self.n = n
        self.logging = logging
        self.initial_state = State(self.n,initial_state)

        self.goal_reached = False
        self.explored = set({})
        self.frontier = None
        self.solution = None

    def print_solution(self):
        print(self.solution.print_state())

    def add_explored_state(self,state):
        self.explored.add(hash(frozenset(state)))

    #Check if hash of state in explored
    def state_explored(self,state):
        if hash(frozenset(state)) not in self.explored:
            return False
        return True

    def found_solution(self,solution_state):
        self.solution = solution_state
        self.goal_reached = True

    def map_new_state(self,parent,ds_push):
        for action in list(State(self.n,parent).enumerate_actions()):
            if not State(self.n,action).state_in_conflict():
                self.found_solution(action)
            #Check if state not explored
            elif not self.state_explored(action):
            #Add new state to data structure (queue,stack...etc)
                ds_push(action)

        
                        

class BFS(Search):
    """Breadth first search is a tree search which implements a queue to find a solution"""

    def __init__(self,n,initial_state=None,logging=None):
        super().__init__(n,initial_state,logging)
        self.frontier = Queue()
        self.frontier.put(self.initial_state.get_state())

    def search(self):
        """Performs the breadth-first to find a solution to the initial state"""
        print("n = ", self.n)
        self.initial_state.print_state()
        start = time()
        print("Search Started:  ",datetime.datetime.now())
        while not self.goal_reached and not self.frontier.empty():
            state = self.frontier.get()
            self.add_explored_state(state)

            self.map_new_state(state,self.frontier.put)
            print("States Explored: {}".format(len(self.explored)),end='\r',flush=True)

        search_time = time()-start
        print()
        print("Time taken: {} seconds".format(search_time))
        print("Search Finished: ", datetime.datetime.now())
        if self.frontier.empty():
            print("No solution")
        else:
            print("Solution found:")
            State(self.n,self.solution).print_state()

        print()
        print("="*50)
        print()

        if not self.solution:
            self.solution = "None"

        if self.logging:
            self.logging.writerow([self.n,search_time,len(self.explored),\
                self.initial_state.get_state(),self.solution])
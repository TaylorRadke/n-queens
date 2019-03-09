from queue import Queue
from queens.state import State
from time import time
import datetime

class Search(object):
    def __init__(self,n,initial_state=None):
        self.n = n
        self.initial_state = State(self.n,initial_state)
        print("n = ", self.n)
        self.initial_state.print_state()

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

    def map_new_state(self,parent):
        for state in parent:
            for transition in State(self.n,parent).enumerate_actions():
                #If queen has a legal move
                if state in transition:
                    new_state = parent.copy()
                    #Pop current position
                    new_state.pop(new_state.index(state))
                    #Push new position
                    new_state.append(transition[state])
                    #Check if state is a solution
                    if not State(self.n,new_state).state_in_conflict():
                        self.found_solution(new_state)
                    #Check if state not in frontier or explored
                    if not self.state_explored(new_state):
                        #Add new state to frontier queue
                        yield new_state

        
                        

class BFS(Search):
    """Breadth first search is a tree search which implements a queue to find a solution"""

    def __init__(self,n,initial_state=None):
        super().__init__(n,initial_state)
        self.frontier = Queue()
        self.enqueue_frontier(self.initial_state.get_state())

    def search(self):
        """Performs the breadth-first to find a solution to the initial state"""
        start = time()
        print("Search Started:  ",datetime.datetime.now())


        while not self.goal_reached and not self.frontier.empty():
            state = self.frontier.get()
            self.add_explored_state(state)
            for action in list(self.map_new_state(state)):
                self.frontier.put(action)
            print("States Explored: {}".format(len(self.explored)),end='\r',flush=True)
        print()
        print("Time taken: {} seconds".format(time()-start))
        print("Time Finished: ", datetime.datetime.now())
        if (self.frontier.empty()):
            print("No solution")
        else:
            print("Solution found:")
            State(self.n,self.solution).print_state()


    def enqueue_frontier(self,node):
        self.frontier.put(node)
from queue import Queue
from queens.state import State
from time import time

class Search(object):
    def __init__(self,n,initial_state=None):
        self.n = n
        self.initial_state = State(self.n,initial_state)

        self.initial_state.print_state()
        print('\n')

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

class Leaf(object):
   
    def __init__(self,tree,parent):
        self.tree = tree
        self.parent = parent
        self.state = self.parent.get_state()
        self.n = self.parent.get_n()

    def map_new_state(self):
        enumerated_states = self.parent.enumerate_actions()
        for state in self.state:
            for transition in enumerated_states:
                #If queen has a legal move
                if state in transition:
                    new_state = self.state.copy()
                    #Pop current position
                    new_state.pop(new_state.index(state))
                    #Push new position
                    new_state.append(transition[state])

                    #Check if state is a solution
                    if not State(self.n,new_state).state_in_conflict():
                        self.tree.found_solution(new_state)
                    #Check if state not in frontier or explored
                    if not self.tree.state_explored(new_state):
                        #Add new state to frontier queue
                        self.tree.enqueue_frontier(new_state)
                        #Add state to explored
                        self.tree.add_explored_state(new_state)
                        

class BFS(Search,Leaf):
    """Breadth first search is a tree search which implements a queue to find a solution"""

    def __init__(self,n,initial_state=None):
        super().__init__(n,initial_state)
        self.frontier = Queue()
        self.enqueue_frontier(self.initial_state.get_state())

    def search(self):
        """Performs the breadth-first to find a solution to the initial state"""
        start = time()
        while not self.goal_reached and not self.frontier.empty():
            state = self.frontier.get()
            self.add_explored_state(state)
            Leaf(self,State(self.n,state)).map_new_state()
            print("Frontier: {}\tExplored: {}\tTime: {}"
                .format(self.frontier.qsize(),len(self.explored),time()-start),end="\r")

        print("\n")
        print("Time taken: {}\n".format(time()-start))
        if (self.frontier.empty()):
            print("No solution")
        else:
            print("Solution found")
            State(self.n,self.solution).print_state()


    def enqueue_frontier(self,node):
        self.frontier.put(node)

class DFS(Search):
    def __init__(self,n,initial_state=None):
        super().__init__(self,initial_state)

from queue import Queue
from queens.state import State

class SEARCH(object):
    def __init__(self,n,initial_state=None):
        self.n = n
        self.initial_state = self.initialise_state()

        self.initial_state.get_parent().print_state()
        print('\n')

        self.goal_reached = False
        self.explored = set({})
        self.frontier = None
        self.solution = None

    def initialise_state(self):
        return Leaf(self,State(self.n))

    def add_explored_state(self,state):
        self.explored.add(hash(frozenset(state)))

    def state_exists(self,state):
        #Check if hash of state in explored
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

    def is_goal(self):
        return not self.parent.state_in_conflict()
    
    def get_parent(self):
        return self.parent

    def get_state(self):
        return self.state

    def map_new_state(self):
        self.enumerated_states = self.parent.enumerate_legal_successor_states()
        for state in self.state:
            for transition in self.enumerated_states:
                if state in transition:
                    new_state = self.state.copy()
                    #Pop current position
                    new_state.pop(new_state.index(state))
                    #Push new position
                    new_state.append(transition[state])

                    #Check if state not in frontier or explored
                    if not self.tree.state_exists(new_state):
                        #Add new node to frontier
                        c_state = State(self.n,new_state)

                        #Check if state is a solution
                        if not c_state.state_in_conflict():
                            self.tree.found_solution(c_state)
                        self.tree.enqueue_frontier(Leaf(self.tree,c_state))

class BFS(SEARCH):
    """Breadth first search is a tree search which implements a queue to find a solution"""

    def __init__(self,n):
        super().__init__(n)
        self.frontier = Queue()
        self.enqueue_frontier(self.initial_state)

    def search(self):
        """Performs the breadth-first to find a solution to the initial state"""
        while not self.goal_reached and not self.frontier.empty():
            leaf = self.frontier.get()
            self.add_explored_state(leaf.get_state())
            leaf.map_new_state()

        if (self.frontier.empty()):
            print("No solution")
        else:
            print(self.solution.print_state())

    def enqueue_frontier(self,node):
        self.frontier.put(node)

    
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

    def initialise_state(self):
        return Leaf(self,State(self.n))

    def add_explored_state(self,state):
        self.explored.add(hash(frozenset(state)))

    def state_exists(self,state):
        #Check if hash of state in explored
        if hash(frozenset(state)) not in self.explored:
            return False
        return True

    def is_goal_reached(self):
        return self.goal_reached

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
                        self.tree.enqueue_frontier(Leaf(self.tree,State(self.n,new_state)))

class BFS(SEARCH):
    """Breadth first search is a tree search which implements a queue to find a solution"""

    def __init__(self,n):
        super().__init__(n)

        self.frontier = Queue()
        self.enqueue_frontier(self.initial_state)

    def search(self):
        if not self.frontier.empty():
            leaf = self.frontier.get()
            self.add_explored_state(leaf.get_state())
            if not leaf.is_goal():
                leaf.map_new_state()
                self.search()
            else:
                print("found solution")
        else:
            return False

    def enqueue_frontier(self,node):
        self.frontier.put(node)

    
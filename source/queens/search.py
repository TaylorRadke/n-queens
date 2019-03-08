from queue import Queue
from queens.state import State

class SEARCH(object):
    def __init__(self,n):
        self.n = n
        self.goal_reached = False
        self.explored = set({})

    def add_explored(self,state):
        self.explored.add(state)

    def state_in_explored(self,state):
        return state in self.explored

    def is_goal_reached(self):
        return self.goal_reached

class LeafNode(object):
    def __init__(self,tree,parent,initial_state):
        self.parent = parent
        self.tree = tree
        self.initial_state = initial_state
        self.state = self.initial_state.get_state()
        self.n = self.initial_state.get_n()

    def node_is_goal(self):
        return not self.initial_state.state_in_conflict()
    
    def get_node_state(self):
        return self.initial_state

    def map_new_state(self):
        self.enumerated_states = self.initial_state.enumerate_legal_successor_states()
        for state in self.state:
            for transition in self.enumerated_states:
                if state in transition:
                    new_state = self.state.copy()
                    #Pop current position
                    new_state.pop(new_state.index(state))
                    #Push new position
                    new_state.append(transition[state])

                    new_state = State(self.n,new_state)
                    new_leaf = LeafNode(self.tree,self,new_state)
                    self.tree.enqueue_frontier(new_leaf)

class BFS(SEARCH):
    """Frontier contains node leafs"""
    def __init__(self,n):
        super().__init__(n)
        self.n
        self.frontier = Queue()

        self.initial_state = None
        self.initialise_state()
        self.enqueue_frontier(self.initial_state)

    def initialise_state(self):
        state = State(self.n)
        self.initial_state = LeafNode(self,None,state)
        self.initial_state.get_node_state().print_state()
        print('\n')

    def search(self):
        if not self.frontier.empty():
            node = self.frontier.get()
            if not node.node_is_goal():
                node.map_new_state()
                self.search()
            else:
                node.get_node_state().print_state()
        else:
            return False


    def enqueue_frontier(self,state):
        self.frontier.put(state)

    def dequeue_frontier(self):
        return self.frontier.get()

    
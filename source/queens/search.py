from queue import Queue

class SEARCH(object):
    def __init__(self,n,state):
        self.n = n
        self.goal_reached = False
        self.explored = set({})
        self.frontier = Queue()
        
        self.enqueue_frontier(state)

    def enqueue_frontier(self,state):
        self.frontier.put(state)

    def dequeue_frontier(self):
        return self.frontier.get()

    def add_explored(self,state):
        self.explored.add(state)

    def state_in_explored(self,state):
        return state in self.explored

    def is_goal_reached(self):
        return self.goal_reached

class LEAFNODE(object):
    def __init__(self,tree,parent,initial_state):
        self.parent = parent
        self.tree = tree
        self.initial_state = initial_state
        self.state = self.initial_state.get_state()
        self.n = self.initial_state.get_n()

        self.map_new_state()

    def map_new_state(self):
        self.enumerated_states = self.initial_state.enumerate_legal_successor_states()
        for state in self.state[:1]:
            for transition in self.enumerated_states[:1]:
                new_state = self.state.copy()

                #Pop current position
                new_state.pop(new_state.index(state))
                #Push new position
                new_state.append(transition[state])
        
        

#Tree contains data about the search tree
class TREESEARCH(SEARCH):
    def __init__(self,n):
        super().__init__()
    
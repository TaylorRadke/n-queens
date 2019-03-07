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
    def __init__(self,parent,state):
        self.parent = parent
        self.state = state
        self.actions = []

    def get_actions(self):
        return self.actions
    


#Tree contains data about the search tree
class TREESEARCH(SEARCH):
    def __init__(self,n):
        super().__init__()
    
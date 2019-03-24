import sys
from random import randrange,random
from math import e
from time import time

class Queue(list):
    def __init__(self):
        super().__init__(self)

    def get(self):
        value = self[0]
        del self[0]
        return value
    
    def put(self,item):
        self.append(item)

    def empty(self):
        return len(self) == 0
    
    def _qsize(self):
        return len(self)
    
    def __contains__(self,other):
        for i in self:
            if i == other:
                return True
        return False

#Print the board state representation by printing Q when the index and value of the 
# list are the same as in the nested loop, otherwise prints - or newline if inner loop reach n
def print_state(state, n = None):
    if n == None:
        n = len(state)

    print('\n')
    if len(state) == 0:
        for i in range(n):
            for j in range(n):
                print("-",end=" ")
                if j == n-1:    print('\n')
    else:
        for i in range(n):
            for j in range(n):
                if state[j] == i: print("Q", end=" ")
                else: print("-",end=" ")
                if j == n-1:
                    print('\n')
    print('\n')

#Create a random state by generating a random number for each index of the list indicating the row the queen is in
def create_random_state(n):
    #Create list of queens where the index is the column and the value is the row
    return [randrange(0,n) for _ in range(n)]

#yields true if two queens are on the same row or are diagonal to each other
def conflict(state):
    n = len(state)
    for i in range(n-1):
        for j in range(i+1,n):
            #Check queens on same row or diagonal to each other
            yield state[i] == state[j] or abs(j - i) == abs(state[j] - state[i])

#Checks if given state is a goal. Immediately returns False if any of the yields from conflict are True otherwise returns True
def is_goal_state(state, n):
    #Check if the given state is a goal state, returns False if the len of the state is less than the given n
    #or if any conflict check yields True
    if len(state) < n:  return False

    for i in conflict(state):
        if i:
            return False
    return True

#increments cost counter when the yield from conflict is True then returns counter
def state_cost(state):
    n = len(state)
    cost = 0
    for i in conflict(state):
        if i:
            cost += 1
    return cost

#Yields each legal state by checking each column and yielding new state where the current column is replaced with the
#iterator value if it is not the current position and none of the queens to the left are in the same row
def enumerate_actions(state,n):
    for i in range(n):
        new_state = list(state[:])
        new_state.append(i)
        yield new_state
        
            
def prune_enumerate_action(state,n):
    for i in range(n):
        if i not in state:
            new_state = list(state[:])
            new_state.append(i)
            yield tuple(new_state)

#Breadth-First-Search using a Queue where each action yielded from enumerate_actions is added to the queue
#Popping states from the queue and checking if they are goal state and they are not explored
def BFS(n):
    solutions = []
    initial_state = ()
    print_state(initial_state,n)

    explored = set({})
    explored.add(initial_state)
    frontier = Queue()
    frontier.put(initial_state)

    start = time()

    while not frontier.empty():
        print("n: {}, Solutions: {}, Queue: {}".format(n,len(solutions),frontier._qsize()),end='\r')

        state = frontier.get()
    
        for action in tuple(enumerate_actions(state,n)):
            if action not in explored:
                explored.add(action)
                if is_goal_state(action,n):
                    if action not in solutions:
                        solutions.append(action)
                        print_state(action)
                else:
                    frontier.put(action)

    print("\nSearch time: {}".format(time()-start))

def HillClimbing(n):
    state = ()
    print_state(state,n)
    cost = n
    solution_found = False
    restarts = 0

    start = time()
    while not solution_found:
        #print("Restarts: {}".format(restarts),end='\r')

        old_cost = cost

        if not is_goal_state(state,n):
            for action in tuple(enumerate_actions(state,n)):
                new_cost = state_cost(action)
                if new_cost < cost:
                    cost = new_cost
                    state = action
            if old_cost == cost and len(state) == n:
                #Random restart, set first queen to random row in first column
                state = (randrange(n),)
                cost
                restarts+=1
        else:
            solution_found = True

    print("\nSearch Time: {}".format(time()-start))

def SimulatedAnnealing(n):
    state = create_random_state(n)
    print_state(state)
    k = 15000

    #Get temperature with alpha^n where alpha is small change in T
    temp_alpha = 0.99
    temp_change = lambda n: pow(temp_alpha,n)

    solution_found = False
    iteration = 0
    temp = temp_change(iteration)

    start = time()
    
    while not solution_found:
        for _ in range(k):
            cost = state_cost(state)
            #Check if state is goal state
            if cost:
                #Generate random state by moving random queen to random row
                random_neighbour = state[:]
                random_neighbour[randrange(n)] = randrange(n)
                
                random_neighbour_cost = state_cost(random_neighbour)
                
                if random_neighbour_cost <= cost:
                    state = random_neighbour
                    cost = random_neighbour_cost
                else:
                    state_change_probability = pow(e,-(random_neighbour_cost - cost)/temp)
                    if state_change_probability >= random():
                        state = random_neighbour
                        cost = random_neighbour_cost
            else:
                solution_found = True
                break

        iteration+=1
        temp = temp_change(iteration)
        print(temp,end='\r')

    print("Search Time: {}, Solution:\n".format(time()-start))
    print_state(state)


if __name__ == "__main__":
    n = int(sys.argv[1])
    BFS(n)
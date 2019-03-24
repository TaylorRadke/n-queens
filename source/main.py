import sys
from random import randrange,random
from math import e
from time import time
from queue import Queue

def print_state(state):
    n = len(state)
    print('\n')
    for i in range(n):
        for j in range(n):
            if state[j] == i: print("Q", end=" ")
            else: print("-",end=" ")
            if j == n-1:
                print('\n')
    print('\n')

def create_random_state(n):
    #Create list of queens where the index is the column and the value is the row
    return [randrange(0,n) for _ in range(n)]

def conflict(state):
    n = len(state)
    for i in range(n-1):
        for j in range(i+1,n):
            #Check queens on same row or diagonal to each other
            yield state[i] == state[j] or abs(j - i) == abs(state[j] - state[i])

def is_goal_state(state):
    #Check if self state in conflict, returns True when any queen 
    #can attack any other, otherwise returns False(goal reached)
    for i in conflict(state):
        if i:
            return False
    return True

def state_cost(state):
    n = len(state)
    cost = 0
    for i in conflict(state):
        if i:
            cost += 1
    return cost


def enumerate_actions(parent):
    #Yields each possible state for each queen, where a queen can go up or down in its
    #column but does not move diagonally or horizontally 
    n = len(parent)
    for i in range(n):
        for j in range(n):
            if parent[i] != j:
                state = parent[:]
                state[i] = j
                yield state

def BFS(n):
    initial_state = [0 for _ in range(n)]
    print_state(initial_state)

    explored = set({})
    frontier = Queue()
    
    solutions = []
    frontier.put(initial_state)
    start = time()

    while not frontier.empty():
        print("n: {}, Solutions: {}, Queue: {}"
        .format(n,len(solutions),frontier._qsize()),end='\r')

        state = frontier.get()

        for action in list(enumerate_actions(state)):
            hash_action = hash(str(action))
            if hash_action not in explored:
                explored.add(hash_action)
                if is_goal_state(action):
                    if action not in solutions:
                        solutions.append(action)
                        print_state(action)
                else:
                    frontier.put(action)
            

    print("\nSearch time: {}".format(time()-start))

def HillClimbing(n):
    state = create_random_state(n)
    print_state(state)
    cost = state_cost(state)
    solution_found = False
    restarts = 0

    start = time()
    while not solution_found:
        print("Restarts: {}".format(restarts),end='\r')
        old_cost = cost
        if is_goal_state(state):
            for action in list(enumerate_actions(state)):
                new_cost = state_cost(action)
                if new_cost < cost:
                    cost = new_cost
                    state = action
            if old_cost == cost:
                state = create_random_state(n)
                cost = state_cost(state)
                restarts+=1
        else:
            solution_found = True
    #Print Solution
    print_state(state)
    print("Search Time: {}".format(time()-start))

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
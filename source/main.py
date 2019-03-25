import sys
from random import randrange,random
from math import e
from time import time
from queue import Queue
import csv

#Print the board state representation by printing Q when the index and value of the 
# list are the same as in the nested loop, otherwise prints - or newline if inner loop reach n
def print_state(state, n = None):
    if n == None:
        n = len(state)

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

#Breadth-First-Search using a Queue where each action yielded from enumerate_actions is added to the queue
#Popping states from the queue and checking if they are goal state and they are not explored
def BFS(n,csv_w = None):

    #Yields all children states of the current states if there are no conflict
    def pruned_actions(state):
        if (len(state) == n):   return
        for i in range(n):
            new_state = list(state[:])
            new_state.append(i)
            
            if is_goal_state(new_state,len(new_state)):
                yield tuple(new_state)

    #yields all new states by appending i from 0 to n to end of state
    def enumerate_actions(state):
        if (len(state) == n):   return
        for i in range(n):
            new_state = list(state[:])
            new_state.append(i)
            yield tuple(new_state)

    solutions = []
    initial_state = ()
    #print_state(initial_state,n)

    explored = set({})
    explored.add(initial_state)
    frontier = Queue()
    frontier.put(initial_state)

    start = time()

    while not frontier.empty():
        state = frontier.get()
    
    #uncomment whichever state enumeration to use
        for action in tuple(pruned_actions(state)):
    #   for action in tuple(enumerate_action(state)):
            if action not in explored:
                explored.add(action) 
                if is_goal_state(action,n):
                    if action not in solutions:
                        solutions.append(action)
                else:
                    frontier.put(action)

    print("n: {}, Search time: {}, Solutions found: {}".format(n,(time()-start),len(solutions)))
    if csv_w:   csv_w.writerow([n,len(solutions),time()-start])
    # for solution in solutions:
    #     print_state(solution)



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

#increments cost counter when the yield from conflict is True then returns counter
def state_cost(state):
    n = len(state)
    cost = 0
    for i in conflict(state):
        if i:
            cost += 1
    return cost

#HillClimbing algorithm to find a single goal state
def HC(n,csv_w):
    state = [0 for _ in range(n)]
    print_state(state)
    cost = state_cost(state)
    solution_found = False
    restarts = 0

    start = time()

    while not solution_found:
        print("Restarts: {}".format(restarts),end='\r')
        old_cost = cost
        if cost:
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

def SA(n):
    state = [0 for _ in range(n)]
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
                    #Sets the probability that the state will go uphill (further from solution)
                    state_change_probability = pow(e,(cost - random_neighbour_cost)/temp)
                    if state_change_probability >= random():
                        state = random_neighbour
            else:
                solution_found = True
                break

        iteration+=1
        temp = temp_change(iteration)
        print(temp,end='\r')

    print("Search Time: {}, Solution:\n".format(time()-start))
    print_state(state)

if __name__ == "__main__":
    #Either set n as an argument on commandline or set it direcly below and uncomment whichever function to search with

    #n = int(sys.argv[1])
    #n = some integer

    #Breadth first search
    #BFS(n)
    BFS(int(sys.argv[1]))
    # with open("hc_output.txt",'a',newline='') as file:
    #     writer = csv.writer(file)
    #     for n in range(20):
    #         for _ in range(10):
    #             HC(n,writer)

    #HillClimbing Search

    #Simulated Annealing Search
    #SA(15)
import sys
from random import randrange,random
from math import e
from time import time
from queue import Queue

def print_state(state):
    n = len(state)
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

def state_in_conflict(state):
    """Check if self state in conflict, returns True when any queen 
    can attack any other, otherwise returns False(goal reached)"""
    attacking = 0
    n = len(state)
    for i in range(n-1):
        for j in range(i+1,n):
            #if value is the same indicates queen on the same row
            if state[i] == state[j]:
                attacking += 1
            else:
                if abs(j - i) == abs(state[j] - state[i]):
                    attacking+=1   
    return attacking

def enumerate_actions(parent): 
    """
    Finds all possible legal moves for each queen on the board
    """
    n = len(parent)
    for i in range(n):
        for j in range(n):
            if parent[i] != j:
                state = parent[:]
                state[i] = j
                yield state

def BFS(n):
    initial_state = create_random_state(n)
    explored = set({})
    frontier = Queue()
    solutions = 0
    frontier.put(initial_state)

    start = time()

    while not frontier.empty():
        print("n: {}, Solutions: {}, Queue: {}, States Checked: {}"
        .format(n,solutions,frontier._qsize(),len(explored)),end='\r')

        state = frontier.get()

        if hash(str(state)) not in explored:
            explored.add(hash(str(state)))
            if not state_in_conflict(state):
                solutions+=1
                print('\n')
                print_state(state)
                print('*'*90)

        for action in list(enumerate_actions(state)):
            #Check if state has already been explored
            if hash(str(action)) not in explored:
                #Add state to frontier
                frontier.put(action)
    print()
    print("Search time: {}".format(time()-start))

def HillClimbing(n):
    state = create_random_state(n)
    cost = state_in_conflict(state)
    solution_found = False
    restarts = 0

    start = time()
    while not solution_found:
        print("Restarts: {}".format(restarts),end='\r')
        old_cost = cost
        if state_in_conflict(state):
            for action in list(enumerate_actions(state)):
                new_cost = state_in_conflict(action)
                if new_cost < cost:
                    cost = new_cost
                    state = action
            if old_cost == cost:
                state = create_random_state(n)
                cost = state_in_conflict(state)
                restarts+=1
        else:
            solution_found = True
    #Print Solution
    print_state(state)
    print("Search Time: {}".format(time()-start))


class SimulatedAnnealing(object):
    def __init__(self,n):
        self.n = n
        self.state = create_random_state(self.n)
        self.k = 1000
        self.temp = self.k
        self.cost = None
        self.solution_found = False

    
    def random_select_neighbour(self):
        random_queen = self.state[randrange(0,self.n)]
        return random_queen


    def temp_func(self,n):
        return pow(0.99,n)

    def search(self):
        n = 0
        while not self.solution_found:
            print("Temp: {}".format(self.temp),end='\r')
            for _ in range(self.k):
                self.cost = state_in_conflict(self.state)
                if bool(self.cost):
                    random_neighbour = self.random_select_neighbour()
                    random_neighbour_cost = state_in_conflict(random_neighbour)

                    if random_neighbour_cost <= self.cost:
                        self.state = random_neighbour
                        self.cost = random_neighbour_cost
                    else:
                        p = pow(e,-(self.cost - random_neighbour_cost)/self.temp) 
                        if p > random():
                            self.state = random_neighbour
                            self.cost = random_neighbour_cost
                else:
                    self.solution_found = True
                    print_state(self.state)
                    break
            self.temp -= self.temp_func(n)
            n+=1


def main():
    n = int(sys.argv[1])
    HillClimbing(n)


if __name__ == "__main__":
    main() 
import queens.state as state
import queens.search as search

def main():
    n = 5

    #i_state = [(0,0),(0,2),(2,0),(1,2)]
    state1 = state.STATE(5,None)
    state1.print_state()
    state1.enumerate_legal_successor_states()

if __name__ == "__main__": 
    main()

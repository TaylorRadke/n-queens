import queens.state as state
import queens.search as search

def main():
    n = 4

    state1 = state.STATE(n,None)
    state1.print_state()
    state1.enumerate_legal_successor_states()

if __name__ == "__main__": 
    main()

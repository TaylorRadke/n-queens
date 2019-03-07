import board.state as state
import board.search as search

def main():
    n = 4

    state1 = state.STATE(n)
    state1.set_state([(0,0),(1,1),(2,2),(3,3)])
    state1.print_state()


   
if __name__ == "__main__": 
    main()

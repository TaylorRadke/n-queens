import searchtree

def main():
    n = 4
    state1 = searchtree.BOARDSTATE(n)
    state1.create_random_initial_state()
    leaf1 = searchtree.LEAFNODE(None,state1)
    leaf1.enumerate_legal_state_actions()
   
if __name__ == "__main__": 
    main()

import queens.search as search
import sys
from queens.state import State

def main():
    n = int(sys.argv[1])
    search.SimulatedAnnealing(n).search()
        
if __name__ == "__main__":
    main() 
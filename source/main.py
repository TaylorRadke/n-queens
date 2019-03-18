import queens.search as search
import sys
from queens.state import State

def main():
    n = int(sys.argv[1])
    State(n).print_state()

if __name__ == "__main__":
    main() 
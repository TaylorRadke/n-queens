from queens.search import BFS
import sys
from queens.state import State

def main():
    n = int(sys.argv[1])
    BFS(n).search()

if __name__ == "__main__":
    main() 
import queens.state as state
import queens.search as search
import sys

def main():
    n = int(sys.argv[1])
    print(n)
    tree = search.BFS(n)
    tree.search()

if __name__ == "__main__": 
    main()

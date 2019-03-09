import queens.search as search
import sys

def main():
    n = int(sys.argv[1])
    search.BFS(n).search()

if __name__ == "__main__": 
    main()

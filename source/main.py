import queens.state as state
import queens.search as search

def main():
    n = 5
    tree = search.BFS(n)
    tree.search()

if __name__ == "__main__": 
    main()

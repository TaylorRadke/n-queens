import queens.search as search
import sys
import csv
import os
def main():
    n = int(sys.argv[1])
    sample_size = int(sys.argv[2])
    csv_ = os.path.join("results",'results.csv')

    with open(csv_,'a',newline='') as csv_file:
        csv_writer = csv.writer(csv_file,)
        for n in range(1,n+1):
            for _ in range(sample_size):
                tree = search.BFS(n,logging=csv_writer)
                tree.search()
                del tree
                csv_file.flush()

if __name__ == "__main__":
    main()

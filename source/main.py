import queens.search as search
import sys
import csv

def main(n,sample_size):
    with open("results.csv",'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for n in range(n):
            for i in range(sample_size):
                search.BFS(n,logging=csv_writer).search()

if __name__ == "__main__": 
    main(int(sys.argv[1]),int(sys.argv[2]))

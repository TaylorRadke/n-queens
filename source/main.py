import queens.search as search
import sys
import csv
import os

def main():
    # n = int(sys.argv[1])
    # sample_size = int(sys.argv[2])
    # csv_ = os.path.join("results",'results.csv')
    
    
    search.BFS(5).search()
    # n = 5
    # sample_size = 1
    # with open("results\\results.csv",'w',newline='') as csv_file:
    #     csv_writer = csv.writer(csv_file,)
    #     for n in range(n,n+1):
    #         for _ in range(sample_size):
    #             search.BFS(n,logger=csv_writer).search()
    #             csv_file.flush()

if __name__ == "__main__":
    main()

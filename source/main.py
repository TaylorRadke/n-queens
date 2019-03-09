import queens.search as search
import sys
import csv

def main():
    with open("results.csv",'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for n in range(1,6):
            for i in range(5):
                initial_state,search_time,solution = search.BFS(n).search()
                csv_writer.writerow([n,search_time,initial_state,solution])

if __name__ == "__main__": 
    main()

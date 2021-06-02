import csv
import sys

file_name = sys.argv[1]

def sortFirstThree(arr):
  arr.sort(key=lambda x : x[1])
  if len(arr) > 3:
    arr.pop(0) 
  return arr

file =  open(file_name)
csv_reader = csv.reader(file, delimiter=',')
line_count = 0
titles = []
toppers = []
top_rankers = []
for row in csv_reader:
    if line_count == 0:
        for col in row[1:]:
          titles.append(col)
          toppers.append(('Name', 0))
    else:
      total = 0
      for i in range(1,len(row)):
        if int(toppers[i-1][1]) < int(row[i]):
          toppers[i-1] = (row[0], row[i])
        total+=int(row[i])
      top_rankers.append((row[0], total))
      top_rankers = sortFirstThree(top_rankers)
    line_count += 1

# Print results
for i in range(len(titles)):
  print(f"Topper in {titles[i]} is {toppers[i][0]}")
print(f"Best students in the class are {top_rankers[2][0]}, {top_rankers[1][0]} and {top_rankers[0][0]}")

# The time complexity is O(rc)
# where r is the number of rows in the list and c is the number of columns
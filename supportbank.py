import csv

with open('Transactions2014.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
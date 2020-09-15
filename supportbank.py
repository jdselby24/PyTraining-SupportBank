import csv

class Person:
    name = ''
    transactions =[]
    owed = 0
    owes = 0

    def __init__(self, name):
        self.name = name

    def addFromTrasaction(self, transaction):
        self.transactions.append(transaction)

    def addToTransaction(self, transaction):
        self.transactions.append(transaction)

class Transaction:
    date = ''
    fromPerson = ''
    toPerson = ''
    narrative = ''
    value = 0

    def __init__(self, date, fromPerson, toPerson, narrative, value):
        self.date = date
        self.fromPerson = fromPerson
        self.toPerson = toPerson
        self.narrative = narrative
        self.value = value

allTransactions = []
people = {}

with open('Transactions2014.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
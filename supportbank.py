import csv

class Person:
    name = ''
    transactions =[]
    owed = 0
    owes = 0

    def __init__(self, name):
        self.name = name

    def addFromTransaction(self, transaction):
        self.transactions.append(transaction)
        self.owes -= transaction.value

    def addToTransaction(self, transaction):
        self.transactions.append(transaction)
        self.owed += transaction.value

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
        valAmount = int(row['Amount'].replace('.',''))
        transact = Transaction(row['Date'], row['From'], row['To'], row['Narrative'], valAmount)
        
        if transact.fromPerson not in people.keys():
            people[transact.fromPerson] = Person(transact.fromPerson)
        
        people[transact.fromPerson].addFromTransaction(transact)

        if transact.toPerson not in people.keys():
            people[transact.toPerson] = Person(transact.toPerson)

        people[transact.toPerson].addToTransaction(transact)

print(people)

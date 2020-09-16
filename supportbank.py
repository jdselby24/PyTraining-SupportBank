import csv
import re

import logging
logging.basicConfig(filename='SupportBank.log', filemode='w',
level=logging.DEBUG)

class Person:
    name = ''
    transactions = []
    owed = 0
    owes = 0

    def __init__(self, name):
        self.name = name
        self.transactions = []

    def addFromTransaction(self, transaction):
        self.transactions.append(transaction)
        self.owes += transaction.value

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

class DateException(Exception):
    pass

def printPoundsPence(value):
    val = str(value)
    
    return val[:(len(val)-2)] + '.' + val[2:]

allTransactions = []
people = {}

def listAll(people):
    for person in people.values():
        print("Name: " + person.name)
        print("Owes: " + str((person.owes)))
        print("Owed: " + str((person.owed)))
        print("------")

def listName(people, name):
    person = people[name]
    for transaction in person.transactions:
        print(transaction.date + ' | From:' + transaction.fromPerson + ' | To:' + transaction.toPerson + ' | Narrative:' + transaction.narrative + ' | Amount:' + str(transaction.value))

datePattern = re.compile("([0-9]{2}\/[0-9]{2}\/[0-9]{4})")

with open('DodgyTransactions2015.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            if not datePattern.match(row['Date']):
                raise DateException()

            valAmount = int(row['Amount'].replace('.',''))

            transact = Transaction(row['Date'], row['From'], row['To'], row['Narrative'], valAmount)
        
            if transact.fromPerson not in people.keys():
                people[transact.fromPerson] = Person(transact.fromPerson)
            
            people[transact.fromPerson].addFromTransaction(transact)

            if transact.toPerson not in people.keys():
                people[transact.toPerson] = Person(transact.toPerson)

            people[transact.toPerson].addToTransaction(transact)

        except ValueError:
            print('')
            print("WARNING: Ammount for transaction was not numeric")
            print("         Value Given: " + row['Amount'])
            print("         on row: " + str(row))
            print('')
        except DateException:
            print('')
            print("WARNING: Date format incorrect")
            print("         Value Given: " + row['Date'])
            print("         on row: " + str(row))
            print('')
        

name = 'Dan W'

listAll(people)

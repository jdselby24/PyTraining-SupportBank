import csv
import re

from os import path

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

allTransactions = []
people = {}

def loadFile():
    filename = input("Please eneter a filename to load: ")
    if not filename == "EXIT":
        filenamePattern = re.compile("[a-zA-Z0-9\"\*\/\:\<\>\?\\\|]{1,255}[\.]{1}[a-zA-Z0-9]{1,255}")
        if filenamePattern.match(filename):
            if path.exists(filename):
                extension = filename.split('.')[1]
                if extension == "csv":
                    processCsv(filename)
                elif extension == "json":
                    pass
                else:
                    pass
            else:
                print("File does not exist")
                loadFile()
        else:
            print("Invalid file name")
            loadFile()

def processCsv(filename):
    with open(filename, newline='') as f:
        counter = 0
        logging.info("Loading file" + str(f.name))
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

                counter += 1

            except ValueError:
                logging.warning("Ammount for transaction was not numeric   Value Given:"  + row['Amount']+  " on row: " + str(counter) )

                print('')
                print("WARNING: Ammount for transaction was not numeric")
                print("         Value Given: " + row['Amount'])
                print("         on row: " + str(counter))
                print('')
            except DateException:
                logging.warning("Date format incorrect   Value Given:"  + row['Date']+  " on row: " + str(counter) )

                print('')
                print("WARNING: Date format incorrect")
                print("         Value Given: " + row['Date'])
                print("         on row: " + str(counter))
                print('')
        
        logging.info("Loaded " + str(counter) + " rows")

loadFile()
listAll(people)

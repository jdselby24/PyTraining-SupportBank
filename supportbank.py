import csv
import re

from os import path

import json

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

datePattern1 = re.compile("([0-9]{2}\/[0-9]{2}\/[0-9]{4})")
datePattern2 = re.compile("([0-9]{2}\-[0-9]{2}\-[0-9]{4})")
datePattern3 = re.compile("([0-9]{2}\.[0-9]{2}\.[0-9]{4})")

datePattern4 = re.compile("([0-9]{4}\/[0-9]{2}\/[0-9]{2})")
datePattern5 = re.compile("([0-9]{4}\-[0-9]{2}\-[0-9]{2})")
datePattern6 = re.compile("([0-9]{4}\.[0-9]{2}\.[0-9]{2})")

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
                    logging.info("Loading file" + str(filename))
                    processCsv(filename)
                elif extension == "json":
                    logging.info("Loading file" + str(filename))
                    processJson(filename)
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
        reader = csv.DictReader(f)
        csvKeySet = {'Date': 'Date', 'From': 'From', 'To': 'To', 'Narrative': 'Narrative', 'Amount': 'Amount'}
        dictProcessor(reader, csvKeySet)
        
def processJson(filename):
    with open(filename, 'r') as f:
        json_dict = json.load(f)
        jsonKeySet = {'Date': 'date', 'From': 'fromAccount', 'To': 'toAccount', 'Narrative': 'narrative', 'Amount': 'amount'}
        dictProcessor(json_dict, jsonKeySet)

def dictProcessor(dict,keySet):
    counter = 0
    for row in dict:
            try:
                if not (datePattern1.match(row[keySet['Date']]) 
                or datePattern2.match(row[keySet['Date']]) 
                or datePattern3.match(row[keySet['Date']])
                or datePattern4.match(row[keySet['Date']])
                or datePattern5.match(row[keySet['Date']])
                or datePattern6.match(row[keySet['Date']])):
                    raise DateException()

                valAmount = int(str(row[keySet['Amount']]).replace('.',''))

                transact = Transaction(row[keySet['Date']], row[keySet['From']], row[keySet['To']], row[keySet['Narrative']], valAmount)
            
                if transact.fromPerson not in people.keys():
                    people[transact.fromPerson] = Person(transact.fromPerson)
                
                people[transact.fromPerson].addFromTransaction(transact)

                if transact.toPerson not in people.keys():
                    people[transact.toPerson] = Person(transact.toPerson)

                people[transact.toPerson].addToTransaction(transact)

                counter += 1

            except ValueError:
                logging.warning("Ammount for transaction was not numeric   Value Given:"  + row[keySet['Amount']] +  " on row: " + str(counter) )

                print('')
                print("WARNING: Ammount for transaction was not numeric")
                print("         Value Given: " + row['Amount'])
                print("         on row: " + str(counter))
                print('')
            except DateException:
                logging.warning("Date format incorrect   Value Given:"  + row[keySet['Date']]+  " on row: " + str(counter) )

                print('')
                print("WARNING: Date format incorrect")
                print("         Value Given: " + row[keySet['Date']])
                print("         on row: " + str(counter))
                print('')
        
    logging.info("Loaded " + str(counter) + " rows")


loadFile()
listAll(people)


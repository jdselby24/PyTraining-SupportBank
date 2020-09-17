import csv
import re

from os import path

import json

import logging
logging.basicConfig(filename='SupportBank.log', filemode='w',
level=logging.DEBUG)

from datetime import date, timedelta

import xmltodict
import xml.etree.ElementTree as ET

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
        self.owes += int(transaction.value)

    def addToTransaction(self, transaction):
        self.transactions.append(transaction)
        self.owed += int(transaction.value)

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

datePattern1 = re.compile("([0-9]{2}[\/\-\.]{1}[0-9]{2}[\/\-\.]{1}[0-9]{4})")
datePattern2 = re.compile("([0-9]{4}[\/\-\.]{1}[0-9]{2}[\/\-\.]{1}[0-9]{2})")

allTransactions = []
people = {}

def exlDateConverter(delta):
    origin = date(1900,1,1)
    return str(origin + timedelta(days=delta))

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

                elif extension == "xml":
                    logging.info("Loading file" + str(filename))
                    processXml(filename)

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

def processXml(filename):
    with open(filename, 'r') as f:
        counter = 0
        print(f)
        tree = ET.parse(f)
        xml_data = tree.getroot()
        xmlstr =  ET.tostring(xml_data, encoding='utf-8', method='xml')
        doc = xmltodict.parse(xmlstr)
        print(xmlstr)
        for trnsct in doc['TransactionList']:
            date = exlDateConverter(trnsct['@Date'])
            fromAcc = trnsct['Parties']['From']
            toAcc = trnsct['Parties']['To']
            narr = trnsct['Description']
            amo = trnsct['Value']

            rowProcessor(date, fromAcc, toAcc, narr, amo, counter)

            counter + 1

def rowProcessor(date,fromAcc,toAcc,narr,amo, counter):
    try:
        if not (datePattern1.match(date)
        or datePattern2.match(date)):
            raise DateException()

        valAmmount = int(str(amo).replace('.',''))

        transact = Transaction(date, fromAcc, toAcc, narr, valAmmount)

        if transact.fromPerson not in people.keys():
            people[transact.fromPerson] = Person(transact.fromPerson)

        people[transact.fromPerson].addFromTransaction(transact)

        if transact.toPerson not in people.keys():
            people[transact.toPerson] = Person(transact.toPerson)

        people[transact.toPerson].addToTransaction(transact)

    except ValueError:
        logging.warning("Ammount for transaction was not numeric   Value Given:"  + amo +  " on row: " + str(counter) )

        print('')
        print("WARNING: Ammount for transaction was not numeric")
        print("         Value Given: " + amo )
        print("         on row: " + str(counter))
        print('')
    
    except DateException:
        logging.warning("Date format incorrect   Value Given:"  + date +  " on row: " + str(counter) )

        print('')
        print("WARNING: Date format incorrect")
        print("         Value Given: " + date)
        print("         on row: " + str(counter))
        print('')

def dictProcessor(dict,keySet):
    counter = 0
    for row in dict:
            counter + 1
            rowProcessor(row[keySet['Date']], row[keySet['From']], row[keySet['To']], row[keySet['Narrative']], row[keySet['Amount']], counter)
            

loadFile()
listAll(people)
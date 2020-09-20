#############################
##     HACK ZURICH 2020    ##
##                         ##
##  Author: Simon C. Stock ##
##                         ##
##  For the Team of AiLaw  ##
#############################

# install list to make it work:
# 
#  pip install Py3DNS
#  pip install validate_email
#  pip install wikipedia
#  pip install datefinder
#

#
# Important Note: Some Computers had issues with DNS Servers, therefore activate the right function in the mail check software down below.
#                 If check_mx=False NO DNS Check will be performed. And only the form of the email is checked.
#


import numpy
import datefinder
from datetime import date
import datetime
from enum import Enum  # for enum34, or the stdlib version
import wikipedia
import random
from validate_email import validate_email

## Umrechnung von Moneyz und so https://pypi.org/project/CurrencyConverter/

def week(i):
    switcher={
            0:'Monday',
            1:'Tuesday',
            2:'Wednesday',
            3:'Thursday',
            4:'Friday',
            5: 'Saturday',
            6:'Sunday'
         }
    return switcher.get(i,"Invalid day of week")

def brAIn(inputString):
    # from aenum import Enum  # for the aenum version
    Entscheider = Enum('Entscheider', 'datum geld wiki mail')
    entscheidung = -1 # To save what it actually was

    # Get input string from outside
    #inputString = ""
    outputString = ""

    example1 = "600 USD" # Umrechnungs API ???
    example2 = "Saul Goodman" # Linked in API
    example3 = "Dies war 24.10.1648" # Kalender API
    example4 = "Logitech"  # Wiki API
    example5 = "Technopark Technoparkstrasse 1 8005 Zürich Schweiz"  # Maps
    example6 = "mariuswanner@gmail.com"
  #  mariuswanner@gmx.de



    # Decide what the String is all about

    # Check for Dates
    string_with_dates = inputString
    matches = datefinder.find_dates(string_with_dates)
    for match in matches:
        firstMatch = match
        entscheidung = Entscheider.datum
        theWeekday = match.weekday
        break

    # check for @
    if (inputString.find('@') > 0):
        #is_validmail = validate_email(inputString, verify=True) #check_mx=True) # Will check the domain
        is_validmail = validate_email(inputString, check_mx=False)# will only check the mailing adress if it is somehow possible
        entscheidung = Entscheider.mail
            

    #############################################################
    ## If nothing else is fitting we look up in the wikipedia ...
    if (entscheidung == -1):
        wikipedia.set_lang("en")

        try:
            wPage = wikipedia.page(inputString)
            wShortDesc = wikipedia.summary(inputString, sentences=2)
        except wikipedia.DisambiguationError as e:
            s = e.options[0]
            wPage = wikipedia.page(s)
            wShortDesc = wikipedia.summary(s, sentences=2)
        wTitle = wPage.title
        wURL = wPage.url
        entscheidung = Entscheider.wiki

        #print(wikipedia.suggest(inputString)) # can be used if nothing is found on the normal way



    ##########################################################################################################################
    #############################  GENERATE OUTPUT CONTENT ###################################################################
    ##########################################################################################################################

    if (entscheidung == Entscheider.datum):  # it was a date!!
        d0 = date.today()
        d1 = match.date()
        delta = d0 - d1
        years = delta.days / int(365)
        days = delta.days % 365
        outputString = '' + week(match.weekday()) + '\n' + str(int(years)) + ' years and ' + str(days) + ' days ago'

    if (entscheidung == Entscheider.mail):
        if (is_validmail == True):
            print('SMTP check completed.\nThis mail is valid.')
            outputString = inputString + ' is a valid mail address'
        else:
            print('SMTP check failed!\nThis is NOT a valid mail adress')
            outputString = inputString + ' is NOT a valid mail address'    

    if (entscheidung == Entscheider.wiki):
        outputString = 'From Wikipedia \'' + wTitle + '\':\n' + wShortDesc + '\nFrom: ' + wURL

    # Debug outputs for testing
    
    #print(outputString)
    return outputString


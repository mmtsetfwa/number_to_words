# -*- coding: utf-8 -*-
"""
    Spyder Editor
"""
#0-9 ones
#10-19 tens
#20-99 tens
#100-999 hundreds
#1,000-999,000 thousands
#1,000,000-999,000,000 millions
#1,000,000,000-999,000,000,000 billions
"""
    The starting point of the solution is to recognize that any number can be 
    broken down to hundreds, tens and ones. Even a billion or a thrillion can
    be broken down into these components.
    
    We need to handle ones from 0 to 9 as a separate group.
    Tens can be broken down to two groups: namely the 10 - 19 range and the 
    20 - 99 range.
    
    I chose to use Python dictionaries for these groupings but could have used
    a case statements.
    
    Solution flow:
    Loop through the file input and process each line per iteration.
    For each line feed the string into a regular expression processor in Python
    to extract digits. A valid input will return result with a list containing one 
    item else the input does not have a valid number.
    
    Process the number starting on the highest grouper if applicable for example
    billions part, millions part, thousands part, hundreds part, tens and lastly ones.
    Discard the part that has been processed but append words part to a string that is 
    being concatenated as we go. This means the number in its string representation
    processed as a Python list is reducing in size as we go through the different
    groups. Processing number as string because strings are subscriptable in python
    whereas integers are not.
    
    Billions, millions, thousands and hundreds are all handled by one function because they
    all range from 1 to 999. The same concept can be used to process Trillions etc; block
    for processing it can be added.
    
    Leaving some of the commented printlines on the code to show thought process and
    debugging side steps that I went through.
    
    Steps for running code:
    Amend input file path file to your path, then run script.
    
    
    
"""
import re

ones_mapper = {
        '0':"",'1':"one",'2':"two",'3':"three",'4':"four",'5':"five",
        '6':"six",'7':"seven",'8':"eight",'9':"nine"
        }
ten_nineteen_mapper = {'10':"ten",'11':"eleven",'12':"twelve",'13':"thirteen",
                     '14':"fourteen", '15':"fifteen",'16':"sixteen",'17':"seventeen",
                     '18':"eighteen",'19':"nineteen"
              }
twenty_ninetynine_mappper = {'2':"twenty",'3':"thirty",'4':"fourty",'5':"fifty",
                           '6':"sixty",'7':"seventy",'8':"eighty",'9':"ninety"}
def hundreds_handler(key):
    units = ""
    if int(key) < 10:
        units = ones_mapper[key]
    elif int(key) >= 10 and int(key) < 20:
        units = ten_nineteen_mapper[key]
    elif int(key) >= 20 and int(key) < 100:
        units = twenty_ninetynine_mappper[key[0]] + " "+ones_mapper[key[1]]
    elif int(key) >= 100 and int(key) < 1000:
        units = ones_mapper[key[0]] + " hundred"#
        if int(key[-2:]) >= 10 and int(key[-2:]) < 20:
            units += ten_nineteen_mapper[key[:-2]]
        elif int(key[-2:]) >= 20 and int(key[-2:])< 100:
            units += " and "+twenty_ninetynine_mappper[key[-2:][0]] + " "+ones_mapper[key[-2:][1]]
    return units

def get_valid_number(line):
    digits = re.findall('\d+', line )
    if len(digits)==1:
        return digits[0]    
    return None        

file = open("C:\\Users\\27828\\test_case_inputs.txt","r")
lines = file.readlines()

for line in lines:#loop through all lines in the file
    
    string_repr = ''
    valid_number = get_valid_number(line)
    original_number = valid_number
    if valid_number:
        print('Trying to convert %s to int' % valid_number)
        if len(valid_number)>= 10 and len(valid_number)<= 12:#billions
            key = str(int(valid_number[:-9]))
            #print("Billions key %s" % key)       
            billions = hundreds_handler(key)
            string_repr = billions + ' billion '
            valid_number = valid_number[-9:]#slicing
            #print('This is what remains after slicing: %s' % item)
        
        if len(valid_number)>= 7 and len(valid_number)<= 9:#millions
            key = str(int(valid_number[:-6]))#helps with discarding leading zeros like 003 million, becomes 3
            #print('Key is % s'% key) 
            millions = hundreds_handler(key)
            if millions!="":
                string_repr += millions + ' million'
            valid_number = valid_number[-6:]#slicing
            #print('This is what remains after slicing: %s' % item)
    
        if len(valid_number) >= 4 and len(valid_number)<= 6:#thousands
            key = str(int(valid_number[:-3]))
            #print('Key is % s'% key)    
            thousands = hundreds_handler(key)
            if thousands!="":
                string_repr += " "+ thousands + ' thousand'
            valid_number = valid_number[-3:]#slicing
            #print('This is what remains after slicing: %s' % item)
            
        if len(valid_number) == 3:#hundreds
            #print("In hudreds")
            key = str(int(valid_number[:-2]))
            #print('Key is % s'% key)
            hundreds = hundreds_handler(key)
            #print('Hundreds: %s' % hundred_units)
            if hundreds != "":
                string_repr += " "+hundreds + ' hundred'
            valid_number = valid_number[-2:]#slicing
            #print('This is what remains after slicing: %s' % item)
            
        if len(valid_number) == 2:#tens
            #print("In tens: key %s" % valid_number)            
            if(int(valid_number) >= 10 and int(valid_number) <= 19):
                tens = ten_nineteen_mapper[valid_number]
                valid_number = valid_number[-1:]# slicing further reduction to remain with ones
            elif(int(valid_number) >= 20 and int(valid_number) <= 99):
                tens_part_one = twenty_ninetynine_mappper[valid_number[0]]
                tens_part_two = ones_mapper[valid_number[1]]  
                tens = tens_part_one + " "+ tens_part_two  
                valid_number = []
            if tens != "":
                if string_repr != "":
                    string_repr += " and " + tens 
                else:
                    string_repr += tens               
            valid_number = valid_number[-1:]#slicing
            tens=""
            
        if len(valid_number) == 1:#ones  
            #print("In ones")
            ones = ones_mapper[valid_number]
            if ones!="":
                if string_repr != "" and int(valid_number) != 0:                    
                    string_repr += " and " + ones
                else:
                    string_repr += ones                        
            #break                    
    
        print("Number: %s in words is: %s \n" % (original_number,string_repr))
        #break
    else:
        print("Invalid Input: %s" % line)
            
file.close()

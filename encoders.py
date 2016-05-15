

dayConversion = {
    'year':365,
    'month':30,
    'week':7,
    'day':1
}

def EncodeAgeInDays(age):
    """Take in a string age, return the value in units of days."""
    try:
        input  = age.split()
    except:
        return -1
        
    number = int(input[0])
    
    if input[1][-1] == 's':
        input[1] = input[1][:-1]
    factor = dayConversion[input[1]]

    return number*factor  


def EncodeColor(color):
    """Encode mixed as 1, solid as 0"""
    if len(color.split()) == 1 and '/' not in color:
        return 0
    else:
        return 1    

def EncodeAnimalType(animal):
    """Encode cat=0 and dog=1."""
    if animal.lower() == 'cat':
        return 0
    elif animal.lower() == 'dog':
        return 1
    else:
        return 2

def EncodeBreed(breed):
    """Encode animal breed where Mix=1 and pure=0."""
    if 'mix' in breed.lower() or '/' in breed:
        return 1
    else:
        return 0    

def EncodeSexAndSterility(outcome):
    """Encode male=1, female=0 and sterile=1, intact=0."""
    try:
        data = outcome.split()
    except:
        return (-1,-1)
    if len(data) == 1:
        return (-1,-1)

    if data[1].lower() == 'male':
        sex = 1
    elif data[1].lower() == 'female':
        sex = 0

    if data[0].lower() == 'spayed' or data[0].lower() == 'neutered':
        sterility = 1
    elif data[0].lower() == 'intact':
        sterility = 0

    return (sex,sterility)

def EncodeOutcome(value):
    positive_outcomes = ['Adoption','Return to Owner']
    if value in positive_outcomes:
        return 1
    else:
        return 0

def EncodeSingleVariable(data):
    import numpy as np
    import pandas as pd
    
    # get unique values
    unique = np.unique(data)
    translator = {}
    cnt = 0

    # assign an integer to each unique value
    for k in unique:
        translator[k] = cnt
        cnt += 1

    # loop through all values and assign the proper integers
    vals = np.zeros(len(data),dtype=np.int32)
    i=0
    for d in data.iteritems():
        vals[i] = translator[d[1]]
        i += 1
        
    reverse_translator = {}
    for k,v in translator.iteritems():
        reverse_translator[v] = k
    
    return pd.Series(vals, index=data.index), reverse_translator

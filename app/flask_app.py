import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import sys
sys.path.insert(0,'../')
from model.shelter_model import ShelterModel

app = Flask(__name__)

# dropdown menu options
avail_age = dict(
    years=np.arange(0,30),
    months=np.arange(0,13),
    days=np.arange(0,32)
)

# return the result as a useful text string
result_key = {
    1:'adopted',
    0:'killed',
#    2:'euthanized',
#    3:'returned to owner',
#    #4:'transfered to another facility'
}

# create model reference
MODEL = ShelterModel()

# set max year to the max age in the dataset
avail_age['years'] = np.arange(int(MODEL.min_age / 365.),int(MODEL.max_age / 365.))


@app.route('/')
def index():
    """display form"""
    return render_template('index.html', age_options=avail_age)


@app.route('/query', methods=['POST'])
def query_animal():
    """gather form inputs and send them to the model for a prediction"""    
    rf = request.form

    # calculate the total age in days
    age = int(rf['age_years'])*365 + int(rf['age_months'])*30 + int(rf['age_days'])

    # check for missing data that is required
    missing = []
    if age == 0:
        missing.append('Pet Age')
    if 'animal_type' not in rf:
        missing.append('Pet Type')
    if 'animal_sex' not in rf:
        missing.append('Pet Sex')
    if len(missing) > 0:
        return render_template('error.html', missing=missing)

    
    # check to see if our animal is named
    if len(rf['name'].strip()) > 0:
        named = 1
    else:
        named = 0

    # assign sex
    if rf['animal_sex'] == 'male':
        sex = 1
    else:
        sex = 0

    # assign type
    if rf['animal_type'] == 'cat':
        animal_type = 0
    else:
        animal_type = 1

    # assign mixed
    if 'mixed_breed' in rf.keys():
        mixed = 1
    else:
        mixed = 0

    # assign spayed/neutered
    if 'fixed' in rf.keys():
        fixed = 1
    else:
        fixed = 0

        
    # create animal
    animal = np.array([age,mixed,named,sex,fixed,animal_type])

    # make a prediction on the user's input
    pred   = MODEL.predict(animal.reshape(1,-1))

    # get probabilities of prediction
    prob = MODEL.predict_probability(animal.reshape(1,-1))
    probabilities = {}
    cnt = 0
    for k,v in result_key.iteritems():
        probabilities[v] = '%05.2f' % (prob[cnt] * 100.)
        cnt += 1    
    
    # make a prediction with an opposite name entry
    if animal[2] == 0:
        animal[2] = 1
        has_name = False
    elif animal[2] == 1:
        animal[2] = 0
        has_name = True
    pred2  = MODEL.predict(animal.reshape(1,-1))
    prob2  = MODEL.predict_probability(animal.reshape(1,-1))
    print prob2
    
    # return the result 
    return render_template('results.html',
                           result=result_key[pred],
                           hypothetical=result_key[pred2],
                           has_name=has_name,
                           prob=probabilities,
                           accuracy='%0.0f%%' % (MODEL.accuracy_score*100))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

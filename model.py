import os
import numpy as np
import pandas as pd

import encoders as encode

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score

SEED          = 8675309
n_estimators  = 64
training_size = 0.2
outcome_file  = 'outcomes.csv'

translator = dict(
    Sex = {0:'male', 1:'female'},
    Named = {0:'Not named', 1:'Named'},
    Sterility = {0:'Not sterile', 1:'Sterile'},    
)

class Model(object):
    def __init__(self, *args, **kwargs):
        self.translator = translator
        
        self.download_data()
        self.read_data()
        self.process_data()
        self.create_model()

    def download_data(self):
        if not os.path.isfile(outcome_file):
            os.system('wget https://data.austintexas.gov/api/views/jpst-ix7f/rows.csv -O %s' % outcome_file)
            
    def read_data(self):
        self.input_data = pd.read_csv(outcome_file)

    def process_data(self):
        df   = pd.DataFrame()
        
        def drop_type(to_drop):
            n_drops = len(self.input_data[self.input_data['Outcome Type'] == to_drop])
            print('dropping %d %s (%0.2f%%)' %
                  (n_drops, to_drop, float(n_drops)/float(len(self.input_data)) * 100.))
            self.input_data = self.input_data.drop(
                self.input_data[self.input_data['Outcome Type'] == to_drop].index
            )
            
        # drop some results as they give us little insight
        self.input_data = self.input_data.drop(
            self.input_data[self.input_data['Outcome Type'].isnull()].index
        )
        drop_type('Transfer')
        drop_type('Missing')
        drop_type('Relocate')
        data = self.input_data
        
        # classify animal as being named or not-named
        df['Named'] = data['Name']
        df['Named'][data['Name'].isnull()]  = 0
        df['Named'][~data['Name'].isnull()] = 1

        # convert age to days
        df['AgeInDays'] = data['Age upon Outcome'].map(encode.EncodeAgeInDays)

        # classify sex and sterility
        sex_sterility    = data['Sex upon Outcome'].map(encode.EncodeSexAndSterility)
        df['Sex']        = sex_sterility.map(lambda x: x[0])
        df['Sterility']  = sex_sterility.map(lambda x: x[1])

        d = encode.EncodeSingleVariable(data['Animal Type'])
        self.translator['AnimalType'] = d[1]
        df['AnimalType'] = d[0]        

        df['Color']      = data['Color'].map(encode.EncodeColor)
        df['MixedBreed'] = data['Breed'].map(encode.EncodeBreed)
        df['Outcome']    = data['Outcome Type'].map(encode.EncodeOutcome)
                
        self.df = df
        
    def create_model(self):
        self.x = self.df[[
            'Named','AgeInDays','Sex',
            'Sterility','AnimalType','Color','MixedBreed'
        ]]
        self.y = self.df['Outcome']

        x_train, x_test, y_train, y_test = train_test_split(self.x, self.y,
                                                            train_size=training_size,
                                                            random_state=SEED)
        print('Training with %d values, testing with %d' % (len(x_train), len(x_test)))

        self.model = RandomForestClassifier(random_state=SEED, n_estimators=n_estimators)
        self.model.fit(x_train, y_train)
        pred = self.model.predict(x_test)
        self.accuracy_score = accuracy_score(y_test, pred)
        print('Accuracy score:',self.accuracy_score)
              

if __name__ == '__main__':
    model = Model()

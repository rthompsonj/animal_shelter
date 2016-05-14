import os
import numpy as np
import pandas as pd

from encoders import EncodeAgeInDays, \
    EncodeColor, EncodeAnimalType, \
    EncodeSexAndSterility, EncodeBreed, \
    EncodeSingleVariable

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

    def download_data(self):
        if not os.path.isfile(outcome_file):
            os.system('wget https://data.austintexas.gov/api/views/jpst-ix7f/rows.csv -O %s' % outcome_file)
            
    def read_data(self):
        self.input_data = pd.read_csv(outcome_file)

    def process_data(self):
        data = self.input_data
        df   = pd.DataFrame()
        
        # drop transfers because they do not tell us anything
        n_transfers = len(data[data['Outcome Type'] == 'Transfer'])
        print('dropping %d transfers (%0.2f%%)' %
              (n_transfers, float(n_transfers)/float(len(data)) * 100.))
        data = data.drop(data[data['Outcome Type'] == 'Transfer'].index)
        data = data.drop(data[data['Outcome Type'].isnull()].index)
        self.input_data = data
        
        # classify animal as being named or not-named
        df['Named'] = data['Name']
        df['Named'][data['Name'].isnull()]  = 0
        df['Named'][~data['Name'].isnull()] = 1

        # convert age to days
        df['AgeInDays'] = data['Age upon Outcome'].map(EncodeAgeInDays)

        # classify sex and sterility
        sex_sterility    = data['Sex upon Outcome'].map(EncodeSexAndSterility)
        df['Sex']        = sex_sterility.map(lambda x: x[0])
        df['Sterility']  = sex_sterility.map(lambda x: x[1])
        
        d = EncodeSingleVariable(data['Animal Type'])
        self.translator['AnimalType'] = d[1]
        df['AnimalType'] = d[0]        

        df['Color']      = data['Color'].map(EncodeColor)
        df['MixedBreed'] = data['Breed'].map(EncodeBreed)

        d = EncodeSingleVariable(data['Outcome Type'])
        self.translator['Outcome'] = d[1]
        df['Outcome']    = d[0]
        
        self.df = df
        
    def create_model(self):
        pass
        


if __name__ == '__main__':
    model = Model()

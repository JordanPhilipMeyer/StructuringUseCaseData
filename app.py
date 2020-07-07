# Take a json and the running data dictionary spreadsheet

import json
from random import randint
import pandas as pd

with open('usecase.json') as f:
    data = json.load(f)


# print(lookupValueTable.head())
def get_lookup_dict():
    lookup_value_table = pd.read_csv('ValueLookup.csv')
    testing = zip(lookup_value_table['Value'], lookup_value_table['ID'])
    lookup_dict = {x[0]: x[1] for x in testing}
    return lookup_dict, lookup_value_table


def updateValueSetCSV(option, tag, df):
    # new_row = pd.Series({'Value': option, 'ID': tag})
    df = df.append(pd.Series([option, tag], index=df.columns), ignore_index=True)
    df.to_csv('ValueLookup.csv', index=False)
    return df


lookup_table, lookup_df = get_lookup_dict()

for element in data['Data Elements']['Primary Outputs']:
    if element['Data Type'].lower() == 'categorical':
        print('this is a categorical value')
        print(element['Value Set'])
        valueIDPairing = {}
        for option in element['Value Set']:
            ## Look up the option from a generic look up table
            if option in lookup_table:
                print('the element exists in our lookup table!')
                valueIDPairing[option] = lookup_table[option]
            else:
                tag = randint(100000, 999999)
                valueIDPairing[option] = tag
                print(tag, option)
                lookup_df = updateValueSetCSV(option, tag, lookup_df)
                print(lookup_df.head())

        element['Value Set'] = valueIDPairing
        print(element['Value Set'])
print(data['Data Elements']['Primary Outputs'])

with open('updatedUseCase.json', 'w') as json_file:
    json.dump(data, json_file)

## still needs to send relevant data to a csv file

# Take a json and the running data dictionary spreadsheet

import json
from random import randint
import pandas as pd
import DataDictionaryAPI

with open('Use Cases/usecase.json') as f:
    data = json.load(f)


# print(lookupValueTable.head())
def get_lookup_dict():
    """ Loads up the data element look up table stored as a CSV. Returns the data element and
    ID as a dictionary and the pandas data frame. We will use this df as an easy way to save and
    update the CSV later."""
    lookup_value_table = pd.read_csv('ValueLookup.csv')
    testing = zip(lookup_value_table['Value'], lookup_value_table['ID'])
    lookup_dict = {x[0]: x[1] for x in testing}
    return lookup_dict, lookup_value_table


def updateValueSetCSV(option, tag, df):
    """ Saves the new dataframe after we add new elements to the lookup table."""
    # new_row = pd.Series({'Value': option, 'ID': tag})
    df = df.append(pd.Series([option, tag], index=df.columns), ignore_index=True)
    df.to_csv('ValueLookup.csv', index=False)
    return df


def updateDataElementsWithIDTag(data, lookup_df, lookup_table, element_type='Primary Outputs'):
    """ This function runs through the data element outputs (default = Primary) and updates each categorical data element with
    random ID number tags. This function returns the json of the updated use case.

     Remember to run on primary and secondary data elements."""
    for element in data['Data Elements'][element_type]:
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
                    while tag in lookup_table.values():
                        tag = randint(100000, 999999)
                    valueIDPairing[option] = tag
                    print(tag, option)
                    updateValueSetCSV(option, tag, lookup_df)
                    # print(lookup_df.head())

            element['Value Set'] = valueIDPairing
            print(element['Value Set'])
        new_record = DataDictionaryAPI.format_new_record_for_data_dictionary(element, data, element_type)
        DataDictionaryAPI.update_DD_CSV(new_record)
    print(data['Data Elements'][element_type])
    return data


lookup_table, lookup_df = get_lookup_dict()
## Add try/except block here
data = updateDataElementsWithIDTag(data, lookup_df, lookup_table, 'Primary Outputs')
data = updateDataElementsWithIDTag(data, lookup_df, lookup_table, 'Secondary Outputs')


with open('Use Cases/updatedUseCase.json', 'w') as json_file:
    json.dump(data, json_file)

## still needs to send relevant data to a csv file

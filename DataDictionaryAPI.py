import csv
import json

# with open('Use Cases/updatedUseCase.json') as f:
#     data = json.load(f)

with open('DataDictionary.csv', newline='') as f:
    reader = csv.reader(f)
    data_dictionary_header = next(reader)  # gets the first line
    index_dd_header = {'CommonElementName': data_dictionary_header.index('CommonElementName'),
                       'Description': data_dictionary_header.index('Description'),
                       'ElementType': data_dictionary_header.index('ElementType'),
                       'Unit': data_dictionary_header.index('Unit'),
                       'Element_Allowed_Values_Def': data_dictionary_header.index('Element_Allowed_Values_Def'),
                       'Source': data_dictionary_header.index('Source'),
                       'Program-PReference': data_dictionary_header.index('Program-PReference'),
                       'RegistryName': data_dictionary_header.index('RegistryName'),
                       'RegistryElementName': data_dictionary_header.index('RegistryElementName'),
                       'Registry_allowed_values_Defination_Notes': data_dictionary_header.index('Registry_allowed_values_Defination_Notes'),
                       'Usage': data_dictionary_header.index('Usage'),
                       'Cardinality': data_dictionary_header.index('Cardinality'),
                       'Hint': data_dictionary_header.index('Hint'),
                       'FirstActiveVersion': data_dictionary_header.index('FirstActiveVersion'),
                       'Category': data_dictionary_header.index('Category'),
                       'Procedure': data_dictionary_header.index('Procedure'),
                       'Modality': data_dictionary_header.index('Modality'),
                       'BodyArea': data_dictionary_header.index('BodyArea'),
                       'Anatomy': data_dictionary_header.index('Anatomy')
                       }

def update_value_set_dict_to_dd_string(dict):
    response = ''
    for item in dict.items():
        response = response + str(item[1]) + '!' + str(item[0]) + '| '

    response = response[:-2]
    return response





def format_new_record_for_data_dictionary(data_element, data, Usage ='Primary Outputs'):
    """ This will update the data dictionary csv with the relevant data from the use case json. Default is a primary data element"""
    new_record = [''] * 32
    new_record[index_dd_header['CommonElementName']] = data_element['Data Element']
    new_record[index_dd_header['Description']] = data_element['Definition']
    new_record[index_dd_header['Hint']] = data_element['Definition']

    if (data_element['Data Type'] == 'categorical') | (data_element['Data Type'] == 'categoric'):
        new_record[index_dd_header['ElementType']] = 'enumerated'

        new_record[index_dd_header['Registry_allowed_values_Defination_Notes']] = update_value_set_dict_to_dd_string(data_element['Value Set'])
        new_record[index_dd_header['Element_Allowed_Values_Def']] = update_value_set_dict_to_dd_string(
            data_element['Value Set'])

    if (data_element['Data Type'] == 'numeric') | (data_element['Data Type'] == 'numerical'):
        new_record[index_dd_header['ElementType']] = 'float'

    if (data_element['Units'] != 'n/a') and (data_element['Units'] != ''):
        new_record[index_dd_header['Unit']] = data_element['Units']

    new_record[index_dd_header['Source']] = 'DSI'

    new_record[index_dd_header['Program-PReference']] = data['Core Features']['Panel']+ " Panel"

    new_record[index_dd_header['RegistryElementName']] = data_element['Data Element']
    new_record[index_dd_header['RegistryName']] = data_element['Data Element']

    new_record[index_dd_header['Usage']] = 'Required'
    if Usage != 'Primary Outputs':
        new_record[index_dd_header['Usage']] = 'Optional'
    new_record[index_dd_header['Cardinality']] = 'One'

    new_record[index_dd_header['FirstActiveVersion']] = 1

    new_record[index_dd_header['Category']] = 'Image'

    useCaseProcedure= data['Data Elements']['Execution Conditions']['Procedure']['Procedure']
    useCaseProcedure = useCaseProcedure.replace(',', '|')
    new_record[index_dd_header['Procedure']] = useCaseProcedure

    new_record[index_dd_header['Modality']] = data['Data Elements']['Execution Conditions']['Procedure']['Modality']

    new_record[index_dd_header['BodyArea']] = data['Data Elements']['Execution Conditions']['Procedure']['Body Area']

    new_record[index_dd_header['Anatomy']] = data['Data Elements']['Execution Conditions']['Procedure']['Anatomy']

    return new_record

def update_DD_CSV(new_record):
    # new_record = format_new_record_for_data_dictionary(element, data)

    with open(r'DataDictionary.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(new_record)

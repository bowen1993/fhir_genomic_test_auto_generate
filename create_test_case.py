'''
automative test case generator based on resource defination
@author: Bowen
'''

import csv
import json
import random
import string
from datetime import datetime, date
from type_generator import *
from config import *


possibles = globals().copy()
possibles.update(locals())

def trans_csv_to_dict(desc_csv_file):
    '''
    transform csv description file to dict object

    @param desc_csv_file: description csv file
    @type desc_csv_file: csv.reader
    @return description dict
    @rtype dict
    '''
    res_dict = {}
    headers = []
    for index, row in enumerate(desc_csv_file):
        if index == 0:
            headers = row
        else:
            element = row[0]
            res_dict[element] = {}
            for subindex in range(1, len(headers)):
                res_dict[element][headers[subindex]] = row[subindex]
    return res_dict

def remove_prefix(element):
    return element[element.find('.')+1:]

def is_sub_element(element):
    return ['.' in element, None if '.' not in element else element[:element.find('.')]]

def create_one_case(element_type, demand_value=None):
    '''
    create ont test case for a certain type. For reference type, a reference must be putted in demand value. Other type can be generate without and value

    @param element_type: type to be generated, required
    @type element_type: str
    @param demand_value: user defined datas
    @type demand_value: dict
    @return generated type value
    '''
    if element_type.lower() == 'resource':
        if demand_value and 'reference' in demand_value:
            return create_reference(demand_value['reference'])
        else:
            return None
    method_name = 'create_%s' % element_type.lower()
    method = possibles.get(method_name)
    if not method:
        return None
    if demand_value:
        return method(**demand_value)
    else:
        return method()

def create_cases(element_type, length, demand_values=None):
    if length < 1:
        return None
    if length == 1:
        return create_one_case(element_type, demand_values[0] if demand_values else None)
    results = []
    if element_type.lower() in customed_multi_list:
        method_name = 'create_multi_%s'%element_type.lower()
        method = possibles.get(method_name)
        if not method:
            pass
        else:
            results.extend(method(length,demand_values))
    else:
        for i in range(length):
            results.append(create_one_case(element_type,demand_values[i] if demand_values else None))
    return results


    
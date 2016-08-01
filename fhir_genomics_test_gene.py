from create_test_case import *
import csv
import json

def trans_csv_to_dict(csv_file):
    headers = []
    detail_dict = {}
    for index, row in enumerate(csv_file):
        if index == 0:
            headers = row
        else:
            element = row[0]
            detail_dict[element] = {}
            for subindex in range(1, len(headers)):
                detail_dict[element][headers[subindex]] = row[subindex]
    return detail_dict

def create_element_test_cases(detail_dict):
    test_cases = {}
    for element in detail_dict:
        non_prefix_element = remove_prefix(element)
        element_type = detail_dict[element]['Type']
        control = control_analyze(detail_dict[element]['Control'])
        binding_str = detail_dict[element]['Binding_Value']
        binding = None if len(binding_str) == 0 else json.loads(binding_str)
        if element_type.lower() == 'extension' or element_type.lower() == 'resource' or element_type.lower() == 'identifier':
            continue
        if element_type.lower() == 'backboneelement':
            test_cases[non_prefix_element] = 'backbone'
        else:
            if 'reference' in element_type.lower():
                binding = {'reference_type':detail_dict[element]['Reference']}
                element_type = 'reference'
            test_cases[non_prefix_element] = create_all_cases_for_type(element_type, control, binding)
    return test_cases

def combine_all_lists(lists):
    total = reduce(lambda x, y: x*y, map(len, [lists[key] for key in lists]))
    res_list = []
    for i in range(total):
        step = total
        tempItem = {}
        for key in lists:
            l = lists[key]
            step /= len(l)
            tempItem[key] = l[i/step % len(l)]
        res_list.append(tempItem)
    return res_list

def create_all_test_cases(element_test_cases):
    #generate all right test cases
    element_right_cases = {}
    element_name_lists = []
    for element in element_test_cases:
        element_name_lists.append(element)
        if element_test_cases[element] == 'backbone' or len(element_test_cases[element]['right']) == 0:
            continue
        element_right_cases[element] = element_test_cases[element]['right']
    right_cases = combine_all_lists(element_right_cases)
    #generate all wrong test cases
    element_wrong_cases = {}
    for element in element_test_cases:
        if element_test_cases[element] == 'backbone' or len(element_test_cases[element]['wrong']) == 0:
            continue
        element_wrong_cases[element] = element_test_cases[element]['wrong']
    wrong_cases = []
    for key in element_wrong_cases:
        cases = element_wrong_cases[key]
        for case in cases:
            wrong_case = {}
            wrong_case[key] = case
            for subkey in element_name_lists:
                if subkey == key:
                    continue
                if subkey not in element_right_cases:
                    continue
                wrong_case[subkey] = element_right_cases[subkey]
            wrong_cases.append(wrong_case)
    all_cases = right_cases + wrong_cases
    total_cases = len(all_cases)
    print total_cases


    

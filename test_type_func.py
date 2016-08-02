'''
test code
@author: Bowen
'''

import csv
from create_test_case import *
from fhir_genomics_test_gene import *

possibles = globals().copy()
possibles.update(locals())

if __name__ == '__main__':
    # file_list = ['DiagnosticReport.csv', 'DiagnosticRequest.csv', 'Observation.csv', 'Sequence.csv', 'FamilyMemberHistory.csv']
    # types = []
    # for filename in file_list:
    #     csv_reader = csv.reader(open('../%s' %filename, 'r'))
    #     for index, row in enumerate(csv_reader):
    #         if index == 0:
    #             continue
    #         if row[2].lower() not in types:
    #             types.append(row[2].lower())
    # print types
    # non_function_types = ['resource','extension', 'id', 'identifier', 'backboneelement','meta','see observation.referencerange']
    #print create_reference()
    #print create_all_cases_for_type('codeableconcept', 3, {'code':'123123', 'system':'http://lonic.org'})
    csv_reader = csv.reader(open('../Observation.csv', 'r'))
    detail_dict = trans_csv_to_dict(csv_reader)
    test_cases = create_element_test_cases(detail_dict)
    create_orthogonal_test_cases(test_cases)


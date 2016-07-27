import csv
import json
import random
import string
from datetime import datetime, date

def random_string_generate(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

def create_reference(reference_type):
    reference_str = "%s/%s" % (reference_type, random_string_generate(5))
    return {'reference':reference_str}

def random_picker(pick_list):
    low, high = 0, len(pick_list)
    return pick_list[random.randint(low, high)]

def create_string(suggested="", length=5):
    if len(suggested) != 0:
        return suggested
    else:
        return random_string_generate(length)

def create_uri(suggested=""):
    if len(suggested) != 0:
        return suggested
    else:
        uri = 'http://%s.com' % random_string_generate(5)
        return uri

def create_codeableconcept(code=None, system=None):
    concept_dict = {
          "code": {
            "coding": [
              {
                "system": system if system else create_uri(),
                "code": code if code else random_string_generate(5)
              }
            ],
          }
        }
    return concept_dict

def create_quantity(customed_value=None, unit='oz'):

    return {
        'value':customed_value if customed_value else create_decimal(),
        'comparator':'<=',
        'unit':unit,
        'system':''
    }

def create_simplequantity():
    return create_quantity()

def create_integer(customed=None):
    if customed == None:
        return random.randint(1,10)
    else:
        return customed

def create_code(code="",customed='code'):
    if len(code) != 0:
        return {customed:code}
    else:
        return {customed:random_string_generate(5)}

def create_attachment(data=None,content_type="application/pdf", language="en"):
    return {
        'contentType':content_type,
        'language':language,
        'date':data,
        'title':random_string_generate(6)
    }

def create_instant():
    return create_datetime()

def create_decimal(customed=None):
    if customed: 
        return customed
    else:
        return random.uniform(0,10)


def create_annotation():
    return {
        'author': create_reference('Patient'),
        'time':create_datetime(),
        'text':random_string_generate(15)
    }

def create_age(age_value=None):
    return create_quantity(age_value if age_value else random.randint(1,20), 'year')

def create_boolean():
    return random_picker([True, False])

def create_date():
    return date.today().isoformat()

def create_datetime():
    time_isoStr = datetime.now().isoformat(' ')
    return time_isoStr

def create_narrative():
    return {
        'status': random_picker(['generated', 'extensions', 'additional', 'empty']),
        'div':'<p>%s</p>' % random_string_generate(20)
    }

def create_range(low=1.0, high=2.0):
    return {
        "low": create_quantity(low),
        "high": create_quantity(high)
    }

def create_by_type(element_type):
    

def trans_csv_to_dict(desc_csv_file):
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

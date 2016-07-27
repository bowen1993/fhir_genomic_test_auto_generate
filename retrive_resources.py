from bs4 import BeautifulSoup
import requests
import csv

baseUrl = 'http://hl7-fhir.github.io/'

url_dict = {
    'Sequence': 'http://genomics-advisor.smartplatforms.org:4000/consensus-sequence-block-definitions.html',
    'Observation' : 'http://genomics-advisor.smartplatforms.org:4000/observation-definitions.html',
    'FamilyMemberHistory':'http://genomics-advisor.smartplatforms.org:4000/familymemberhistory-genetic-definitions.html',
    'DiagnosticReport':'http://genomics-advisor.smartplatforms.org:4000/reportforgenetics-definitions.html',
    'DiagnosticOrder':'http://genomics-advisor.smartplatforms.org:4000/orderforgenetics-definitions.html'
}

def get_html_doc(url):
    response = requests.get(url);
    return response.text

def analyse_html(html_str):
    soup = BeautifulSoup(html_str, "html.parser")
    detail_table = soup.find('table');
    trs = detail_table.findAll('tr')
    res_dict = {}
    curr_element = ''
    for tr in trs:
        td_objs = tr.td
        if td_objs.has_attr('class') and 'structure' in td_objs['class']:
            curr_element = td_objs.text
            res_dict[curr_element] = {}
        elif len(curr_element) != 0:
            if 'Control' in td_objs.text:
                res_dict[curr_element]['Control'] = td_objs.next_sibling.text
            elif 'Type' in td_objs.text:
                res_dict[curr_element]['Type'] = td_objs.next_sibling.text
            elif 'Binding' in td_objs.text:
                res_dict[curr_element]['Binding'] = td_objs.next_sibling.text
                res_dict[curr_element]['Binding_Url'] = baseUrl + td_objs.next_sibling.a['href']
    new_res_dict = extract_reference(res_dict)
    return new_res_dict

def extract_reference(res_dict):
    for key in res_dict:
        if 'Type' not in res_dict[key]:
            continue
        if 'Reference' in res_dict[key]['Type']:
            index = res_dict[key]['Type'].find('(')
            res_dict[key]['Reference'] = res_dict[key]['Type'][index+1:-1]
    return res_dict

def write_res_to_csv(name, res_dict):
    csv_writer = csv.writer(open('%s.csv' % name, 'w'))
    head = ['Element', 'Type' ,'Control', 'Binding', 'Reference', 'Binding_Url']
    csv_writer.writerow(['Element', 'Type' ,'Control', 'Binding', 'Reference', 'Binding_Url'])
    for key in res_dict:
        if 'Type' not in res_dict[key]:
            continue
        new_row = [key, res_dict[key]['Type']]
        for item in head:
            if item == 'Element' or item == 'Type':
                continue
            new_row.append('' if item not in res_dict[key] else res_dict[key][item])
        print new_row
        csv_writer.writerow(new_row)
    del csv_writer

def mainFunc():
    for key in url_dict:
        info_dict = analyse_html(get_html_doc(url_dict[key]))
        write_res_to_csv(key, info_dict)



if __name__ == '__main__':
    info_dict = analyse_html(get_html_doc('http://hl7-fhir.github.io/orderforgenetics-definitions.html'))
    write_res_to_csv('DiagnosticRequest', info_dict)
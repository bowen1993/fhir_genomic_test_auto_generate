import json

def json2xml_(json_obj, line_padding=""):
    result_list = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json2xml_(sub_elem, line_padding))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml_(sub_obj, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))

        return "\n".join(result_list)

    return "%s%s" % (line_padding, json_obj)

def json2xml(json_obj, curr_tag=""):
    curr_str = ''
    json_obj_type = type(json_obj)
    if json_obj_type is list:
        for sub_ele in json_obj:
            curr_str += '\n' + json2xml(sub_ele)
    elif json_obj_type is dict:
        for tag_name in json_obj:
            child_obj = json_obj[tag_name]
            child_obj_type = type(child_obj)
            if child_obj_type is not dict and child_obj_type is not list:
                curr_str += '\n<%s value="%s" />' % (tag_name, child_obj)
            else:
                curr_str += '\n<%s>' % tag_name
                curr_str += '\n' + json2xml(child_obj, tag_name)
                curr_str += '\n</%s>' % tag_name
    return curr_str

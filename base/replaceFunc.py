import sys

from base.radarDetector import *

sys.path.append(r"..")

import re
import ast
from base.parser import parse_string_value
from func_maker.functions import *

fake = Faker("zh-cn")


# function_regexp = re.compile(r"""\$\{(\w+)\(([\$\{\}\w=,\.^$\(\)]*)\)\}""")


def is_functon(content):
    matched = find_all_function(content)

    return True if matched else False


def parse_function(content):
    # backups = content

    matched = find_all_function(content)

    # print(matched)

    len_func = len(matched) if matched is not None else 0
    func_list = []
    for i in range(len_func):

        function_meta = dict(args=[], kwargs={})

        function_meta["func_name"] = matched[i][0]

        args_str = matched[i][1].strip()

        args_list = find_all_params(args_str)

        for arg in args_list:
            func_str_start_index = get_index(func_start, arg)
            equal_str_start_index = get_index('=', arg)
            if equal_str_start_index < 0 or (0 <= func_str_start_index < equal_str_start_index):
                value = run(arg, 1)[0]
                function_meta["args"].append(value)
            else:
                key = arg[0:equal_str_start_index]
                value = run(arg[equal_str_start_index + 1:len(arg)], 1)[0]
                # key, value = arg.split('=')
                parsed_value = run(value, 1)[0]
                function_meta["kwargs"][key] = parse_string_value(parsed_value)
                # print(function_meta["kwargs"][key])
                # func_list.append(function_meta)
        func_list.append(function_meta)

    return func_list


def func_run(xxx=[]):
    all_result = []

    # print(xxx)
    for i in xxx:

        # print(i)
        try:
            res = getattr(fake, i["func_name"])(*i["args"], **i["kwargs"])
        except Exception as ex:
            res = eval(i["func_name"])(*i["args"], **i["kwargs"])

        all_result.append(res)

    return all_result


def replace(content, all_result):
    finally_res = content
    func_list = find_all_function(content)
    len_func = len(func_list) if func_list is not None else 0
    if len(all_result) == len_func:
        for i in range(len_func):
            finally_res = finally_res.replace(func_list[i][2], str(all_result[i]), 1)
    return finally_res


def run_same_data(content, numb):
    res = []
    content = f"""{content}"""
    func_list = parse_function(content)
    for i in range(numb):
        res.append(replace(content, func_run(func_list)))
    return res


def run(content, numb):
    res = []
    for i in range(numb):
        content = f"""{content}"""
        func_list = parse_function(content)
        res.append(replace(content, func_run(func_list)))
    return res


def replace_all_dic_ref_with_max_times(str_val, circular_reference_parse_max_times=1, ref_dic={}):
    if circular_reference_parse_max_times == 1:
        return replace_all_dic_ref(str_val, ref_dic)
    for i in range(1,circular_reference_parse_max_times+1):
        start_index = get_index(ref_start, str_val)
        if start_index <= -1:
            return str_val
        str_val = replace_all_dic_ref(str_val, ref_dic)
    return str_val


def replace_all_dic_ref(str_val, ref_dic={}):
    ref_val_mapping_dic = {}
    if ref_dic is None or len(ref_dic) == 0:
        return str_val
    start_index = get_index(ref_start, str_val)
    while -1 < start_index < len(str_val):
        start = start_index
        flag = 0
        is_head = 0
        for i in range(start, len(str_val)):
            char = str_val[i]
            if char == '{':
                flag += 1
                is_head += 1
            if char == '}':
                flag -= 1
            if flag == 0 and is_head > 0:
                ref_dic_str = str_val[start: i + 1]
                start_index = get_index(ref_start, str_val, start_index + 1)
                ref_name = ref_dic_str[ref_dic_str.index("{") + 1:ref_dic_str.rindex("}")]
                ref_execute_val = run(ref_dic[ref_name], 1)[0]
                ref_dic[ref_name] = ref_execute_val
                if ref_execute_val is not None:
                    ref_val_mapping_dic[ref_dic_str] = ref_execute_val
                break
            if i == len(str_val) - 1:
                start_index = len(str_val)
        if flag != 0:
            raise Exception('Parentheses do not match')
    for key in ref_val_mapping_dic:
        str_val = str_val.replace(key, ref_val_mapping_dic[key])
    return str_val

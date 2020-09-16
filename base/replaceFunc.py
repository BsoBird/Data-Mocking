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
                value = run(arg[equal_str_start_index + 1:len(arg)],1)[0]
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
                if ref_execute_val is not None:
                    ref_val_mapping_dic[ref_dic_str] = ref_execute_val
                break
            if i == len(str_val)-1:
                start_index = len(str_val)
        if flag != 0:
            raise Exception('Parentheses do not match')
    for key in ref_val_mapping_dic:
        str_val = str_val.replace(key, ref_val_mapping_dic[key])
    return str_val


if __name__ == '__main__':
    # str_val = "t1=======$FUNC{t2(a=1)}"
    str_val = "$FUNC{date_between(start_date='-5y', end_date='today')}"
    func_start_index = get_index(func_start, str_val)
    equal_start_index = get_index('=', str_val)
    if equal_start_index < 0 or func_start_index < equal_start_index:
        print(str_val)
    else:
        print(str_val[0:equal_start_index])
        print(str_val[equal_start_index + 1:len(str_val)])
    # print(quote_replacement('$test'))
    # dic_test={}
    # str_val_1 = "'n1'"
    # dic_test['t1']=str_val_1
    # print(f"""{dic_test}""")
    # print(quote_escaped("['工具直接为了游戏帮助生活你的.', '部分到了不要出现.', '帮助计划北京生产经济.']"))
    # template = "$REF{msg_id},$REF{event_date},$REF{process_time},$REF{data_type},$FUNC{concat('TAOBAO|',$REF{trade_id},'|',$REF{shop_tag})},$FUNC{concat($REF{event_date},' 13:50:27')},$FUNC{concat('TAOBAO|',$REF{trade_id},'|',$REF{shop_tag},'|',$REF{event_date})},$REF{table_id},$REF{rw},,$REF{tenant},$REF{shop_tag},$REF{group_id}"
    # template = "$REF{msg_id},$REF{event_date},$REF{process_time},$REF{data_type},$FUNC{concat('TAOBAO|',$REF{trade_id},'|',$REF{shop_tag})},$FUNC{concat($REF{event_date},' 13:50:27')},$FUNC{concat('TAOBAO|',$REF{trade_id},'|',$REF{shop_tag},'|',$REF{event_date})},$REF{table_id},$REF{rw},,$REF{tenant},$REF{shop_tag},$REF{group_id}"
    # template = "$FUNC{concat(\'TAOBAO|\',676124699114,\'|\',51456122,\'|\',2017-11-10)}"\
    # template = "$FUNC{concat(TAOBAO|,$REF{trade_id},|,$REF{shop_tag})},'13:50:27',$FUNC{concat(TAOBAO|,$REF{trade_id},|,$REF{shop_tag},|,$REF{event_date})}"
    template="$FUNC{date_between(start_date=-5d, end_date=today)}"
    dic = {
        "msgId":"$FUNC{md5()}",
        "serviceCode":"$FUNC{random_enum(TEST01,TEST02,TEST03)}",
        "eventDate":"$FUNC{random_enum(2020-07-07,2020-07-06,2020-07-05)}",
        "processTime":"$FUNC{date_between(start_date=-5d, end_date=today)}",
        "dataType":"standard_trade",
        "tradeId":"$FUNC{credit_card_number()}",
        "shopTag":"$FUNC{ean8()}",
        "tableId":"$FUNC{range_id(start=0,end=1000)}",
        "modify":"$FUNC{random_enum(2020-07-07 13:56:21,2020-07-06 13:56:21,2020-07-05 13:56:21)}",
        "type":"$FUNC{range_id(start=0,end=1)}",
        "parentId":"null",
        "parentModify":"null",
        "tenant":"$FUNC{concat(TENANT,$FUNC{range_id(start=0,end=10)})}",
        "groupId":"$FUNC{random_enum(21836,21774,20720,21284,21818,21592,21282,21000)}"
    }
    print({"result": run(template,1)})
    # print(concat())
    # str_json = "{p1=$FUNC{t2(a=1)}}"
    # func_str_2 = "$REF{p}$FUNC{concat($FUNC{name($REF{p})},s,f,ffffssda)}#$REF{p}$FUNC{funcc(123,a=123,b=222)}asda$REF{p}sda$FUNC{age()}$FUNC{name()}"
    # p2f = eval(str_json)
    # p2f = ast.literal_eval(f"""{str_json}""")
    # print(p2f)
    # print(p2f['p1'])
    # print(replace_all_dic_ref(func_str_2, {"pp": "ad"}))
    # for i in range(1):
    #     test = "$FUNC{concat($FUNC{name()},s,f,ffffssda)}#$FUNC{funcc(123,a=123,b=222)}asdasda$FUNC{age()}$FUNC{name()}"
    #     print(run(replace_all_dic_ref(func_str_2, {"p": "ad"}), 10))

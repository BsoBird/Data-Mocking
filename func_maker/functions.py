from faker import Faker
from random import randint
import re
import time
import sys

from base.parser import parse_string_value

fake = Faker("zh-cn")


def company(arg=None):
    return arg if arg else fake.company()


def age(arg=None):
    return arg if arg else randint(15, 60)


def name(arg=None):
    return arg if arg else fake.name()


def range_id(start=None, end=None):
    if start is None and end is None:
        return Id()
    else:
        if start is None:
            start = 0
        if end is None:
            end = sys.maxsize
    return randint(start, end)


def random_enum(*args):
    return '' if args is None or len(args) == 0 else args[randint(0, len(args) - 1)]


def Id(arg=None):
    return arg if arg else randint(111111111111111111, 911111111111111111)

def concat_list_ws(tag, args=[]):
    new_list = []
    for unit in args:
        new_list.append(unit)
        new_list.append(tag)
    new_list.pop()
    return concat(*new_list)

def concat_ws(tag, *args):
    new_list = []
    for unit in args:
        new_list.append(unit)
        new_list.append(tag)
    new_list.pop()
    return concat(*new_list)


def concat(*args):
    str_list = []
    for i in args:
        str_list.append(str(i).replace("'", ""))
    return ''.join(str_list)


def funcc(x, a=12, b=12313):
    return x + str(a) + str(b)


def quote_escaped(str_val):
    if str_val is None:
        return None
    return re.sub(r'(?<!\\)"', '\\"', re.sub(r"(?<!\\)'", "\\'", str_val))


def quote_replacement(str_val=None):
    from base.radarDetector import get_index
    if (str_val is None) or (get_index('\\', str_val) == -1 and get_index('$', str_val) == -1):
        return str_val
    str_buffer = []
    for i in range(len(str_val)):
        c = str_val[i]
        if c == '\\' or c == '$':
            str_buffer.append('\\')
        str_buffer.append(c)
    return concat(*str_buffer)


def eval_str(value):
    return parse_string_value(value)


def timeNow(arg=None):
    return arg if arg else time.strftime("%H:%M:%S", time.localtime())


def dateNow(arg=None):
    return arg if arg else time.strftime("%Y-%m-%d", time.localtime())


def dateTimeNow(arg=None):
    return arg if arg else time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def mock_default(params="", times=-1,separator=""):
    import json
    from base.replaceFunc import replace_all_dic_ref_with_max_times, run
    if params == "":
        return None
    params = params.replace("$FUNC_PRE{","$FUNC{")
    params = params.replace("$REF_PRE{","$REF{")
    params_dic = json.loads(params)
    times = int(times)
    numb = int(params_dic.setdefault('numb', -1))
    if times == -1 and numb > 0:
        times = int(params_dic['numb'])
    return concat_list_ws(separator,run(
        replace_all_dic_ref_with_max_times(params_dic.setdefault('content',''), params_dic.setdefault('circular_reference_parse_max_times',1),
                                           params_dic.setdefault('function_dic','')),
        times))


def mock_all_single(params="", times=-1,separator=""):
    import json
    import copy
    from base.replaceFunc import replace_all_dic_ref_with_max_times, run
    if params == "":
        return None
    params = params.replace("$FUNC_PRE{","$FUNC{")
    params = params.replace("$REF_PRE{","$REF{")
    params_dic = json.loads(params)
    times = int(times)
    numb = int(params_dic.setdefault('numb', -1))
    if times == -1 and numb > 0:
        times = int(params_dic['numb'])
    result = []
    for i in range(1, times + 1):
        content = copy.deepcopy(params_dic.setdefault('content',''))
        unit = run(
            replace_all_dic_ref_with_max_times(content, params_dic.setdefault('circular_reference_parse_max_times',1),
                                               params_dic.setdefault('function_dic','')),
            times)
        result.append(unit[0])
    return concat_list_ws(separator,result)

func_start = "$FUNC{"
ref_start = "$REF{"


def find_all_function(str_val):
    tuple_list = []
    while get_index(func_start, str_val) != -1:
        start_index = get_index(func_start, str_val)
        flag = 0
        is_head = 0
        for i in range(start_index, len(str_val)):
            char = str_val[i]
            if char == '{':
                flag += 1
                is_head += 1
            if char == '}':
                flag -= 1
            if flag == 0 and is_head > 0:
                func_def_str = str_val[start_index: i + 1] if str_val[start_index] == '$' else str_val[start_index + 1: i + 1]
                func_name = func_def_str[func_def_str.index("{") + 1:func_def_str.index("(")]
                func_param_list_str = func_def_str[func_def_str.index("(") + 1:func_def_str.rindex(")")]
                tuple_list.append((func_name, func_param_list_str, func_def_str))
                str_val = str_val[i + 1:len(str_val)]
                break
        if flag != 0:
            raise Exception('Parentheses do not match')
    return tuple_list


def find_all_params(str_val: str):
    list_param = []
    if str_val == '':
        return list_param
    if str_val[len(str_val) - 1] != ',':
        str_val = str_val + ","
    start = 0
    flag = 0
    for i in range(len(str_val)):
        char = str_val[i]
        if char == '{' or char == '(':
            flag += 1
        if char == '}' or char == ')':
            flag -= 1
        if (char == ',' and flag == 0) or i == len(str_val) - 1:
            list_param.append(str_val[start:i].strip())
            start = i + 1
    if flag != 0:
        raise Exception('Parentheses do not match')
    return list_param


def get_index(substr, original_str, begin=0):
    try:
        return original_str.index(substr, begin)
    except ValueError:
        return -1


if __name__ == '__main__':
    # func_str_1 = "$FUNC{concat(s,s,f,ffffssda)}"
    # print(func_str_1[func_str_1.index("{") + 1:func_str_1.index("(")])
    # print(func_str_1[func_str_1.index("(") + 1:func_str_1.rindex(")")])
    # print(find_all_params("${t1(${t2(1)})}"))
    print(find_all_function(
        "$FUNC{concat(TAOBAO|,$REF{trade_id},|,$REF{shop_tag})},'13:50:27',$FUNC{concat(TAOBAO|,$REF{trade_id},|,$REF{shop_tag},|,$REF{event_date})}"))

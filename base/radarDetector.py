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
    add_separator:bool = False
    if str_val == '':
        return list_param
    if str_val[len(str_val) - 1] != ',':
        str_val = str_val + ","
        add_separator = True
    start = 0
    flag = 0
    for i in range(len(str_val)):
        previous_char = ""
        char = str_val[i]
        if i > 0:
            previous_char = str_val[i-1]
        if char == '{' or char == '(':
            flag += 1
        if char == '}' or char == ')':
            flag -= 1
        if (char == ',' and flag == 0 and previous_char!='\\') or i == len(str_val) - 1:
            if i < len(str_val) - 1:
                value = str_val[start:i].strip()
            else:
                value = str_val[start:i+1].strip()
            if value == '\\,':
                value = ','
            list_param.append(value)
            start = i + 1
    if flag != 0:
        raise Exception('Parentheses do not match')
    if add_separator:
        t = len(list_param)
        final_param = list_param[t-1]
        final_param = final_param[0:-1]
        list_param[t-1] = final_param
    return list_param


def get_index(substr, original_str, begin=0):
    try:
        return original_str.index(substr, begin)
    except ValueError:
        return -1
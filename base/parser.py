import ast
import re

invalid_escape = re.compile(r'\\[0-7]{1,3}')  # up to 3 digits for byte values up to FF

def replace_with_byte(match):
	return chr(int(match.group(0)[1:], 8))

def repair(brokenjson):
	return invalid_escape.sub(replace_with_byte, brokenjson)


def parse_string_value(str_value):
	""" parse string to number if possible
	e.g. "123" => 123
		 "12.2" => 12.3
		 "abc" => "abc"
		 "$var" => "$var"
	"""
	try:

		return ast.literal_eval(str_value)
	except ValueError:

		return str_value
	except SyntaxError:
		# e.g. $var, ${func}
		return str_value


if __name__ == '__main__':
	a = '1234+1234'
	print(parse_string_value(a))
	b = "{\"content\": \"\x01\",\"numb\": 10}"
	print(repair(b))

import ast



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

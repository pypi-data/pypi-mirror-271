"""
https://www.mclean.net.nz/cpan/couponcode/
Coupon Codes from https://github.com/grantm/Algorithm-CouponCode?tab=readme-ov-file

# quick runs:
python3 -c "import cccodes.coupon as c; print(c.generate())"

python3 -c "import cccodes.coupon as c; print(c.validate('T13P-2LMP-E0B5'))"

"""

import secrets
import string

from .badwords import bad_words

symbols = '0123456789ABCDEFGHJKLMNPQRTUVWXY'
num_parts = 3
part_length = 5


def generate_random_plaintext(length=8):
	alphabet = string.ascii_letters + string.digits
	alphabet = symbols
	return ''.join(secrets.choice(alphabet) for i in range(length))

def normalize(code):
	"""
	Normalize the input, fixing any typos we can automatically.
	"""
	code = code.upper()
	code = code.replace('O', '0')
	code = code.replace('I', '1')
	code = code.replace('Z', '2')
	code = code.replace('S', '5')
	return code
def check_digit_alg1(part_number, part_value):
	"""
	check digit algorithm

	For a given part #(a digit 0-3 normally)
	add 1 to make it 1-indexed, not 0 indexed.
	Then for the values in the part
	iterate through each character
	Get the index of where it is in the symbols

	Take the part_number * 19 + the index
	Store that and for subsequent runs replace part_number
	with the last computed result.
	"""
	# print(f"check: part_number:{part_number+1} part_value={part_value}")
	result = part_number + 1
	for i in range(len(part_value)):
		c = part_value[i]
		idx = symbols.index(c)
		result = result * 19 + idx
		# print(f"check: char:{c} index:{idx} result:{result}")
	# print(f"check_result:{result}")
	r = result % (len(symbols) - 1)
	s = symbols[r]
	# print(f"check_digit:{r} symbol:{s}")
	return s


def generate():
	parts = []
	for i in range(num_parts):
		# print(f"i:{i}")
		part = generate_random_plaintext(part_length - 1)
		# print(f"part_before_check:{part}")
		part += check_digit_alg1(i, part)
		# print(f"part_after_check:{part}")
		if part in bad_words:
			i = i - 1
		else:
			parts.append(part)
	return '-'.join(parts)


def validate(code):
	"""validate"""
	code = normalize(code)
	parts = code.split('-')

	for i in range(len(parts)):
		part = parts[i]
		check = part[-1]
		computed = check_digit_alg1(i, part[:-1])
		# print(f"part:{i} check:{check} computed:{computed}")
		if check != computed:
			return False
	return True

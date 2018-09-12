from roman_numeral_to_integer import separated_numbers_to_int


def create_test_data():
    numerals_dict = dict()
    with open('numerals.txt', 'r') as infile:
        for line in infile.read().splitlines():
            k, v = line.split(': ')
            numerals_dict[k] = v
    return numerals_dict


def test_numbers():
    numerals_and_integers = create_test_data()
    for k, v in numerals_and_integers.items():
        integer = separated_numbers_to_int(v)
        assert integer == int(k)


test_numbers()

# Convert a roman numeral into an integer


def convert_roman_numeral_into_separated_numbers(roman):
    numerals_and_values = {
        "M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1
    }
    numbers = []
    for x in list(roman):
        number = numerals_and_values[x]
        numbers.append(number)
    return numbers


def separated_numbers_to_int(roman):
    numbers = convert_roman_numeral_into_separated_numbers(roman)
    total = 0
    for counter, x in enumerate(numbers):
        try:
            if x < numbers[counter + 1]:
                total -= x
            else:
                total += x
        except IndexError:
            total += x
    print(total)
    return total


integer = separated_numbers_to_int('MCMLXXIV')

# A Python class to convert a roman numeral into an integer

class PyConverter:
    def convert_roman_numeral_into_separated_numbers(self, roman):
        numerals_and_values = {
            "M": 1000, "D": 500, "C": 100, "L": 50, "X": 10, "V": 5, "I": 1
        }
        numbers = []
        for x in list(roman):
            number = numerals_and_values[x]
            numbers.append(number)
        return numbers

    def roman_to_int(self, roman):
        numbers = self.convert_roman_numeral_into_separated_numbers(roman)
        biggest_n = max(numbers)
        biggest_n_positions = [
            i for i, x in enumerate(numbers) if x == biggest_n
        ]
        integer = 0
        for x in numbers:
            if x < biggest_n:
                x_position = numbers.index(x)
                if x_position < biggest_n_positions[-1]:
                    integer -= x
                else:
                    integer += x
            else:
                integer += x
        return integer

print(PyConverter().roman_to_int('CMMM'))


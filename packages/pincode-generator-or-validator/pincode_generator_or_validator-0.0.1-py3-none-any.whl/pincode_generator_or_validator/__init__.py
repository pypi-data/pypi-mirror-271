import random

def validate(pin):
    string_pin = str(pin)
    length = len(string_pin)
    result = True

    if length != 6:
        result = False
    
    first_digit = string_pin[0]
    if not first_digit.isdigit() or int(first_digit) == 0:
        result = False

    for digit in string_pin[1:]:
        if not digit.isdigit():
            result = False

    if length == 6 and string_pin[3] != ' ':
        result = True
    elif length == 6 and string_pin[3] == ' ':
        if not (string_pin[:3].isdigit() and 1 <= int(string_pin[0]) <= 9):
            result = True

    if result:
        return "Valid PIN"
    else:
        return "Invalid PIN"


def generate():

    first_digit = random.randint(1, 9)
    remaining_five_digits = ''.join(str(random.randint(0, 9)) for _ in range(5))
    pin = str(first_digit) + remaining_five_digits
    return pin


import re

def read_equation():
    s = input("Enter equation: ")
    return s

def parse_equation(equation):
    pattern = r'(\w+)\s*([+\-*/])\s*(-?\d+)\s*=\s*(-?\d+)'
    match = re.match(pattern, equation)
    if match:
        variable = match.group(1)
        operator = match.group(2)
        number1 = int(match.group(3))
        number2 = int(match.group(4))
        return variable, operator, number1, number2
    else:
        raise ValueError()

def solve_equation(operator, number1, number2):
    x = 0
    match operator:
        case "+":
            x = number2 - number1
        case "-":
            x = number1 + number2
        case "*":
            x = number2 / number1
        case "/":
            x = number2 * number1
    return x

def solver():
    while (1):
        try:
            s = read_equation()
            if (s == "bye"):
                break
            variable, operator, number1, number2 = parse_equation(s)
            x = solve_equation(operator, number1, number2)
            print(variable + " = " + str(x))
        except:
            print("Invalid equation ... try again!")
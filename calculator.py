import operator
import re


class RPNAPIError(Exception):
    pass


class InvalidTokenError(RPNAPIError):
    pass


class MismatchedParenthesesError(RPNAPIError):
    pass


class RPNSyntaxError(RPNAPIError):
    pass


class RPNCalculator:

    OPERATORS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
    }

    PRIORITY = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
    }

    def __init__(self):
        self._functions = {
            'sin': lambda x: self.evaluate(f'0 {x} - sin'),
            'cos': lambda x: self.evaluate(f'0 {x} - cos'),
        }

    def _tokenize(self, expression: str) -> list:
        tokens = re.findall(r'\d+\.?\d*|[()+*\/-]|\w+', expression)
        return tokens

    def _validate_tokens(self, tokens: list) -> None:
        for token in tokens:
            if not (token.replace('.', '').isdigit() or
                    token in self.OPERATORS or
                    token in '()'):
                raise InvalidTokenError(f'Недопустимый токен: {token}')

    def _check_parentheses(self, tokens: list) -> None:
        stack = []
        for token in tokens:
            if token == '(':
                stack.append(token)
            elif token == ')':
                if not stack:
                    raise MismatchedParenthesesError(
                        "Несбалансированные скобки")
                stack.pop()
        if stack:
            raise MismatchedParenthesesError("Несбалансированные скобки")

    def infix_to_rpn(self, expression: str) -> list:
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        self._check_parentheses(tokens)

        output = []
        operators = []

        for token in tokens:
            if token.replace('.', '').isdigit():
                output.append(token)
            elif token in self.OPERATORS:
                while (operators and operators[-1] != '(' and
                       self.PRIORITY[operators[-1]] >= self.PRIORITY[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()

        while operators:
            output.append(operators.pop())

        return output

    def evaluate_rpn(self, rpn: list) -> float:
        stack = []

        for token in rpn:
            if token.replace('.', '').isdigit():
                stack.append(float(token))
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise RPNSyntaxError(
                        "Недостаточно операндов для оператора")
                b = stack.pop()
                a = stack.pop()
                try:
                    result = self.OPERATORS[token](a, b)
                except ZeroDivisionError:
                    raise RPNSyntaxError("Деление на ноль")
                stack.append(result)
            else:
                raise InvalidTokenError(f'Недопустимый токен в ОПН: {token}')

        if len(stack) != 1:
            raise RPNSyntaxError("Некорректное выражение")

        return stack[0]

    def evaluate(self, expression: str) -> float:
        rpn = self.infix_to_rpn(expression)
        return self.evaluate_rpn(rpn)


if __name__ == '__main__':
    calc = RPNCalculator()
    print("Калькулятор ОПН. Введите 'quit' для выхода.")

    while True:
        try:
            expr = input("Введите выражение: ").strip()
            if expr.lower() == 'quit':
                break
            if not expr:
                continue

            rpn = calc.infix_to_rpn(expr)
            result = calc.evaluate_rpn(rpn)
            print(f"ОПН: {' '.join(map(str, rpn))}")
            print(f"Результат: {result}")
        except RPNAPIError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")

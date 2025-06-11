"""Module providing a Reverse Polish Notation (RPN) calculator."""
import operator
import re


class RPNAPIError(Exception):
    """Base exception for RPN calculator errors."""


class InvalidTokenError(RPNAPIError):
    """Raised when an invalid token is encountered in the expression."""


class MismatchedParenthesesError(RPNAPIError):
    """Raised when parentheses are mismatched in the expression."""


class RPNSyntaxError(RPNAPIError):
    """Raised for general syntax errors in RPN evaluation."""


class RPNCalculator:
    """Reverse Polish Notation (RPN) Calculator supporting +, -, *, /."""

    OPERATORS = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }

    PRIORITY = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
    }

    def __init__(self):
        pass

    def _tokenize(self, expression: str) -> list:
        """Tokenize the input expression into numbers, operators, and parentheses."""
        tokens = re.findall(r"\d+\.?\d*|[()+\-*/]", expression)
        return tokens

    def _validate_tokens(self, tokens: list) -> None:
        """Validate that all tokens are numbers, operators, or parentheses."""
        for token in tokens:
            if not (
                token.replace(".", "", 1).isdigit()
                or token in self.OPERATORS
                or token in ("(", ")")
            ):
                raise InvalidTokenError(f"Invalid token: {token}")

    def _check_parentheses(self, tokens: list) -> None:
        """Check for balanced parentheses in the token list."""
        stack = []
        for token in tokens:
            if token == "(":
                stack.append(token)
            elif token == ")":
                if not stack:
                    raise MismatchedParenthesesError("Mismatched parentheses")
                stack.pop()
        if stack:
            raise MismatchedParenthesesError("Mismatched parentheses")

    def infix_to_rpn(self, expression: str) -> list:
        """Convert infix expression to RPN (postfix) as a list of tokens."""
        tokens = self._tokenize(expression)
        self._validate_tokens(tokens)
        self._check_parentheses(tokens)

        output = []
        operators: list[str] = []

        for token in tokens:
            if token.replace(".", "", 1).isdigit():
                output.append(token)
            elif token in self.OPERATORS:
                while (
                    operators
                    and operators[-1] != "("
                    and self.PRIORITY[operators[-1]] >= self.PRIORITY[token]
                ):
                    output.append(operators.pop())
                operators.append(token)
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    output.append(operators.pop())
                if not operators:
                    raise MismatchedParenthesesError("Mismatched parentheses")
                operators.pop()

        while operators:
            if operators[-1] in ("(", ")"):
                raise MismatchedParenthesesError("Mismatched parentheses")
            output.append(operators.pop())

        return output

    def evaluate_rpn(self, tokens: list) -> float:
        """Evaluate an RPN (postfix) expression given as a list of tokens."""
        stack = []

        for token in tokens:
            if token.replace(".", "", 1).isdigit():
                stack.append(float(token))
            elif token in self.OPERATORS:
                if len(stack) < 2:
                    raise RPNSyntaxError("Not enough operands for operator")
                b = stack.pop()
                a = stack.pop()
                try:
                    res = self.OPERATORS[token](a, b)
                except ZeroDivisionError as exc:
                    raise RPNSyntaxError("Division by zero") from exc
                stack.append(res)
            else:
                raise InvalidTokenError(f"Invalid token in RPN: {token}")

        if len(stack) != 1:
            raise RPNSyntaxError("Malformed expression")

        return stack[0]

    def evaluate(self, expression: str) -> float:
        """Evaluate an infix expression and return the result."""
        rpn_tokens = self.infix_to_rpn(expression)
        return self.evaluate_rpn(rpn_tokens)


if __name__ == "__main__":
    calc = RPNCalculator()
    print("RPN Calculator. Type 'quit' to exit.")

    while True:
        try:
            expr = input("Enter expression: ").strip()
            if expr.lower() == "quit":
                break
            if not expr:
                continue

            rpn_token_list = calc.infix_to_rpn(expr)
            result_val = calc.evaluate_rpn(rpn_token_list)
            print(f"RPN: {' '.join(map(str, rpn_token_list))}")
            print(f"Result: {result_val}")
        except RPNAPIError as e:
            print(f"Error: {e}")

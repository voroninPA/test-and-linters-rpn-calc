import unittest
from calculator import RPNCalculator, RPNAPIError, InvalidTokenError, MismatchedParenthesesError, RPNSyntaxError


class TestRPNCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = RPNCalculator()

    def test_infix_to_rpn(self):
        test_cases = [
            ("3 + 4", ['3', '4', '+']),
            ("3 + 4 * 2", ['3', '4', '2', '*', '+']),
            ("(3 + 4) * 2", ['3', '4', '+', '2', '*']),
            ("3 + 4 * 2 / (1 - 5)", ['3', '4',
             '2', '*', '1', '5', '-', '/', '+']),
            ("2 + 3 * 4 - 5", ['2', '3', '4', '*', '+', '5', '-']),
            ("(1 + 2) * (3 + 4)", ['1', '2', '+', '3', '4', '+', '*']),
            ("10 - (2 + 3) * 4", ['10', '2', '3', '+', '4', '*', '-']),
            ("2.5 + 3.7 * 4", ['2.5', '3.7', '4', '*', '+']),
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                self.assertEqual(self.calc.infix_to_rpn(expr), expected)

    def test_evaluate_rpn(self):
        test_cases = [
            (['3', '4', '+'], 7),
            (['3', '4', '2', '*', '+'], 11),
            (['3', '4', '+', '2', '*'], 14),
            (['3', '4', '2', '*', '1', '5', '-', '/', '+'], 1),
        ]

        for rpn, expected in test_cases:
            with self.subTest(rpn=rpn):
                self.assertAlmostEqual(self.calc.evaluate_rpn(rpn), expected)

    def test_evaluate(self):
        test_cases = [
            ("3 + 4", 7),
            ("3 + 4 * 2", 11),
            ("(3 + 4) * 2", 14),
            ("3 + 4 * 2 / (1 - 5)", 1),
            ("10 / 2", 5),
            ("2.5 * 3", 7.5),
        ]

        for expr, expected in test_cases:
            with self.subTest(expr=expr):
                self.assertAlmostEqual(self.calc.evaluate(expr), expected)

    def test_invalid_tokens(self):
        with self.assertRaises(InvalidTokenError):
            self.calc.evaluate("3 + 4a")

    def test_mismatched_parentheses(self):
        with self.assertRaises(MismatchedParenthesesError):
            self.calc.evaluate("(3 + 4")
        with self.assertRaises(MismatchedParenthesesError):
            self.calc.evaluate("3 + 4)")

    def test_syntax_errors(self):
        with self.assertRaises(RPNSyntaxError):
            self.calc.evaluate("3 +")
        with self.assertRaises(RPNSyntaxError):
            self.calc.evaluate("+ 3")
        with self.assertRaises(RPNSyntaxError):
            self.calc.evaluate("3 3 +")

    def test_division_by_zero(self):
        with self.assertRaises(RPNSyntaxError):
            self.calc.evaluate("3 / 0")


if __name__ == '__main__':
    unittest.main()

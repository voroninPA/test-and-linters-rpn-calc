"""Unit tests for the RPNCalculator module."""
import unittest
from calculator import RPNCalculator, InvalidTokenError, MismatchedParenthesesError, RPNSyntaxError


class TestRPNCalculator(unittest.TestCase):
    """Unit tests for the RPNCalculator class."""

    def setUp(self):
        """Set up a new RPNCalculator instance for each test."""
        self.calc = RPNCalculator()

    def test_infix_to_rpn(self):
        """Test conversion from infix to RPN (postfix) notation."""
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
        """Test evaluation of RPN (postfix) expressions."""
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
        """Test evaluation of infix expressions."""
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
        """Test that invalid tokens raise InvalidTokenError."""
        with self.assertRaises(InvalidTokenError):
            self.calc.evaluate("3 + 4a")

    def test_mismatched_parentheses(self):
        """Test that mismatched parentheses raise MismatchedParenthesesError."""
        with self.assertRaises(MismatchedParenthesesError):
            self.calc.evaluate("(3 + 4")
        with self.assertRaises(MismatchedParenthesesError):
            self.calc.evaluate("3 + 4)")

    def test_syntax_errors(self):
        """Test that syntax errors raise RPNSyntaxError."""
        with self.assertRaises(RPNSyntaxError):
            self.calc.evaluate("3 +")
        with self.assertRaises(RPNSyntaxError):
            self.calc.evaluate("+ 3")
        with self.assertRaises(RPNSyntaxError):
            self.calc.evaluate("3 3 +")

    def test_division_by_zero(self):
        """Test that division by zero raises RPNSyntaxError."""
        with self.assertRaises(RPNSyntaxError):
            self.calc.evaluate("3 / 0")


if __name__ == '__main__':
    unittest.main()

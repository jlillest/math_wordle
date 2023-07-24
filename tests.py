import unittest

from wordle import WordleFormatError
from wordle import WordleMathError
from wordle import WordleGuess
from wordle import MathWordle


class TestWordleGuess(unittest.TestCase):
    def test_bad_equation_formats(self):
        guesses = [
            # bad length
            "1",
            # bad character
            "&1234567",
            # no equal sign
            "11234567",
            # too many equal signs
            "1=2=34+6",
            # does not start with number
            "+1234567",
            # starts with zero
            "0123=567",
            # expressions with multiple zeros
            "11-11=00",
            "11/01=11",
            "01*11=11",
            "11+01=11",
            "1+2*4=01",
            # does not end with number
            "1123456+",
            # contains no operations
            "1123=567",
            # adjacent operations
            "1+-34567",
            # operation on right side of equation
            "5+2=21/3",
        ]

        for guess in guesses:
            if guess != guesses[0]:
                self.assertEqual(len(guess), 8, f"guess length is too long: {guess}")
            with self.assertRaises(WordleFormatError, msg=f"guess did not raise: {guess}"):
                WordleGuess(guess)

    def test_bad_equation_math(self):
        guesses = [
            "12+34=77",
            "1*2*3=46"
        ]

        for guess in guesses:
            message = f"guess did not raise: {guess}"
            with self.assertRaises(WordleMathError, msg=message):
                WordleGuess(guess)


class TestMathWordle(unittest.TestCase):
    def test_wordle_guesses(self):
        guesses = [
            ("73-6_=1_", "5", "1", "73-61=12"),
            ("_*_3=1__", "5689", "24", "4*33=132"),
            ("_+___=1_", "24689-", "35", "5+3+7=15"),
        ]

        for guess, blacklist, whitelist, solution in guesses:
            mw = MathWordle(guess, blacklist, whitelist)
            self.assertIn(solution, mw.get_guesses())


if __name__ == '__main__':
    unittest.main()

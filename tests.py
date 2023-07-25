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
    def assert_wordle_solution(self, guess, blacklist, whitelist, solution):
        mw = MathWordle(guess, blacklist, whitelist)
        self.assertIn(solution, mw.get_guesses())

    def test_wordle_guess1(self):
        guess = "73-6_=1_"
        blacklist = "5"
        whitelist = "1"
        solution = "73-61=12"
        self.assert_wordle_solution(guess, blacklist, whitelist, solution)

    def test_wordle_guess2(self):
        guess = "_*_3=1__"
        blacklist = "5689"
        whitelist = "24"
        solution = "4*33=132"
        self.assert_wordle_solution(guess, blacklist, whitelist, solution)

    def test_wordle_guess3(self):
        guess = "_+___=1_"
        blacklist = "24689-"
        whitelist = "35"
        solution = "5+3+7=15"
        self.assert_wordle_solution(guess, blacklist, whitelist, solution)

    def test_exlusions1(self):
        guess = "[1]_+_1=34"
        exclusions = {0: "1"}
        bad_answer = "13+21=34"
        good_answer = "23+11=34"

        mw = MathWordle(guess)
        self.assertEqual(mw.exclusions, exclusions)
        guesses = mw.get_guesses()
        self.assertIn(good_answer, guesses)
        self.assertNotIn(bad_answer, guesses)

    def test_exlusions2(self):
        guess = "__+[2]1=34"
        exclusions = {3: "2"}
        bad_answer = "13+21=34"
        good_answer = "23+11=34"

        mw = MathWordle(guess)
        self.assertEqual(mw.exclusions, exclusions)
        guesses = mw.get_guesses()
        self.assertIn(good_answer, guesses)
        self.assertNotIn(bad_answer, guesses)

    def test_exlusions3(self):
        guess = "2[23]/[7][=][=]_0"
        exclusions = {1: "23", 3: "7", 4: "=", 5: "="}
        blacklist = "14568+"
        whitelist = "7"
        good_answer = "27/3-9=0"

        mw = MathWordle(guess, blacklist, whitelist)
        self.assertEqual(mw.exclusions, exclusions)
        guesses = mw.get_guesses()
        self.assertTrue(guesses)
        self.assertIn(good_answer, guesses)

    def test_exclusions_give_refined_results(self):
        guess_with = "2*8[26]=17[8]"
        guess_without = "2*8_=17_"
        blacklist = "345"
        whitelist = "6"
        good_answer = "2*88=176"

        mw_with = MathWordle(guess_with, blacklist, whitelist)
        self.assertTrue(mw_with.exclusions)
        guesses_with = mw_with.get_guesses()
        self.assertIn(good_answer, guesses_with)

        mw_without = MathWordle(guess_without, blacklist, whitelist)
        self.assertFalse(mw_without.exclusions)
        guesses_without = mw_without.get_guesses()
        self.assertIn(good_answer, guesses_without)

        self.assertGreater(len(guesses_without), len(guesses_with))


if __name__ == '__main__':
    unittest.main()

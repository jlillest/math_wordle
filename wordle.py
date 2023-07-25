import argparse
import re
from itertools import product

NUMBERS = "1234567890"
OPERATIONS = "+-*/"
EQUAL_SIGN = "="
VALID_CHARACTERS = NUMBERS + OPERATIONS + EQUAL_SIGN


class WordleFormatError(Exception):
    pass


class WordleMathError(Exception):
    pass


class WordleGuess:
    def __init__(self, guess):
        if not guess or len(guess) != 8:
            length = len(guess) if guess else None
            raise WordleFormatError(f"bad guess format: len={length} guess={guess}")
        self.guess = guess
        self.process()

    def process(self):
        bad_characters = [c for c in self.guess if c not in VALID_CHARACTERS]
        if bad_characters:
            raise WordleFormatError(f"Found bad characters: {bad_characters}")

        equal_signs = [c for c in self.guess if c == EQUAL_SIGN]
        if len(equal_signs) == 0:
            raise WordleFormatError(f"Equation does not contain an equal sign: {self.guess}")
        if len(equal_signs) > 1:
            raise WordleFormatError(f"Equation contains too many equal signs: {self.guess}")
        if self.guess[0] not in NUMBERS:
            raise WordleFormatError(f"Equation must start with a number: {self.guess}")
        if self.guess[0] == "0":
            raise WordleFormatError(f"Equation cannot start with a zero: {self.guess}")
        numbers = re.split(r"[=\-*+/]", self.guess)
        for number in numbers:
            if len(number) > 1 and number[0] == "0":
                raise WordleFormatError(f"Number cannot start with a zero: {self.guess}")
        if self.guess[-1] not in NUMBERS:
            raise WordleFormatError(f"Equation must end with a number: {self.guess}")
        if not [c for c in self.guess if c in OPERATIONS]:
            raise WordleFormatError(f"Equation does not contain any operations: {self.guess}")
        non_number_index = [i for i, c in enumerate(self.guess) if c not in NUMBERS]
        for index in range(len(non_number_index) - 1):
            if non_number_index[index+1] - non_number_index[index] == 1:
                raise WordleFormatError(f"Equation can't have adjacent operations: {self.guess}")

        equal_sign = self.guess.find(EQUAL_SIGN)
        self.test_equation(self.guess[:equal_sign], self.guess[equal_sign + 1:])

    def test_equation(self, left, right):
        if [c for c in right if c in OPERATIONS]:
            raise WordleFormatError(f"Equation has operations right of the equal sign: {self.guess}")

        try:
            if eval(left) != eval(right):
                raise WordleMathError(f"Equation is not equal: {self.guess}")
        except SyntaxError as e:
            raise WordleMathError(f"Syntax error on eval: guess={self.guess} {e}")
        except ZeroDivisionError:
            raise WordleMathError(f"Bad equation, divide by zero: {self.guess}")

    def __str__(self):
        return self.guess


class MathWordle:
    WILDCARD = "_"

    def __init__(self, guess_format, blacklist=None, whitelist=None):
        self.guess_format = guess_format
        self.guesses = []
        self.blacklist = blacklist if blacklist else []
        self.whitelist = whitelist if whitelist else []
        self.exclusions = {}

        self.find_exclusions()

        if len(self.guess_format) != 8:
            raise WordleFormatError(f"Wordle guess does not have 8 characters: {self.guess_format}")
        self.generate_guesses()

    def find_exclusions(self):
        """ extract elements within square braces and add them to the exclusions dict """
        pattern = r"\[.*?\]|."
        splits = re.findall(pattern, self.guess_format)

        for i, split in enumerate(splits):
            if "[" in split:
                self.exclusions[i] = split.replace("[", "").replace("]", "")
                splits[i] = self.WILDCARD

        self.guess_format = "".join(splits)

    def generate_guesses(self):
        wildcards = [i for i, c in enumerate(self.guess_format) if c == "_"]

        if not wildcards:
            self.add_guess(self.guess_format)
            return

        for option_fields in self.get_options(len(wildcards)):
            self.add_guess(self.get_new_guess(wildcards, option_fields))

    def get_new_guess(self, wildcards, option_fields):
        guess = [c for c in self.guess_format]

        # check that whitelisted values are represented in option fields
        if [c for c in self.whitelist if c not in option_fields]:
            return

        for new_character, wildcard in enumerate(wildcards):
            value = option_fields[new_character]

            # make sure that this isn't one of our excluded values
            excluded_values = self.exclusions.get(wildcard)
            if self.exclusions.get(wildcard) and value in excluded_values:
                return
            guess[wildcard] = value

        # return as string, not a list of characters
        return "".join(guess)

    def add_guess(self, guess):
        try:
            self.guesses.append(WordleGuess(guess))
        except (WordleFormatError, WordleMathError):
            pass

    def get_options(self, length):
        characters = [c for c in VALID_CHARACTERS if c not in self.blacklist]
        return list(product(characters, repeat=length))

    def get_guesses(self):
        return [guess.guess for guess in self.guesses]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve Math Wordle")
    parser.add_argument("-m", "--math", type=str,
                        help="The equation guesses so far, use _ for empty spots")
    parser.add_argument("-b", "--blacklist", type=str,
                        help="The tiles that are grayed out and cannot exist in the solution")
    parser.add_argument("-w", "--whitelist", type=str,
                        help="The tiles that are yellow and must exist in the solution")
    args = parser.parse_args()

    if args.math and len(args.math) < 8:
        print("Equation must be provided with at least 8 characters")
        exit(0)

    if not args.math or all([c == "_" for c in args.math]):
        print("All blanks provided, try a solution like \"12+46=58\" to get some guesses on the board")
        exit(0)

    wordle = MathWordle(args.math, blacklist=args.blacklist, whitelist=args.whitelist)

    for solution_number, solution in enumerate(wordle.get_guesses()):
        print(f"{solution_number:3d}: {solution}")

import argparse
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
        if len(guess) != 8:
            raise WordleFormatError(f"bad guess format: len={len(guess)} guess={guess}")
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
            # Be careful here, it's likely a leading zero error, but there may be other reasons
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

        self.update_guesses()

    def update_guesses(self):
        if self.WILDCARD not in self.guess_format:
            try:
                self.guesses = [WordleGuess(self.guess_format)]
            except (WordleFormatError, WordleMathError):
                pass
            return

        wildcards = [i for i, c in enumerate(self.guess_format) if c == "_"]

        options = self.get_options(len(wildcards))

        for option in options:
            new_guess = [c for c in self.guess_format]
            for new_character, wildcard in enumerate(wildcards):
                new_guess[wildcard] = list(option)[new_character]

            try:
                for c in self.whitelist:
                    if c not in new_guess:
                        raise WordleFormatError
                guess = WordleGuess("".join(new_guess))
                self.guesses.append(guess)
            except (WordleMathError, WordleFormatError):
                pass

    def get_options(self, length):
        characters = [c for c in VALID_CHARACTERS if c not in self.blacklist]
        return product(characters, repeat=length)

    def get_guesses(self):
        return [guess.guess for guess in self.guesses]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Solve Math Wordle")
    parser.add_argument("--equation", type=str,
                        help="The equation guesses so far, use _ for empty spots")
    parser.add_argument("--blacklist", type=str,
                        help="The tiles that are grayed out and cannot exist in the solution")
    parser.add_argument("--whitelist", type=str,
                        help="The tiles that are yellow and must exist in the solution")
    args = parser.parse_args()

    if args.equation and len(args.equation) != 8:
        print("Equation must be provided with 8 characters")
        exit(0)

    if not args.equation or all([c == "_" for c in args.equation]):
        print("All blanks provided, try a solution like \"12+46=58\" to get some guesses on the board")
        exit(0)

    wordle = MathWordle(args.equation, blacklist=args.blacklist, whitelist=args.whitelist)

    for solution_number, solution in enumerate(wordle.get_guesses()):
        print(f"{solution_number:3d}: {solution}")

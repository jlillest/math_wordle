# Math Wordle Solver

This is a simple python command-line tool to help solve math wordle 
puzzles from https://mathwordle.com/

Use this tool however you please.

## How to install and run

This tool has no dependencies beyond a system install of python.  It was developed on python 3.10.

Running it is as simple as follows:

```python
python wordle.py
```

To provide the current status of your equation, use the --equation argument.
The equation must conform to the wordle rules, or you'll either see an error
or return zero results.

```python
python wordle.py --math=73-6_=1_
```

You can also provide the whitelist and blacklist arguments to narrow down the guesses.

```python
python wordle.py --math=5+_+7=1_ --whitelist=3 --blacklist=24689-
```

Or, to further narrow down guesses, you can put a list of values that are excluded 
from a column by putting the field in square brackets instead of an underscore.

```python
python wordle.py --math=[13]+[3]+7=1_ --whitelist=3 --blacklist=24689-
```

## Testing

Tests have been written, mostly to help with development of the tool.  They can be
run by executing the following command:

```python
python tests.py
```
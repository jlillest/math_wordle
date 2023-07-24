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
python wordle.py --equation=73-6_=1_
```

You can also provide the whitelist and blacklist arguments to narrow down the guesses.

```python
python wordle.py --equation=5+_+7=1_ --whitelist=3 --blacklist=24689-
```

## The Good, the Bad, and the Ugly

**The Good** This tool is simple to run, will run most everywhere and will help you solve wordle puzzles.

**The Bad** This tool has no gui, no webapp and will probably never see more 
complete features like whitelist characters by position.

**The Ugly** Finding solutions in this tool is not optimized, and therefore may take a really
long time to run on slower systems, especially if you haven't narrowed down the solution much. 
It also uses eval.  Sure, the input to eval is sanitized, but I'm sure there's a better way 
to solve equations, like the python solver library, but it works for this. 
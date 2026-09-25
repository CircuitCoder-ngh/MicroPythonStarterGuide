# Variables & Types

A **variable** is a name for a value you want to use later. You create one
with `=`:

```python
apples = 5
```

Now `apples` means `5` anywhere in your program. You can change it whenever
you like:

```python
apples = apples + 1   # apples is now 6
apples += 1           # a shortcut for the line above; apples is now 7
```

!!! info "`=` versus `==`"
    A single `=` **stores** a value in a variable. A double `==` **compares**
    two values and gives back `True` or `False`. Mixing them up is one of
    the most common beginner mistakes.

## Types of values

Every value has a **type**. These are the ones you'll use most:

| Type | Example | What it's for |
|---|---|---|
| `int` (integer) | `5`, `-12`, `4095` | Whole numbers: counts, pin numbers, sensor readings |
| `float` (floating point) | `5.12`, `0.5`, `-3.3` | Numbers with a decimal point: voltages, seconds |
| `str` (string) | `"Hello"`, `'Fuji'` | Text. Wrap it in single or double quotes |
| `bool` (boolean) | `True`, `False` | Yes/no values: is the button pressed? |

```python
number_of_apples = 5        # int
half_an_apple = 0.5         # float
apple_type = "Fuji"         # str
has_apples = True           # bool
```

You can ask Python for a value's type with `type()`:

```pycon
>>> type(0.5)
<class 'float'>
```

## Naming variables

- Use lowercase words joined with underscores: `button_pin`,
  `servo_angle`.
- Names can't start with a number or contain spaces.
- Names are case-sensitive: `score` and `Score` are different variables.
- Use CAPITALS for values that never change, such as pin numbers:
  `LED_PIN = 27`.

## Maths

```python
print(5 + 5)     # 10   add
print(10 - 5)    # 5    subtract
print(5 * 5)     # 25   multiply
print(4 ** 2)    # 16   power (4 squared)
print(100 / 20)  # 5.0  divide (always gives a float)
print(17 // 5)   # 3    divide and round down to a whole number
print(17 % 5)    # 2    remainder after dividing
```

The `%` (remainder) operator is handy for things that wrap around. For
example, `hour % 12` turns 24-hour time into 12-hour time.

## Converting between types

Sometimes you have a value of one type and need another. For example, a
number that arrives from the internet as text has to become a number before
you can do maths with it.

```python
x = "5.432"     # a string: it's in quotes
x = float(x)    # now the float 5.432
x = int(x)      # now the int 5 (int() chops off the decimals)
x = str(x)      # back to the string "5"
```

!!! warning "`int()` on a string with a decimal point"
    `int("5.432")` gives an error, because the text isn't a whole number.
    Convert to a float first: `int(float("5.432"))` gives `5`.

## Joining text

Use `+` to join strings, and `str()` to turn numbers into text first. An
**f-string** (a string with an `f` in front) is often easier: put any
variable inside `{ }`.

```python
score = 12
print("Score: " + str(score))    # Score: 12
print(f"Score: {score}")         # Score: 12
print(f"{score} points in {half_an_apple} seconds")
```

**Next:** [Lists & Dictionaries](lists-and-dicts.md)

# If, For & While

So far, programs run from top to bottom, one line at a time. **Control
flow** changes that: `if` makes decisions, and `for` and `while` repeat
things.

## if, elif, else

An `if` statement runs its indented code **only when a condition is
`True`**:

```python
fruit = "apple"

if fruit == "apple":
    print("Apples are red")
```

Add `elif` ("else if") to check another condition when the first one was
false, and `else` to catch everything left over. Python checks them from
top to bottom and runs **only the first one that matches**:

```python
fruit = "grape"

if fruit == "apple":
    print("Apples are red")
elif fruit == "grape":
    print("Grapes are purple")      # this one runs
else:
    print("Does not compute")
```

### Comparisons

| Operator | Means |
|---|---|
| `==` | equal to |
| `!=` | not equal to |
| `<` `>` | less than, greater than |
| `<=` `>=` | less than or equal, greater than or equal |

Combine conditions with `and`, `or` and `not`:

```python
if temperature > 30 and not fan_on:
    print("Turning the fan on")
```

## for loops

A `for` loop runs its code **once for every item** in a list, or for every
number in a range.

```python
fruits = ["apple", "grape", "banana"]

for fruit in fruits:
    print(fruit)
```

`fruit` is a new variable that holds the current item each time round the
loop. You can call it anything.

`range()` gives you a sequence of numbers:

```python
for x in range(5):             # 0, 1, 2, 3, 4
    print(x)

for x in range(100, 1000, 50): # 100, 150, 200, ... 950
    print(x)
```

!!! info "range() stops *before* the end number"
    `range(5)` counts 0 to 4, not 0 to 5. And `range(100, 1000, 50)`
    starts at 100, goes up by 50, and stops before reaching 1000.

Loops and `if` statements work together:

```python
for fruit in ["apple", "grape", "banana", "pineapple"]:
    if len(fruit) > 5:
        print(fruit + " has more than 5 letters")
    else:
        print(fruit + " has 5 or fewer letters")
```

## while loops

A `while` loop keeps running **as long as its condition stays `True`**:

```python
x = 10
while x > 0:
    print(x)
    x -= 1          # count down; without this the loop would never end
print("Liftoff!")
```

### while True: the main loop

Almost every microcontroller program has a `while True:` loop. `True` is
always true, so it **runs forever**: check the buttons, update the screen,
check the buttons again, and so on, until the power goes off.

```python
while True:
    if button.was_pressed():
        print("Pressed!")
```

### break

`break` jumps straight out of a loop, even a `while True:` one:

```python
count = 0
while True:
    count += 1
    if count == 5:
        break
print("Stopped at", count)
```

!!! tip "Stuck in a loop?"
    If a program runs forever when it shouldn't, press **Stop** in Thonny
    (++ctrl+f2++), or press ++ctrl+c++ in the Shell.

**Next:** [Functions](functions.md)

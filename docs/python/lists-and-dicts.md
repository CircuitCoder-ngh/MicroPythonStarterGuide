# Lists & Dictionaries

A single variable holds one value. When you have a whole collection, such
as the notes in a song or the squares a snake covers in a game, use a
**list** or a **dictionary**.

## Lists

A list holds values **in order**, inside square brackets:

```python
empty_list = []
fruits = ["apple", "orange", "grape"]
```

Each item has a position, called its **index**. Python starts counting
from **0**:

```python
fruits[0]     # "apple": the first item
fruits[2]     # "grape": the third item
fruits[-1]    # "grape": negative numbers count back from the end
fruits[3]     # IndexError! There is no fourth item
```

Changing a list:

```python
fruits.append("banana")   # add to the end: ["apple", "orange", "grape", "banana"]
fruits.pop(0)             # remove the first item: ["orange", "grape", "banana"]
fruits.remove("grape")    # remove by value: ["orange", "banana"]
fruits[0] = "kiwi"        # replace an item: ["kiwi", "banana"]
len(fruits)               # 2: how many items there are
"kiwi" in fruits          # True: is this value in the list?
```

!!! example "Where lists show up in the projects"
    In [Snake](../projects/snake.md), the snake's body is a list of
    positions. Each move, the new head position is appended to the end, and
    the tail is popped off the front.

## Dictionaries

A **dictionary** (`dict`) stores values under **keys** instead of
positions. Think of a real dictionary: you look up a word (the key) to find
its meaning (the value). Dictionaries use curly braces and `key: value`
pairs:

```python
state_capitals = {
    "Alabama": "Montgomery",
    "Alaska": "Juneau",
    "Arizona": "Phoenix",
}

state_capitals["Alaska"]                      # "Juneau"
state_capitals["California"] = "Sacramento"  # add a new pair
state_capitals.pop("California")             # remove it again
state_capitals.keys()                        # all the keys
state_capitals.values()                      # all the values
len(state_capitals)                          # 3
"Texas" in state_capitals                    # False: checks the keys
```

Keys are usually strings, and values can be anything: numbers, strings,
lists, even other dictionaries.

!!! example "Where dictionaries show up in the lessons"
    When you ask a website's API for data (in [Wi-Fi & APIs](../components/wifi.md)),
    the answer comes back as a dictionary. You pull out the part you want by
    its key, such as `current["temperature_2m"]`.

    The [buzzer lesson](../components/buzzers.md) also uses one to look up
    a musical note's frequency by name: `NOTES["C"]`.

**Next:** [If, For & While](control-flow.md)

# Saving Programs to the Board

When you click **Run**, Thonny sends your code to the board and runs it
once. If you unplug the board, the program is gone. To make the board run
your code **by itself** every time it powers on, save it onto the board as
`main.py`.

## How the ESP32 starts up

MicroPython has a tiny file system on the board, like a mini USB stick.
Every time the board powers on or resets, it:

1. Runs `boot.py`, a setup file that MicroPython creates. Leave it alone.
2. Runs `main.py`, **if there is one**. That's your program.

So "installing" a program just means saving it on the board with the name
`main.py`.

## Save a program as main.py

1. Open your program in Thonny (for example `blink.py` from the last page).
2. Click **File → Save as…**
3. Choose **MicroPython device**.
4. Type the name `main.py` and click **OK**.

Now press the **EN** (or **RST**) button on the board to reset it, or
unplug it and plug it back in. The program starts on its own. It'll even
run from a phone charger or a USB power bank, with no computer attached.

!!! tip "Keep a copy on your computer too"
    Save each program on your computer as well, in a folder such as
    `Documents/circuitcoder/`. The board is a place to *run* code, not
    the best place to *keep* it.

## Copy library files to the board

Some lessons use **library files**: ready-made code that your program
imports, such as `button.py` or the `ssd1306.py` screen driver. These need to
be on the board next to `main.py`.

The easiest way is Thonny's **Files** panel:

1. Open **View → Files**. The top half shows your computer and the bottom
   half shows the board (*MicroPython device*).
2. In the top half, find the file you want (download the library files from
   the [code folder on GitHub](https://github.com/CircuitCoder-ngh/MicroPythonStarterGuide/tree/main/code/lib)
   first).
3. Right-click it and choose **Upload to /**.

The file now appears in the board's list. You can also open any file, then
**File → Save as… → MicroPython device** and type the same file name.

## Stop, edit and delete programs

- **Stop a running program:** click **Stop** (++ctrl+f2++). Thonny
  interrupts the program and gives you a `>>>` prompt again.
- **Edit a file on the board:** double-click it in the **Files** panel
  (bottom half), change it, and press ++ctrl+s++ to save.
- **Delete a file:** right-click it in the bottom half of the Files panel
  and choose **Delete**.

!!! warning "A program that stops you connecting"
    If `main.py` goes wrong in a way that keeps Thonny from connecting
    (for example, a tight loop that hogs the board), click **Stop** a few
    times in a row. If that still doesn't work, see
    [Troubleshooting](../reference/troubleshooting.md).

## One program at a time

The board can only have **one** `main.py` at a time. When you move on to a
new lesson or project, saving its code as `main.py` replaces the old
program. That's fine, because you've kept a copy on your computer.

You're all set up. Next, a quick tour of the Python you'll need, or skip
straight to the hardware if you already know some Python.

[Learn Python Basics](../python/index.md){ .md-button .md-button--primary }
[Skip to Components](../components/index.md){ .md-button }

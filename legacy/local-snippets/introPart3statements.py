
# 'if' statements depend upon a boolean (true/false)
# and either executes the code, or skips it
x = 'apple'
if x == 'apple':# this is true, so the code executes
    print('Apples are red')

# 'elif'(else-if) can be added after an 'if' statement, and
# only activates if that 'if' statement is skipped
x = 'grape'
if x == 'apple': # this is false, so the code is skipped
    print('Apples are red')
elif x == 'grape': # this is true, so the code executes
    print('Grapes are purple')

# 'else' can be added after 'if' or 'elif', and will
# execute if the previous statement is skipped
x = '?'
if x == 'apple': # this is skipped
    print('Apples are red') 
elif x == 'grape': # this is skipped
    print('Grapes are purple')
else: # this executes since the others were skipped
    print('Does not compute')


# 'for' loops iterate through a range or set of data,
# and can execute the same task for each iteration,
# or have specific tasks depending on the iteration
for x in range(0,100): # you are creating a local variable
                       # named 'x' here, you can change it
    # this will print 0-99 since the range command
    # doesn't include the upper bounds number
    print(x)

# iterating through a list
fruits = ['apple','grape','banana','orange','pineapple']
for fruit in fruits:
    print(fruit)

# iterating through a list with multiple actions
fruits = ['apple','grape','banana','orange','pineapple']
for fruit in fruits:
    if len(fruit) > 5:
        print(fruit + 'has more than 5 letters')
    else:
        print(fruit + 'has 5 or less letters')

 
# while loops will continue to execute their code until
# the boolean statement is no longer true, kind of like
# a looping 'if' statement
x = 100
while x >= 20:
    # this will print 100 to 20 before exiting the loop
    print(x)
    X -= 1
    
# to 'break out of a while loop...
while True:
    # this will print the number 5 then exit the loop
    print(5)
    break # without this command, your computer will print
          # out an infinite spawn on 5's 


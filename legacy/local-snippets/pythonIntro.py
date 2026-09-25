# Quick Intro to Python!

# Variables:
# when you need to reference something later on, make a variable, assign it a value, and
#   refer to it when you want to retrieve that value
# accepted data types include...
#   integers, floating point values, strings, booleans, lists, and dictionaries
number_of_apples = 5 # created an integer variable (whole numbers)
half_an_apple = 0.5 # created a floating point variable (decimals)
apple_type = 'Fuji' # created a string variable (text)
has_apples = True # created a boolean variable (True/False)

# Lists:
# lists are a data type that can hold multiple variables
empty_list = [] # created a list that is empty, all you need is the brackets
fruits = ['apples', 'oranges', 'bananas']
fruits[0] # this will return the first value of the list, 'apples'
fruits[3] # this will return our 4th value, 'grapes'
fruits[-1] # this will return the last value of any list
fruits.append('grapes') # adds 'grapes' to the end of the list
fruits.pop(0) # removes the first value from the list

# For Loops and While Loops:
for fruit in fruits:
    print(fruit)
#same as...
for x in range(0,4):
    print(fruits[x])
#same as...
for x in range(0,len(fruits)):
    print(fruits[x])


# Creating/Defining Functions:


-----

# OOP(Object Oriented Programming)


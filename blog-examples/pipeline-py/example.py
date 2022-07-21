from functools import reduce

# Pipeline functions
def add5(x):
    return x+5

def square(x):
    return x*x

def div4(x):
    return x//4

# Use the cool reduce function
output = reduce(lambda input, func: func(input), (add5, square, div4), 5)
print("Push 5 through pipeline: " + str(output))

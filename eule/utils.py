import numpy as np
import functools

# Function to turn array to key with comma-delimiter
def keyfy(lst):
	return str(lst).strip('[]').replace(' ', '')

# reduce function handler
def reduce(func, elems, elem0): 
	return functools.reduce(func, elems+[elem0])

# List with unique elements
unique = lambda lst: list(np.unique(lst))
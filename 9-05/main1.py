# # decorators 
# # decorators are functions that wrap other functions and modify their behavior
# def shout(text):
#     return text.upper()

# f = shout          # no parentheses — the function itself
# print(f('hello')) 

import functools # this is a module that provides a function that wraps other functions and modify their behavior
import time # this is a module that provides a function that returns the current time in seconds

def timed(func):
    @functools.wraps(func) # copy the metadata of the original function
    def wrapper(*args, **kwargs):
        start = time.perf_counter()  # pref_counter is a function that returns the current time in seconds
        result = func(*args, **kwargs)
        print(f" {func.__name__} took {time.perf_counter() - start} seconds")
        return result
    return wrapper
    
@timed
def slow_add(a: int, b: int) -> int:
    time.sleep(0.05) # sleep for 50 milliseconds
    return a + b


def basics():
    print(f"slow_add(1, 2): {slow_add(1, 2)}")
if __name__ == "__main__":
    basics()
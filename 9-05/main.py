
import csv

import sys 
import time
import tempfile 
from pathlib import Path


def squares_list(n:int) -> list[int]:
    result = []
    for i in range(n):
        result.append(i*i)
    return result


def squares_gen(n:int) -> int:
    for i in range(n):

        yield i*i #  hand over one then hold
        
def basics() -> None:
    print(f' "squares_list(5)": {squares_list(5)}')
    g = squares_gen(4)
    print(f' "squares_gen(3)": {g}' , "paused function, nothing ran yet")
    print(next(g)) # 0 -> one value
    print(next(g)) # 1 -> one value
    print(next(g)) # 4 -> one value
    try:
        print(next(g)) # StopIteration
    except StopIteration:
        print("StopIteration")


if __name__ == "__main__":
    basics()





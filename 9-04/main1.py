
from dataclasses import dataclass
from typing import *

def greet(name: str) -> str:
    return f"Hello, {name}!"


def basics() -> None:
    age : int= 32
    price : float= 19.99
    name : str= "Alice"
    active : bool= True
    print(f"Age: {age}, Price: {price}, Name: {name}, Active: {active}")
    
def find_user(user_id:int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob", 3: "Charlie"}
    return users.get(user_id)


def set_mode(mode:list[int],fn:Callable[[int],int]) -> list[int]:
    return [fn(n) for n in mode]

if __name__ == "__main__":
    basics()
    
    

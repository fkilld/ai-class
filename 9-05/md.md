## 1. What it is

A generator is a function that produces values **one at a time, on demand**, instead of building a whole list and handing it over at once.

You write `yield` instead of `return`.

## 2. Why it matters

Memory, and time-to-first-result.

Reading a 4 GB log file into a list needs 4 GB of RAM. Reading it with a generator needs only enough room for one line. Same for a 10-million-row dataset, or a folder of 500 PDFs.

The second reason shows up constantly in LLM work: **streaming**. When ChatGPT prints words as they arrive instead of pausing 8 seconds and dumping a paragraph, that is a generator. You will write exactly this in later modules.
## 3. Simple example

Two ways to get water.

**A list:** you fill a 1000-litre tank first, then drink. You need a tank. You wait for it to fill. If you only wanted one glass, you wasted almost all of it.

**A generator:** you open the tap. Water comes when you ask for it. No tank, no waiting, and you can stop whenever you like.

A generator is a tap, not a tank.




# decorators

## 1. What it is

A decorator wraps a function to add behaviour **without editing the function itself**.

```python
@timed
def fetch_data():
    ...
```

`fetch_data` still does its job. The `@timed` line adds timing around it.

## 2. Why it matters

Some things need to happen around *many* functions: timing, logging, retrying, caching, rate limiting, checking permissions.

Without decorators you copy that code into every function and the real logic drowns in plumbing. With decorators you write it once and apply it with one line.

You will meet decorators constantly in this course:

- `@app.get("/search")` — FastAPI routing
- `@pytest.fixture`, `@pytest.mark.parametrize` — testing
- `@retry(...)` — surviving flaky LLM APIs
- `@lru_cache` — not paying twice for the same embedding
- `@tool` — registering a function as something an agent can call

You need to read them long before you need to write them.

## 3. Simple example

A gift and its wrapping paper.

The gift is unchanged inside. The wrapping adds something around it — presentation, a ribbon, a label. You can wrap any gift with the same paper, and you can unwrap to find the original untouched.

A decorator is wrapping paper for a function.

## 4. How it actually works

The one idea that makes decorators click: **in Python, functions are values.** You can pass them around like numbers or strings.

```python
def shout(text):
    return text.upper()

f = shout          # no parentheses — the function itself
print(f("hi"))     # HI
```

So a decorator is just a function that takes a function and returns a new one:

```python
def timed(func):                       # takes the original
    def wrapper(*args, **kwargs):      # the replacement
        import time
        start = time.perf_counter()
        result = func(*args, **kwargs) # call the original
        print(f"{func.__name__} took {time.perf_counter() - start:.3f}s")
        return result
    return wrapper                     # hand back the replacement
```

And `@` is shorthand:

```python
@timed
def slow_add(a, b):
    ...
```

means exactly:

```python
def slow_add(a, b):
    ...
slow_add = timed(slow_add)
```

That is the whole mechanism. `@timed` reassigns the name `slow_add` to point at `wrapper`.

`*args, **kwargs` means "accept whatever arguments the original accepts" — it makes the wrapper work for any function.

### Always use `functools.wraps`

Without it, the wrapper steals the original's identity:

```python
print(slow_add.__name__)   # "wrapper"  ← wrong, and breaks debugging tools
```

Fix it with one line:

```python
import functools

def timed(func):
    @functools.wraps(func)          # copy name, docstring, type hints across
    def wrapper(*args, **kwargs):
        ...
    return wrapper
```

Now `slow_add.__name__` is `"slow_add"` again. Always include it.

### Decorators that take arguments

`@retry(times=3)` needs one extra layer, because `retry(times=3)` must *return* a decorator:

```python
def retry(times):                 # takes the setting
    def decorator(func):          # takes the function
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ...
        return wrapper
    return decorator
```

Three levels: settings → function → call. That is why `@retry(times=3)` has parentheses and `@timed` does not.

## 5. Code / worked example

A retry decorator — genuinely useful, since LLM and vector-store APIs fail intermittently.

```python
import functools
import time


def retry(times: int = 3, delay: float = 1.0):
    """Retry a function on failure, waiting longer after each attempt."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == times:
                        raise                       # out of attempts, give up
                    print(f"  attempt {attempt} failed ({e}); retrying in {wait}s")
                    time.sleep(wait)
                    wait *= 2                       # exponential backoff
        return wrapper
    return decorator


calls = 0


@retry(times=3, delay=0.5)
def flaky_api(query: str) -> str:
    """Fails the first two times, succeeds on the third."""
    global calls
    calls += 1
    if calls < 3:
        raise ConnectionError("timeout")
    return f"results for {query!r}"


print(flaky_api("cats"))
```

Output:

```
  attempt 1 failed (timeout); retrying in 0.5s
  attempt 2 failed (timeout); retrying in 1.0s
results for 'cats'
```

`flaky_api` contains no retry logic at all. Every function that talks to a network can now get resilience with one line.

Waiting longer each time (0.5s, 1s, 2s) is called **exponential backoff**. Retrying instantly usually just hits the same overloaded server again.

### Free caching from the standard library

```python
import functools


@functools.lru_cache(maxsize=1000)
def embed(text: str) -> tuple[float, ...]:
    print(f"  calling API for {text!r}")
    return (0.1, 0.2, 0.3)          # pretend this costs money and 300ms


embed("hello")   # calls the API
embed("hello")   # instant, free — served from cache
embed("world")   # calls the API
```

Output:

```
  calling API for 'hello'
  calling API for 'world'
```

LRU means *least recently used* — when the cache is full it drops the value untouched for longest. Note the return is a `tuple`, not a `list`: cached values are keyed by argument, and arguments must be hashable.

### Stacking

```python
@timed
@retry(times=3)
def search(query: str): ...
```

Applied **bottom-up**: `retry` wraps `search` first, then `timed` wraps that. So the timer measures all attempts together. Reverse the order and you time each attempt separately. Order matters; think about which behaviour you want.

## 6. Common mistakes

**Forgetting `functools.wraps`.** Breaks `__name__`, docstrings, and tools that inspect functions — including pytest and FastAPI. Symptoms are confusing and hard to trace.

**Forgetting to return the result.** If `wrapper` calls `func(...)` but never returns it, every decorated function silently returns `None`. Extremely common.

**Forgetting to return `wrapper`.** Then the decorator returns `None`, and calling the function gives `TypeError: 'NoneType' object is not callable`.

**Mixing up the two forms.** `@retry` (no parentheses) on a decorator built to take arguments passes your *function* in as `times`. Confusing errors follow. Argument-taking decorators always need `()`, even when empty.

**Hard-coding the signature.** `def wrapper(a, b):` only works for two-argument functions. Use `*args, **kwargs`.

**`lru_cache` with unhashable arguments.** Lists, dicts, and sets cannot be cache keys — `TypeError: unhashable type: 'list'`. Convert to a tuple or string first.

**`lru_cache` on methods.** It holds a reference to `self`, keeping the object alive forever — a slow memory leak.

**Writing one when a plain function would do.** Decorators are for behaviour that must wrap *many* functions. For one place, just write the code there.

## 7. One-line summary

A decorator is a function that takes your function and returns a wrapped version with extra behaviour around it — write `@functools.wraps`, return the result, and you can add timing, retries, or caching to anything in one line.



# context managers

## 1. What it is

A context manager guarantees that **cleanup happens**, even when something goes wrong.

You use one every time you write `with`:

```python
with open("data.txt") as f:
    text = f.read()
# file is closed here — guaranteed
```

## 2. Why it matters

Anything you *open* must be *closed*: files, database connections, network sessions, locks, temporary folders, GPU memory.

If you forget — or an exception jumps over your cleanup line — the resource leaks. A service that leaks database connections works fine in testing and dies in production three hours after deploy, when the connection pool runs out.

`with` makes that impossible to get wrong. Cleanup runs on the happy path, on the error path, and on early `return`.

## 3. Simple example

Borrowing a library book.

You take the book, you read it, you return it. Returning it is not optional — and it has to happen even if you got bored halfway, or the fire alarm went off, or you dropped it in a puddle.

A context manager is a librarian standing at the exit who takes the book back no matter how you leave.

## 4. How it actually works

Look at what `with` replaces:

```python
# manual — leaks if read() raises
f = open("data.txt")
text = f.read()
f.close()

# careful manual — correct, but noisy
f = open("data.txt")
try:
    text = f.read()
finally:
    f.close()          # runs no matter what

# with — same guarantee, one line
with open("data.txt") as f:
    text = f.read()
```

`with` is `try/finally` with the boilerplate removed.

The object you use with `with` needs two methods:

- **`__enter__`** — runs on the way in. Whatever it returns is what `as f` binds to.
- **`__exit__`** — runs on the way out. **Always.** Normal exit, exception, `return`, `break`.

```python
class Resource:
    def __enter__(self):
        print("open")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("close")


with Resource() as r:
    print("working")
    raise ValueError("boom")
```

Output:

```
open
working
close
Traceback (most recent call last):
  ...
ValueError: boom
```

The error still propagates — but "close" printed first. That is the entire point.

`__exit__` receives details of the exception, or three `None`s if all went well. Returning `True` from `__exit__` *swallows* the exception; almost always you want to return nothing, so errors keep travelling.

### The easy way: `@contextmanager`

Writing a class for this is overkill. The standard library gives you a decorator:

```python
from contextlib import contextmanager


@contextmanager
def resource():
    print("open")          # setup
    try:
        yield "the thing"  # hand it to the with-block
    finally:
        print("close")     # teardown — guaranteed


with resource() as r:
    print("got", r)
```

Everything before `yield` is setup. Everything after is cleanup. The `try/finally` is what makes it safe when the body raises — do not skip it.

This is where generators and context managers meet: `yield` pauses the function while the `with` body runs.

## 5. Code / worked example

A timer — the smallest genuinely useful context manager.

```python
import time
from contextlib import contextmanager


@contextmanager
def timer(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {time.perf_counter() - start:.3f}s")


with timer("embedding 1000 docs"):
    time.sleep(0.4)
```

Output:

```
embedding 1000 docs: 0.400s
```

Note there is no `as` — this context manager yields nothing. It just brackets the block.

### Something closer to real work

```python
import sqlite3
from contextlib import contextmanager


@contextmanager
def db(path: str):
    conn = sqlite3.connect(path)
    try:
        yield conn
        conn.commit()        # only on success
    except Exception:
        conn.rollback()      # undo on failure
        raise                # let the caller see the error
    finally:
        conn.close()         # always


with db(":memory:") as conn:
    conn.execute("CREATE TABLE chunks (id INTEGER, text TEXT)")
    conn.execute("INSERT INTO chunks VALUES (1, 'Cats sleep a lot.')")

    for row in conn.execute("SELECT * FROM chunks"):
        print(row)
```

Output:

```
(1, 'Cats sleep a lot.')
```

Commit on success, roll back on failure, close either way. Every caller gets that for free.

### Handy ones already in the standard library

```python
import tempfile
from pathlib import Path
from contextlib import suppress

# temp folder that deletes itself
with tempfile.TemporaryDirectory() as tmp:
    Path(tmp, "test.txt").write_text("hello")
# folder and contents are gone here

# ignore a specific error without a bare try/except
with suppress(FileNotFoundError):
    Path("maybe-missing.txt").unlink()
```

### Several at once

```python
with open("in.txt") as src, open("out.txt", "w") as dst:
    dst.write(src.read())
```

Both close, in reverse order, whatever happens.

### The async version

Since your API clients will be async (see [async/await](01-async-await.md)), you will also see:

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get("https://example.com")
```

Same idea, spelled `async with`, using `__aenter__` / `__aexit__`. To write your own, use `@asynccontextmanager` from `contextlib`.

## 6. Common mistakes

**Not using `with` at all.** Manual `open()` / `close()` works until the line between them raises. Then the file stays open. On Windows this locks the file and the next write fails with a message that names nothing useful.

**Cleanup outside `try` in `@contextmanager`.** This is the big one:

```python
@contextmanager
def bad():
    conn = connect()
    yield conn
    conn.close()      # skipped entirely if the body raises
```

If the `with` body throws, the exception propagates out through `yield` and `conn.close()` never runs. Always wrap in `try/finally`.

**Returning `True` from `__exit__` by accident.** That silently swallows every exception in the block. Bugs vanish without a trace. Return `None` unless suppressing is deliberate.

**More than one `yield` in a `@contextmanager`.** It must yield exactly once. Two yields raises `RuntimeError: generator didn't stop`.

**Assuming the resource survives the block.** After `with open(...) as f:` ends, `f` is closed. Reading from it later fails. Copy out what you need *inside* the block.

**Reusing a `@contextmanager` object.** `cm = timer("x")` then two `with cm:` blocks fails — the underlying generator is exhausted. Call the function fresh each time: `with timer("x"):`.

## 7. One-line summary

A context manager is `try/finally` with a clean face — `with` guarantees setup and teardown around a block, and `@contextmanager` lets you write your own with a `yield` inside a `try/finally`.

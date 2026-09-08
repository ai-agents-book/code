# Python and API basics

Snippets from "Python and API basics", in reading order. These are illustrative fragments rather than a runnable program: the book does not execute them, and several do not stand alone.

```python
help(abs)
dir(str)
```

```python
x = 10
x = "Hello"
```

```python
x = 3
pi = 3.14
flag = True
text = "Python"
missing = None
type(x), type(text), type(missing)
```

```python
x = 3.14
isinstance(x, float)
```

```python
def add(x: int, y: int) -> int:
    return x + y
```

```python
from typing import Optional

def lookup_price(item: str, catalog: dict[str, float]) -> Optional[float]:
    return catalog.get(item)
```

```python
name = "Alice"
name[0]
name[1:4]
```

```python
name = "Alice"
age = 30
msg = f"Name: {name}, age: {age}"
msg
```

```python
price = 19.99
qty = 3
total = price * qty
f"Total: {total:.2f}"
```

```python
line = "  §4.2 Refunds are issued within 5 business days  "
line.strip().lower().startswith("§4.2")
```

```python
parts = "policy,refund,shipping".split(",")
", ".join(parts)
```

```python
values = [10, 20, 30, 40]
pair = (10, 20)
record = {"name": "Alice", "age": 30}
unique = {1, 2, 3}
values[0], pair[1], record["name"]
```

```python
record.get("email", "not provided")
```

```python
10 in {10, 20, 30}
```

```python
def add_numbers(x, y):
    return x + y

args = {"x": 13, "y": 29}
add_numbers(**args)   # identical to add_numbers(x=13, y=29)
```

```python
def describe(*args, **kwargs):
    return args, kwargs

describe(1, 2, city="Berlin")
```

```python
words = ["alpha", "beta", "gamma", "delta"]
lengths = [len(w) for w in words]
long_words = [w for w in words if len(w) > 4]
lengths, long_words
```

```python
long_words = []
for w in words:
    if len(w) > 4:
        long_words.append(w)
long_words
```

```python
x = 5
if x > 10:
    label = "greater than 10"
elif x == 10:
    label = "equal to 10"
else:
    label = "less than 10"
label
```

```python
fruits = ["Apple", "Banana", "Cherry"]
for fruit in fruits:
    print(fruit)
```

```python
words = ["alpha", "beta", "gamma"]
for i, word in enumerate(words):
    print(i, word)

lengths = [5, 4, 5]
for word, length in zip(words, lengths):
    print(f"{word}: {length}")
```

```python
count = 0
while count < 3:
    print(count)
    count += 1
```

```python
temperature = int(input("Temperature (°C): "))
```

```python
def add(x, y):
    return x + y

add(3, 4)
```

```python
def compute_area(width: float, height: float) -> float:
    """Compute the area of a rectangle."""
    return width * height

compute_area.__doc__
```

```python
records = [{"name": "Bob", "age": 30}, {"name": "Anna", "age": 23}]
records_by_age = sorted(records, key=lambda r: r["age"])
records_by_age
```

```python
import math
math.sqrt(16)
```

```python
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call
def greet(name):
    return f"Hello, {name}"

greet("Alice")
```

```python
from contextlib import contextmanager

@contextmanager
def timer(label):
    import time
    start = time.time()
    try:
        yield
    finally:
        print(f"{label}: {time.time() - start:.3f}s")

with timer("work"):
    total = sum(range(1_000_000))
```

```python
import asyncio

async def fetch_value():
    await asyncio.sleep(0.1)
    return 42

asyncio.run(fetch_value())
```

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
    finally:
        print("division attempted")

safe_divide(10, 0)
```

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name}"

person = Person("Alice", 30)
person.greet()
```

```python
class Vehicle:
    def __init__(self, maker, year):
        self.maker = maker
        self.year = year

    def drive(self):
        return f"{self.maker} vehicle is driving"


class Car(Vehicle):
    def __init__(self, maker, year, seats):
        super().__init__(maker, year)
        self.seats = seats

    def drive(self):
        return f"{self.maker} car is driving"


Car("BMW", 2021, 5).drive()
```

```python
from dataclasses import dataclass

@dataclass
class ToolResult:
    status: str
    value: float

ToolResult(status="ok", value=42.0)
```

```python
from pydantic import BaseModel

class TriageResult(BaseModel):
    category: str
    confidence: float
    escalate: bool = False

result = TriageResult(category="refund", confidence=0.87)
result.model_dump()
```

```python
import json

payload = {
    "name": "Alice",
    "age": 25,
    "tags": ["premium", "beta-tester"],
    "address": None,
}
text = json.dumps(payload)
text
```

```python
roundtrip = json.loads(text)
roundtrip == payload
```

```python
print(json.dumps(payload, indent=2))
```

```python
tool_call = {
    "name": "get_weather",
    "arguments": {
        "city": "Berlin",
        "unit": "celsius",
        "forecast_days": [1, 2, 3],
    },
}
json.loads(json.dumps(tool_call))["arguments"]["city"]
```

```python
import requests

base_url = "https://jsonplaceholder.typicode.com"
resp = requests.get(f"{base_url}/posts", params={"userId": 1}, timeout=10)
resp.status_code, resp.json()[0]
```

```python
payload = {"title": "foo", "body": "bar", "userId": 1}
resp = requests.post(f"{base_url}/posts", json=payload, timeout=10)
resp.status_code, resp.json()
```

```python
sess = requests.Session()
sess.headers.update({"Accept": "application/json"})
resp = sess.get(f"{base_url}/posts", timeout=10)
resp.status_code
```

```python
try:
    resp = requests.get(f"{base_url}/posts", timeout=10)
    resp.raise_for_status()
except requests.Timeout:
    print("timeout")
except requests.RequestException as exc:
    print(f"request failed: {exc}")
else:
    print(len(resp.json()))
```

```python
token = "REDACTED"
headers = {"Authorization": f"Bearer {token}"}
```

```python
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
api_key is not None
```

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
async def create_item(item: Item):
    return item
```

```python
from fastapi.testclient import TestClient

client = TestClient(app)
resp = client.post("/items", json={"name": "widget", "price": 9.99})
resp.status_code, resp.json()
```

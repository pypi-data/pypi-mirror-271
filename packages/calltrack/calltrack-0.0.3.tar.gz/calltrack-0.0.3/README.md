Use: 

```py
from calltrack import jsonlog

@jsonlog
def f(x: int) -> int:
    return x

if __name__ == '__main__':
    for i in range(10):
        f(i)
```

This will save a single JSON file containing all the calls to `f` with some details, in a `logs` directory.
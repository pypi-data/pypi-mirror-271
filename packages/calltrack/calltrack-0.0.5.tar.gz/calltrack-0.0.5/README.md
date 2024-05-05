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

This will save a single JSON file containing all the calls to `f` with some details, in a `calltrack_jsonlogs` directory.

A custom directory can be specified as follow:
```py
from calltrack import json_calltrack

json_calltrack.save_dir = "path/to/custom/logs/directory"
```

The logs can be consulted through a streamlit UI. Several files can also be compared one to the other in the UI. 
To display it in a browser, run the following command in CLI: 
```zsh
$ calltrack-view
```

By default, this will point to the default logs directory. 
If a directory was specified by the user, its path should be given as an argument to the command:
```zsh
$ calltrack-view /path/to/custom/logs/directory
```
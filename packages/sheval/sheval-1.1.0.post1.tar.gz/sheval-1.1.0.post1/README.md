# 🐴 sheval

Safely evaluate mathematical and logical expressions. Most operations are supported.

### Whitelisted data types

For security, only certain data types are allowed for constants and variables.

- `str`
- `int`
- `float`
- `complex`
- `list`
- `tuple`
- `set`
- `dict`
- `bool`
- `bytes`
- `NoneType`

## Example

```py
from sheval import sheval

# Variables can be passed on.
variables = dict(
    x =  2,
    y =  3,
)
# And functions too!
functions = dict(
    double = lambda x: x * 2,
)

sheval('double(x) > y', variables, functions)
```
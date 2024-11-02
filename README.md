# CLI Utilities
Useful CLI utilities mostly written in Python.

## `guid`
Generates GUIDs
```
usage: guid.py [-h] [-c COUNT] [-i FROM_INTEGER | -e] [-u | -l]

Generates GUIDs (v4)

options:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        Number of GUIDs to generate
  -i FROM_INTEGER, --from-integer FROM_INTEGER
                        Generate a GUID from a 128-bit integer
  -e, --empty           Generate an empty GUID (all bits 0)
  -u, --uppercase       Use uppercase letters
  -l, --lowercase       Use lowercase letters
```


## `urandom`
Generates a random string
```
usage: urandom.py [-h] [-i SIZE] [-c CHARSET] [-x | -b]

Generate random data

options:
  -h, --help            show this help message and exit
  -i SIZE, --size SIZE  Number of bytes to generate
  -c CHARSET, --charset CHARSET
                        Character set to use
  -x, --hex             Output as HEX
  -b, --bytes           Output as a bytes
```

## `yyargs`
A simpler `xargs`

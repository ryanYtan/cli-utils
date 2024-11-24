#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser(description='Splits text into lines based on a delimiter')
parser.add_argument('-d', '--delimiter', default=',', type=str, help='Delimiter to split on')
parser.add_argument('-n', '--ignore-empty', action='store_true', default=False, help='Ignore empty lines')
parser.add_argument('-w', '--no-empty-write', action='store_true', default=True, help='Do not write empty lines')
parser.add_argument('-t', '--trim', action='store_true', default=True, help='Trim whitespace from lines')

def main():
    args = parser.parse_args()
    delimiter = args.delimiter
    trim = args.trim

    for line in sys.stdin:
        if args.ignore_empty and not line.strip():
            continue
        for part in line.split(delimiter):
            if args.no_empty_write and not part.strip():
                continue
            print(part.strip() if trim else part)

if __name__ == '__main__':
    main()

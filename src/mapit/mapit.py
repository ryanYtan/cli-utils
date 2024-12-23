#!/usr/bin/env python3

import sys
import argparse

parser = argparse.ArgumentParser(description='Maps lines from stdin using a mapping file')
parser.add_argument('-i', '--input-mapping', type=str, required=True, help='File containing the mapping')
parser.add_argument('-d', '--map-delimiter', type=str, default=':', help='Delimiter used in the mapping file')
parser.add_argument('-e', '--default-value', type=str, default='', help='Default value to use if no mapping is found')

def main():
    args = parser.parse_args()
    delimiter = args.map_delimiter
    input_mapping = args.input_mapping
    m = {}
    with open(input_mapping, 'r') as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            line = [x.strip() for x in line.split(delimiter)]
            try:
                key, value = line[0], line[1]
                m[key] = value
            except:
                continue
    for line in sys.stdin:
        line = line.strip()
        if line in m:
            print(m[line])
        else:
            print(args.default_value)

if __name__ == '__main__':
    main()

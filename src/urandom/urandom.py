#!/usr/bin/env python3

import argparse
import string
import sys
import os

parser = argparse.ArgumentParser(description='Generate random data')
parser.add_argument('-i', '--size', type=int, default=32, help='Number of bytes to generate')
parser.add_argument('-c', '--charset', type=str, default=string.ascii_letters + string.digits, help='Character set to use')

output_group = parser.add_mutually_exclusive_group()
output_group.add_argument('-x', '--hex', action='store_true', help='Output as HEX')
output_group.add_argument('-b', '--bytes', action='store_true', help='Output as a bytes')

def main(args: argparse.Namespace):
    rands = os.urandom(args.size)
    if args.hex:
        print(rands.hex())
    elif args.bytes:
        sys.stdout.buffer.write(rands)
        sys.stdout.buffer.flush()
    else:
        print(''.join([args.charset[c % len(args.charset)] for c in rands]))

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

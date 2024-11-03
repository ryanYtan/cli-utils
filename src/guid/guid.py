import argparse
import uuid

parser = argparse.ArgumentParser(description='Generates GUIDs (v4)')
parser.add_argument('-c', '--count', type=int, default=1, help='Number of GUIDs to generate')
from_group = parser.add_mutually_exclusive_group()
from_group.add_argument('-i', '--from-integer', type=int, required=False, help='Generate a GUID from a 128-bit integer')
from_group.add_argument('-e', '--empty', action='store_true', help='Generate an empty GUID (all bits 0)')
to_group = parser.add_mutually_exclusive_group()
to_group.add_argument('-u', '--uppercase', action='store_true', help='Use uppercase letters')
to_group.add_argument('-l', '--lowercase', action='store_true', help='Use lowercase letters')

def main(args: argparse.Namespace):
    for _ in range(args.count):
        if args.from_integer:
            guid = uuid.UUID(int=args.from_integer)
        elif args.empty:
            guid = uuid.UUID(int=0)
        else:
            guid = uuid.uuid4()
        print(str(guid).upper() if args.uppercase else guid)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

from __future__ import annotations
import argparse
import abc
import sys
import subprocess
from typing import Optional, List

class Argument:
    def __init__(self, base: str) -> None:
        self.base = base

    @abc.abstractmethod
    def substitute(self, args: list[str]) -> str:
        raise NotImplementedError()

class Positional(Argument):
    def __init__(self, pos: int) -> None:
        super().__init__('')
        self.pos = pos

    def substitute(self, args: list[str]) -> str:
        return args[self.pos]

    def __eq__(self, value: object) -> bool:
        return super().__eq__(value) and self.pos == value.pos

    def __str__(self) -> str:
        return f'{type(self).__name__}({self.pos})'

    def __repr__(self) -> str:
        return str(self)

class Literal(Argument):
    def __init__(self, base: str) -> None:
        super().__init__(base)

    def substitute(self, _: list[str]) -> str:
        return self.base

    def __add__(self, other: Literal) -> Literal:
        return Literal(self.base + other.base)

    def __eq__(self, value: object) -> bool:
        return super().__eq__(value) and self.base == value.base

    def __str__(self) -> str:
        return f'{type(self).__name__}("{self.base}")'

    def __repr__(self) -> str:
        return str(self)

class Stream:
    def __init__(self, s: str) -> None:
        self.base = s
        self._s = [c for c in s]
        self._i = 0

    def _incr(self, n: int) -> None:
        self._i += n
        if self._i >= len(self._s):
            self._i = len(self._s)
        if self._i < 0:
            self._i = -1

    def look(self, i: int = 0) -> Optional[str]:
        t = self._i + i
        if t < 0 or t >= len(self._s):
            return None
        return self._s[t]

    def consume(self, i: int = 1) -> None:
        self._incr(i)

    def prev(self) -> Optional[str]:
        self._incr(-1)
        return self.look()

    def skip_spaces(self) -> int:
        skipped = 0
        while self.look().isspace():
            skipped += 1
            self.consume()
        return skipped

    def expect(self, s: str) -> bool:
        if self.look() == s:
            self.consume()
            return True
        return False

    def is_at_end(self) -> bool:
        return self._i >= len(self._s)

    def curr(self) -> int:
        return self._i

def parse_fmt(s: str):
    args: List[Argument] = []
    st = Stream(s)
    while not st.is_at_end():
        skipped_spaces = st.skip_spaces()
        if skipped_spaces > 0:
            args.append(Literal(' ' * skipped_spaces))
        elif st.look() == '{' and st.look(1) != '{':
            st.consume()
            if st.is_at_end():
                raise ValueError(f'Expected "}}" in {st.base} at position {st.curr()}')
            elif st.look() == '{':
                st.consume()
                args.append(Literal('{'))
            else:
                pos = ''
                while not st.is_at_end() and st.look().isdigit():
                    pos += st.look()
                    st.consume()
                if st.look() != '}':
                    raise ValueError(f'Expected "}}" in {st.base} at position {st.curr()}')
                st.consume()
                args.append(Positional(int(pos)))
        elif st.look() == '}':
            st.consume()
            if st.look() == '}':
                st.consume()
                args.append(Literal('}'))
            else:
                raise ValueError(f'Unexpected "}}" in {st.base} at position {st.curr()}')
        else:
            curr = []
            while not st.is_at_end():
                if st.look() == '{':
                    if st.look(1)  == '{':
                        curr.append('{')
                        st.consume(2)
                    else:
                        break
                elif st.look() == '}':
                    if st.look(1) == '}':
                        curr.append('}')
                        st.consume(2)
                    else:
                        raise ValueError(f'Unexpected "}}" in {st.base} at {st.curr()}')
                else:
                    curr.append(st.look())
                    st.consume()
            args.append(Literal(''.join(curr)))

    #merge the basic strings
    return args

parser = argparse.ArgumentParser(description='Simpler xargs')
parser.add_argument('command', nargs='+', help='Command to run')

def main(args: argparse.Namespace):
    formatter = [parse_fmt(c) for c in args.command]
    for line in sys.stdin:
        line = line.rstrip('\r\n')
        line = line.split(' ')
        cmd = []
        for f in formatter:
            arg = []
            for a in f:
                arg.append(a.substitute(line))
            cmd.append(''.join(arg))
        subprocess.run(cmd)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

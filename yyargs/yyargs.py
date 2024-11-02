import argparse
import abc
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

class BasicString(Argument):
    def __init__(self, base: str) -> None:
        super().__init__(base)

    def substitute(self, _: list[str]) -> str:
        return self.base

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

    def lookaround(self, i: int = 1) -> Optional[str]:
        t = self._i + i
        if t < 0 or t >= len(self._s):
            return None
        return self._s[t]

    def consume(self, i: int = 1) -> Optional[str]:
        c = self.lookaround(i)
        self._incr(i)
        return c

    def prev(self) -> Optional[str]:
        self._incr(-1)
        return self.lookaround()

    def skip_spaces(self) -> bool:
        skipped = False
        while self.lookaround().isspace():
            skipped = True
            self.consume()
        return skipped

    def expect(self, s: str) -> bool:
        if self.lookaround() == s:
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
        if st.skip_spaces():
            raise ValueError(f'Unexpected space in {st.base} at {st.curr()}')
        if st.lookaround() == '{':
            st.consume()
            if st.lookaround() == '{':
                st.consume()
                args.append(BasicString('{'))
            else:
                pos = ''
                while not st.is_at_end() and st.lookaround().isdigit():
                    pos += st.consume()
                if st.lookaround() != '}':
                    raise ValueError(f'Expected "}}" in {st.base} at {st.curr()}')
                st.consume()
                args.append(Positional(int(pos)))
        elif st.lookaround() == '}':
            st.consume()
            if st.lookaround() == '}':
                st.consume()
                args.append(BasicString('}'))
            else:
                raise ValueError(f'Unexpected "}}" in {st.base} at {st.curr()}')
        else:
            base = ''
            while not st.is_at_end() and st.lookaround() not in '{}':
                base += st.consume()
            args.append(BasicString(base))
    return args


parser = argparse.ArgumentParser(description='Simpler xargs')
parser.add_argument('COMMAND', type=str, help='Command to run')

def main(args: argparse.Namespace):
    print(args.command)
    print(args.args)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

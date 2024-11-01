import argparse
import enum
from typing import Tuple, Optional

class Token(enum.Enum):
    LITERAL = 0
    WHITESPACE = 1
    POS_BR_OPEN = 2
    POS_BR_CLOSE =  3
    POS_NUM = 4

class Stream:
    def __init__(self, s: str) -> None:
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

    def is_at_end(self) -> bool:
        return self._i >= len(self._s)

    def curr(self) -> int:
        return self._i

def get_token(s: Stream) -> Tuple[Token, str]:
    if s.skip_spaces():
        return (Token.WHITESPACE, ' ')
    if s.lookaround() == '{' and s.lookaround(2) is None:
        raise ValueError('')
    if s.lookaround() == '{' and s.lookaround(2) == '{':
        return (Token.POS_BR_OPEN, s.consume())



parser = argparse.ArgumentParser(description='Simpler xargs')
parser.add_argument('COMMAND', type=str, help='Command to run')

def main(args: argparse.Namespace):
    print(args.command)
    print(args.args)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

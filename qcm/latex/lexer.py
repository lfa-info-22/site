
from qcm.latex.token import LatexToken, TokenType
import string

LATEX_OPERATORS = set([
    "\\",
    "{",
    "}",
    "[",
    "]",
])

BINDINGS = {
    "{": TokenType.LEFT_CURLY_BRACKET,
    "}": TokenType.RIGHT_CURLY_BRACKET,
    "[": TokenType.LEFT_SQUARED_BRACKET,
    "]": TokenType.RIGHT_SQUARED_BRACKET,
}

class LatexLexer:
    def __init__(self, string):
        self.string = string
        self.tokens = None

        self.idx = -1
        self.advance()

    def advance (self, off=1):
        self.idx += off
        self.advanced = 0 <= self.idx < len(self.string)
        self.chr = self.string[self.idx] if self.advanced else False

        return self.advanced
    def next (self, off=1):
        valid = 0 <= self.idx + off < len(self.string)

        return self.string[self.idx + off] if valid else False

    def build (self):
        if self.tokens != None: return self.tokens
        self.tokens = []
        cur = 0

        while self.advanced:
            if self.chr == "$":
                self.advance()

                while self.advanced and self.chr != "$":
                    self.advance()
                
                if not self.advanced:
                    raise Exception("Expected a $ to close a $ expression")
                self.advance()

                continue

            if self.chr == "\\" and self.next() in LATEX_OPERATORS:
                self.advance(2)
            elif self.chr == "\\":
                if cur != self.idx:
                    self.tokens.append(
                        LatexToken(TokenType.TEXT, self.string[cur:self.idx])
                            .set_pos(cur, self.idx - cur)
                            .set_source(self.string)
                            .validate_whitespace()
                    )

                self.advance()

                if not self.chr in string.ascii_letters:
                    self.advance()
                    continue

                name_start = self.idx
                while self.chr in string.ascii_letters:
                    self.advance()
                
                self.tokens.append(
                    LatexToken(TokenType.BACKSLASHED_NAME, self.string[name_start:self.idx])
                        .set_pos(name_start, self.idx - name_start)
                        .set_source(self.string)
                )

                cur = self.idx
            elif self.chr in LATEX_OPERATORS:
                if cur != self.idx:
                    self.tokens.append(
                        LatexToken(TokenType.TEXT, self.string[cur:self.idx])
                            .set_pos(cur, self.idx - cur)
                            .set_source(self.string)
                            .validate_whitespace()
                    )
                
                self.tokens.append(
                    LatexToken(BINDINGS[self.chr])
                        .set_pos(self.idx, 1)
                        .set_source(self.string)
                )
                self.advance()

                cur = self.idx
            else:
                self.advance()
        
        if cur != self.idx:
            self.tokens.append(
                LatexToken(TokenType.TEXT, self.string[cur:self.idx])
                    .set_pos(cur, self.idx - cur)
                    .set_source(self.string)
                    .validate_whitespace()
            )

        return self.tokens
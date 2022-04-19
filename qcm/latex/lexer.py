
from qcm.latex.token import LatexToken

LATEX_OPERATORS = set([
    "\\",
    "{",
    "}",
    "[",
    "]",
])

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

        while self.chr:
            if self.chr in LATEX_OPERATORS:
                if self.chr == "\\" and self.next() in LATEX_OPERATORS:
                    self.advance(2)
                    continue
                
                if cur != self.idx:
                    if not self.string[cur:self.idx].isspace():
                        self.tokens.append ( LatexToken ( "NAME", self.string[cur:self.idx])
                            .set_pos(cur, self.idx - cur)
                            .set_source(self.string)
                            .validate_name() )

                self.tokens.append(LatexToken( self.chr )
                        .set_pos( self.idx, 1 )
                        .set_source(self.string))
                cur = self.idx + 1

            self.advance()
        
        if cur != len(self.string):
            if not self.string[cur:].isspace():
                self.tokens.append ( LatexToken ( "NAME", self.string[cur:len(self.string)])
                    .set_pos(cur, len(self.string) - cur)
                    .set_source(self.string)
                    .validate_name() )
        
        return self.tokens
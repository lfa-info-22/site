


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

        
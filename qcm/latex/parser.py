

from qcm.latex.elem import LatexElement, LatexParameter
from qcm.latex.lexer import LATEX_OPERATORS
from qcm.latex.token import TokenType


class LatexParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.root = None

        self.idx = -1
        self.advance()

    def advance (self, off=1):
        self.idx += off
        self.advanced = 0 <= self.idx < len(self.tokens)
        self.token = self.tokens[self.idx] if self.advanced else False

        return self.advanced
    def advance_white_space(self):
        while self.advanced and self.token.type == TokenType.WHITETEXT:
            self.advance()
    def next (self, off=1):
        valid = 0 <= self.idx + off < len(self.tokens)

        return self.tokens[self.idx + off] if valid else False

    def build(self):
        if self.root != None: return self.root

        childs = self._build()

        return LatexElement("root", childs)
    
    def _build(self, until=[]):
        childs = []

        while self.advanced:
            if self.token.type in until: 
                return childs

            if self.token.is_text():
                childs.append(self.token.value if self.token.is_text() else self.token.name)
            elif self.token.type == TokenType.BACKSLASHED_NAME:
                token = self.token
                self.advance()

                last_length = -1
                subchilds = []

                while last_length != len(subchilds):
                    last_length = len(subchilds)

                    self.advance_white_space()

                    while self.token and self.token.type == TokenType.LEFT_SQUARED_BRACKET:
                        self.advance()
                        subchilds.append(LatexParameter("SQUARED", self._build([TokenType.RIGHT_SQUARED_BRACKET])))

                        if self.token and self.token.type != TokenType.RIGHT_SQUARED_BRACKET: raise Exception()
                        self.advance()

                    self.advance_white_space()

                    while self.token and self.token.type == TokenType.LEFT_CURLY_BRACKET:
                        self.advance()
                        subchilds.append(LatexParameter("CURLY", self._build([TokenType.RIGHT_CURLY_BRACKET])))

                        if self.token and self.token.type != TokenType.RIGHT_CURLY_BRACKET: raise Exception()
                        self.advance()
                
                self.idx -= 1
                childs.append(LatexElement(token.value, subchilds))
            
            if self.token and self.token.type in until: return childs
            self.advance()
        
        return childs

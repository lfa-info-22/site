

from qcm.latex.elem import LatexElement, LatexParameter


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
    def next (self, off=1):
        valid = 0 <= self.idx + off < len(self.tokens)

        return self.tokens[self.idx + off] if valid else False

    def build(self):
        if self.root != None: return self.root

        childs = self._build()

        return LatexElement("root", childs)
    
    def _build(self, until="}"):
        childs = []

        while self.advanced:
            if self.token.name in until: 
                return childs

            if self.token.is_text():
                childs.append(self.token.value)
            elif self.token.name == "\\":
                self.advance()

                name = self.token.value.split(" ")[0]
                self.advance()
                subchilds = []
                last_length = -1

                while last_length != len(subchilds):
                    last_length = len(subchilds)

                    while self.token and self.token.name == "[":
                        self.advance()
                        subchilds.append(LatexParameter("SQUARED", self._build("]")))

                        if self.token and self.token.name != "]": raise Exception()
                        self.advance()

                    while self.token and self.token.name == "{":
                        self.advance()
                        subchilds.append(LatexParameter("CURLY", self._build("}")))

                        if self.token and self.token.name != "}": raise Exception()
                        self.advance()
                
                childs.append(LatexElement(name, subchilds))
            
            if self.token and self.token.name in until: return childs
            self.advance()
        
        return childs

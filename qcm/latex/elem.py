

from qcm.latex.lexer import LatexLexer


class LatexParameter:
    def __init__(self, type, elements):
        self.type = type
        self.elements = elements

        if not self.type in ['CURLY', 'SQUARED']: raise Exception()
    def _query(self, tokens, result, depth=-1):
        for element in self.elements:
            if type(element) in [LatexElement, LatexParameter]:
                element._query(tokens, result, depth)
    def __str__(self):
        if self.type == 'CURLY':
            return "{" + " ".join(list(map(str, self.elements))) + "}"
        return "[" + " ".join(list(map(str, self.elements))) + "]"

class LatexElement:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters

    def __str__(self):
        string = "".join(list(map(str, self.parameters)))
        return f"\\{self.name} {string}"

    def query (self, string, depth=-1):
        tokens = string.split(" ")
        result = []

        self._query(tokens, result, depth)

        return result
    
    def _query(self, tokens, result, depth=-1):
        if depth == 0: return
        next_depth = max(-1, depth - 1)


        if self.name == tokens[0]:
            next_tokens = tokens[1:]
            if len( next_tokens ) == 0:
                result.append(self)
                return

            for parameter in self.parameters:
                parameter._query(next_tokens, result, next_depth)
        
        for parameter in self.parameters:
            parameter._query(tokens, result, next_depth)


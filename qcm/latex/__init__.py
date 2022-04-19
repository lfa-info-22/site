

from qcm.latex.lexer import LatexLexer
from qcm.latex.parser import LatexParser


def evaluate_latex(string):
    lexer = LatexLexer(string)
    tokens = lexer.build()

    return LatexParser( tokens ).build()

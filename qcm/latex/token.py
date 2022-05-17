
import enum

class TokenType(enum.Enum):
    TEXT                  = 0
    BACKSLASHED_NAME      = 1
    LEFT_SQUARED_BRACKET  = 2
    RIGHT_SQUARED_BRACKET = 3
    LEFT_CURLY_BRACKET    = 4
    RIGHT_CURLY_BRACKET   = 5
    WHITETEXT             = 6

class LatexToken:
    def __init__(self, type:TokenType, value=None):
        self.type = type
        self.value = value
        self.source = ""
    
    def is_text(self):
        return self.type == TokenType.TEXT or self.type == TokenType.WHITETEXT
    def is_white_text(self):
        return self.type == TokenType.WHITETEXT
    def is_operator(self):
        return not self.is_text()

    def set_pos (self, start, length):
        self.start = start
        self.length = length

        return self
    def set_source(self, string):
        self.source = string

        return self
    def validate_whitespace(self):
        self.type = TokenType.WHITETEXT if self.is_text() and self.value.isspace() else self.type
        return self
    
    def __str__(self):
        return str(self.type) + ":" + str(self.value)

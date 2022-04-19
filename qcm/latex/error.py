


class LatexTokenException:
    def __init__(self, token) -> None:
        self.token = token
    def __str__(self):
        return f"Error at token {self.token.name} at text-idx={self.token.start} with length={self.token.length}"



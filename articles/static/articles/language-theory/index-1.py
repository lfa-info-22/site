
SPECIAL_CHARACTERS = {
    "+": "PLUS",
    "-": "MINUS",
    "*": "TIMES",
    "/": "DIVIDE",
    "=": "EQUALS",
}
NUMBER_CHARACTERS = "0123456789"

def lexer(string):
    tokens = []
    id = 0

    while id < len(string):
        if string[id] in SPECIAL_CHARACTERS:
            tokens.append((SPECIAL_CHARACTERS[string[id]], ))
        elif string[id] in NUMBER_CHARACTERS:
            value = ''
            while id < len(string) and string[id] in NUMBER_CHARACTERS:
                value += string[id]
                id += 1
            id -= 1
            tokens.append(('NUMBER', value))

        id += 1
    
    return tokens

def parse_expr(tokens):
    return parse_add(tokens)

def parse_add(tokens):
    left = parse_mult(tokens)

    while len(tokens) > 0 and tokens[0][0] in [ "PLUS", "MINUS" ]:
        tok = tokens[0][0]
        tokens.pop(0)

        right = parse_mult(tokens)
        left = left + right if tok == "PLUS" else left - right
    
    return left
    
def parse_mult(tokens):
    left = factor(tokens)

    while len(tokens) > 0 and tokens[0][0] in [ "TIMES", "DIVIDE" ]:
        tok = tokens[0][0]
        tokens.pop(0)

        right = factor(tokens)
        left = left * right if tok == "TIMES" else left / right
    
    return left

def factor(tokens):
    num = float(tokens[0][1])
    tokens.pop(0)
    return num

inp = input()
print("Result: "+str(parse_expr(lexer(inp))))
print("Expected (Python): " + str(eval(inp)))

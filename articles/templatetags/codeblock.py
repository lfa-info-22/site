
from django import template

register = template.Library()

@register.tag()
def codeblock(parser, token):
    nodelist = parser.parse(('endcodeblock', ))
    parser.delete_first_token()
    content = token.split_contents()
    return CodeBlockNode(nodelist, 'psc' if len(content) == 1 else content[1], content[2:])

PSC_CONF = {
    'keywords' :[
        ( 'tant', 'text-violet-400' ),
        ( 'que', 'text-violet-400' ),
        ( 'si', 'text-violet-400' ),
        ( 'ajouter', 'text-violet-400' ),
        ( 'fonction', 'text-sky-500' ),
        ( 'id', 'text-sky-300' ),
        ( 'on', 'text-violet-400' ),
        ( 'retire', 'text-violet-400' ),
        ( 'stocke', 'text-violet-400' ),
        ( 'récupère', 'text-violet-400' ),
        ( 'retourner', 'text-violet-400' )
    ],
    'comments': 'text-emerald-200 text-xs lg:text-sm',
    'string': 'text-emerald-300',
    'call': 'text-sky-300',
    'var' : 'text-sky-200',
    'number': 'text-emerald-100',
}
PYTHON_CONF = {
    'keywords' :[
        ( 'while', 'text-violet-400' ),
        ( 'int', 'text-sky-300' ),
        ( 'for', 'text-violet-400' ),
        ( 'in', 'text-violet-400' ),
        ( 'return', 'text-violet-400' ),
        ( 'if', 'text-violet-400' ),
        ( 'elif', 'text-violet-400' ),
        ( 'else', 'text-violet-400' ),
        ( 'def', 'text-sky-500' ),
        ('import', 'text-violet-400')
    ],
    'comments': 'text-emerald-200 text-xs lg:text-sm',
    'string': 'text-emerald-300',
    'call': 'text-sky-300',
    'var' : 'text-sky-200',
    'number': 'text-emerald-100',
}

class CodeBlockNode(template.Node):
    def __init__(self, nodelist, lang, spe_names):
        self.nodelist = nodelist
        self.lang = lang
        self.spe_names = spe_names
    def render(self, context):
        output = self.nodelist.render(context)

        tokens = ColorLexer(output).build()
        color_tokens = []

        config = getattr(self, f"render_{self.lang}")()
        
        last_token = None
        for idx in range(len(tokens) - 1, -1, -1):
            name, text = tokens[idx]
            
            color = None
            if name == "NAME":
                color = config['var']
                if last_token != None and last_token[0] == "TEXT" and last_token[1] == "(":
                    color = config['call']
                
                for key, col in config['keywords']:
                    if key == text:
                        color = col
            elif name == "NUMBER":
                color = config['number']
            elif name == "STRING":
                color = config['string']
            elif name == "COMMENTS":
                color = config['comments']
            
            color_tokens.append((text, color))
            if name != "TEXT" or (not text.isspace()):
                last_token = tokens[idx]
        color_tokens.reverse()
        colored_text = [
            f"<span class=\"{color}\">{text}</span>" if color
            else text for text, color in color_tokens
        ]
        lines = list(map(self.create_line, enumerate("".join(colored_text).split("\n"))))

        LINES  = "".join(lines)
        LANG = self.get_lang_name(self.lang)
        TEMPLATE = f'''
            <div class="text-sm font-light text-right text-gray-400">{LANG}</div>
            <div class="flex flex-wrap bg-stone-800 text-gray-200 rounded-xl p-3 overflow-x-auto">
                {LINES}
            </div>
        '''

        return TEMPLATE
    def get_lang_name(self, lang):
        if lang == "psc": return "Pseudo-Code"
        elif lang == "python": return "Python"
        return "Inconnu"
    
    def create_line(self, tuple):
        idx, line = tuple
        return f'''
        <div class="text-right w-8 px-2 text-gray-300">{idx}</div>
        <div class="w-[calc(100%-40px)] whitespace-pre pr-6">{line}</div>
    '''
    
    def render_psc(self):
        return PSC_CONF
    def render_python(self):
        return PYTHON_CONF

import string

class ColorLexer:
    def __init__(self, string):
        self.string = string
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

    def build(self):
        if hasattr(self, "tokens"): return self.tokens

        self.tokens = []

        self.advance()
        while self.advanced:
            if self.chr == '\\':
                self.advance()
                self.tokens.append(("TEXT", self.string[self.idx:self.idx + 1]))
                self.advance()
            elif (x := self.lex_special(string.digits))[0]:
                self.tokens.append(("NUMBER", x[1]))
            elif (x := self.lex_special(string.ascii_letters + '_éàèêâëïöüä' + string.digits))[0]:
                self.tokens.append(("NAME", x[1]))
            elif (self.chr == "/" and self.next() == "/") \
              or (self.chr == "#" and self.next() == "#"):
                start = self.idx
                while self.advanced and self.chr != "\n":
                    self.advance()

                self.tokens.append(("COMMENTS", self.string[start:self.idx]))
            elif self.chr == "\"" or self.chr == "\'" or self.chr == '`':
                stop_chr = self.chr
                start = self.idx
                self.advance()
                while self.advanced and self.chr != stop_chr:
                    if self.chr == '\\': self.advance()
                    self.advance()
                
                self.advance()
                self.tokens.append(("STRING", self.string[start:self.idx]))
            elif self.chr in string.whitespace:
                start = self.idx
                while self.advanced and self.chr in string.whitespace:
                    self.advance()
                self.tokens.append(("TEXT", self.string[start:self.idx]))
            elif self.chr in "()[]{}:+-=*/^|&,.":
                self.tokens.append(("TEXT", self.string[self.idx:self.idx + 1]))
                self.advance()
            else:
                raise Exception("Unknown character " + self.chr)

        return self.tokens
    def lex_special(self, mstring):
        start = self.idx
        while self.advanced and self.chr in mstring:
            self.advance()
        
        return start - self.idx != 0, self.string[start:self.idx]
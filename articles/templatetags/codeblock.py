
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
        ( 'tant que', 'text-violet-400' ),
        ( 'si', 'text-violet-400' ),
        ( 'ajouter', 'text-violet-400' ),
        ( 'fonction', 'text-sky-500' ),
        ( 'id', 'text-sky-300' ),
        ( 'string', 'text-sky-300' ),
        ( 'tokens', 'text-sky-300' ),
    ],
    'comments': 'text-emerald-200 text-xs lg:text-sm',
    'string': 'text-emerald-300'
}

class CodeBlockNode(template.Node):
    def __init__(self, nodelist, lang, spe_names):
        self.nodelist = nodelist
        self.lang = lang
        self.spe_names = spe_names
    def render(self, context):
        output = self.nodelist.render(context)

        lines = getattr(self, f"render_{self.lang}")(output)
        while len(lines) > 0 and lines[0] == '':
            lines = lines[1:]
        while len(lines) > 0 and lines[-1] == '':
            lines = lines[:len(lines) - 1]

        for lidx in range(len(lines)):
            lines[lidx] = self.create_line(lines[lidx], lidx + 1)

        LINES  = "".join(lines)
        LANG = self.get_lang_name(self.lang)
        TEMPLATE = f'''
            <div class="text-sm font-light text-right text-gray-400">{LANG}</div>
            <div class="flex flex-wrap bg-stone-800 text-gray-200 rounded-xl p-3">
                {LINES}
            </div>
        '''

        return TEMPLATE
    def get_lang_name(self, lang):
        if lang == "psc": return "Pseudo-Code"
        return "Inconnu"
    
    def create_line(self, line, idx):
        return f'''
        <div class="text-right w-8 px-2 text-gray-300">{idx}</div>
        <div class="w-[calc(100%-40px)] whitespace-pre">{line}</div>
    '''
    
    def render_psc(self, string):
        string_indices = []
        for i in range(len(string)):
            if string[i] == "\"":
                string_indices.append(i)
        
        if len(string_indices) % 2 == 1:
            string_indices.pop()
        
        for i in range(len(string_indices) - 1, -1, -2):
            innerString = string[string_indices[i - 1]:string_indices[i] + 1]
            string = string[:string_indices[i - 1]] + f"<span class=\"text-green-600\">{innerString}</span>" + string[string_indices[i] + 1:]

        for keyword in PSC_CONF['keywords']:
            string = f"<span class=\"{keyword[1]}\">{keyword[0]}</span>".join(string.split(keyword[0]))
        for spe_name in self.spe_names:
            keyword = " ".join(spe_name.split("__")).split(":")
            string = f"<span class=\"{keyword[1]}\">{keyword[0]}</span>".join(string.split(keyword[0]))

        lines = string.split('\n')
        lidx = 0
        for line in lines:
            i = 0
            while i < len(line) and (line[i] == ' ' or line[i] == '\t'):
                i += 1
            
            if i < len(line) and i + 1 < len(line) and line[i:i+2] == "//":
                conf_comment = PSC_CONF['comments']
                lines[lidx] = f"<span class=\"{conf_comment}\">{line}</span>"
            lidx += 1

        return lines

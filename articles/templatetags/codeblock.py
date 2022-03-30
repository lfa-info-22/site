
from django import template

register = template.Library()

@register.tag()
def codeblock(parser, token):
    nodelist = parser.parse(('endcodeblock', ))
    parser.delete_first_token()
    return CodeBlockNode(nodelist)

class CodeBlockNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        output = self.nodelist.render(context)

        

        return output

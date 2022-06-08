
from django import template
from django.template.loader import render_to_string

register = template.Library()

@register.tag()
def textblock(parser, token):
    nodelist = parser.parse(('endtextblock', ))
    parser.delete_first_token()
    content = token.split_contents()
    return TextBlockNode(nodelist)

class TextBlockNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context) -> str:
        output = self.nodelist.render(context)

        return render_to_string('home/text/base.html', { 'text' : output }, None)

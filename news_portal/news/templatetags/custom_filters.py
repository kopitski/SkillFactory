from django import template
import re

register = template.Library()

not_allowed = ['RT', 'ТАСС', 'Монако']

@register.filter()

def censor(text: str):
   for word in not_allowed:
       text = re.sub(word, "*" * len(word), text)
   return text
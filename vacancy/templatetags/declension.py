from django import template
import pymorphy2

register = template.Library()


@register.filter(name='decl')
def declension(query):
    morph = pymorphy2.MorphAnalyzer()
    vacancy = morph.parse('вакансия')[0]
    if isinstance(query, int):
        return '{} {}'.format(query, vacancy.make_agree_with_number(query).word)
    else:
        return '{} {}'.format(len(query), vacancy.make_agree_with_number(len(query)).word)

from django import template
from rango.models import Submission

register = template.Library()


@register.inclusion_tag('rango/submission_dropdown.html')
def submission_dropdown(current_page=None):
    return {'current_page': current_page}

from django import template

# Custom Template Tags & Filters
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/
register = template.Library()

""" Custom Filters """
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#writing-custom-template-filters

# @register.filter(name="prev_page")
@register.filter
def multiply(value, arg):
    return value * arg


""" Custom Tags """
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#writing-custom-template-tags

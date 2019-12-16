from django import template

# Custom Template Tags & Filters
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/
register = template.Library()

languageDict = {
    "en": "English",
    "ko": "Korean",
}

""" Custom Filters """
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#writing-custom-template-filters

# @register.filter(name="prev_page")
@register.filter
def selected_choice(field_name):
    return languageDict[field_name]


""" Custom Tags """
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#writing-custom-template-tags

from django import template

# Custom Template Tags & Filters
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/
register = template.Library()

month3letters = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)

""" Custom Filters """
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#writing-custom-template-filters

# @register.filter(name="prev_page")
@register.filter
def month_name(month_num):
    if month_num > 0 and month_num < 13:
        return month3letters[month_num - 1]
    return ""


""" Custom Tags """
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#writing-custom-template-tags

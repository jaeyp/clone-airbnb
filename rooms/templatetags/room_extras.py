from django import template

# Custom Template Tags & Filters
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/
register = template.Library()


""" Custom Filters """
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#writing-custom-template-filters

# @register.filter(name="prev_page")
@register.filter  # we can skip to set filter name in case function and filter has the same name
def prev_page(value):

    split = value.split("&")
    for s in split:
        if "page=" in s:
            page_num = str(int(s.replace("page=", "")) - 1)
            value = value.replace(s, "page=" + page_num)
    return value


@register.filter(name="clear_page")
def clear_page(value):

    split = value.split("&")
    for s in split:
        if "page=" in s:
            split.remove(s)
    return "&".join(split)


@register.filter(name="next_page")
def next_page(value):

    split = value.split("&")
    for s in split:
        if "page=" in s:
            page_num = str(int(s.replace("page=", "")) + 1)
            value = value.replace(s, "page=" + page_num)
    return value


""" Custom Tags """
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#writing-custom-template-tags

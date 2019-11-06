from django import template

register = template.Library()


@register.filter(name="prev_page")
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

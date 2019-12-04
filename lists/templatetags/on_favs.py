from django import template
from lists import models as list_models

register = template.Library()

# Writing custom template tags
# https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#simple-tags
# @register.simple_tag(takes_context=True)


@register.simple_tag(takes_context=True)
def on_favs(context, room):  # we can get the user info from request, so we need only two arguments here.
    user = context.request.user
    fav_list = list_models.WishList.objects.get_or_none(user=user, name=f"{user.first_name}'s favourites")
    if fav_list is not None:
        return room in fav_list.rooms.all()
    else:
        return False

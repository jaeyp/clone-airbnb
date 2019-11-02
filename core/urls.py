from django.urls import path
from rooms import views as room_views

app_name = "core"

""" Function Based Views """
# urlpatterns = [path("", room_views.all_rooms, name="home")]

""" Class Based Views
    the second parameter (view) should be the result fo as_view() for CBV
    which provides a function-like entry to class-based views.
"""
# if you don't want to use the given template name from CBV,
# set template_name as an argument of as_view(), or inside HomeView class
urlpatterns = [path("", room_views.HomeView.as_view(template_name="rooms/home4cbv.html"), name="home")]

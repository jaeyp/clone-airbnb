from django.urls import path
from rooms import views as room_views

app_name = "core"

""" Function Based Views """
# urlpatterns = [path("", room_views.all_rooms, name="home")]

""" Class Based Views """
# HomeView is a class, not a function,
# so we point the URL to the as_view() class method instead,
# which provides a function-like entry to class-based views:
urlpatterns = [path("", room_views.HomeView.as_view(), name="home")]

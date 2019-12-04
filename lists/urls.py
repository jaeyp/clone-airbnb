from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    # {% url 'lists:toggle-room' room.pk %}
    path("toggle/<int:room_pk>", views.toggle_room, name="toggle-room"),
    # {% url 'lists:show-favs' %}
    # path("favs/", views.show_favs, name="show-favs"),
    path("favs/", views.ShowFavsView.as_view(), name="show-favs"),
]

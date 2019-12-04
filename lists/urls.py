from django.urls import path
from . import views

app_name = "lists"

urlpatterns = [
    path("toggle/<int:room_pk>", views.toggle_room, name="toggle-room"),
    # path("favs/", views.show_favs, name="show-favs"),
    path("favs/", views.ShowFavsView.as_view(), name="show-favs"),
]

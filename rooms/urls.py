from django.urls import path
from . import views

app_name = "rooms"

""" Function Based Views """
# urlpatterns = [path("<int:id>", views.room_detail, name="detail")]


""" Class Based Views """
# you must use a primary key for DetailView (in this case, use 'pk' istead of 'id')
# Generic detail view RoomDetailView must be called with either an object pk or a slug in the URLconf.
# urlpatterns = [path("<int:pk>", views.RoomDetailView.as_view(template_name="rooms/detail4cbv.html"), name="detail")]

# With pk_url_kwarg = "id"
urlpatterns = [
    path("<int:id>", views.RoomDetailView.as_view(template_name="rooms/detail4cbv.html"), name="detail"),
    path("search/", views.search, name="search"),
]

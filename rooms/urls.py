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
    path("<int:pk>/", views.RoomDetailView.as_view(template_name="rooms/detail4cbv.html"), name="detail"),
    # TODO: room photo gallery
    # path("<int:pk>/", views.RoomPhotoView.as_view(), name="photos"),
    # {% url 'rooms:edit' room.pk %}
    path("<int:pk>/edit/", views.RoomEditView.as_view(), name="edit"),  # rooms:edit
    # {% url 'rooms:photos' room.pk %}
    path("<int:pk>/photos/", views.RoomPhotosView.as_view(), name="photos"),  # rooms:photos
    # {% url 'rooms:delete-photo' room.pk photo.pk %}
    path("<int:room_pk>/photos/<int:photo_pk>/delete/", views.delete_photo, name="delete-photo"),
    path("search/", views.SearchView.as_view(), name="search"),  # rooms:search
    # path("search/", views.search, name="search"),
]

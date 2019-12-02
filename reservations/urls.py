from django.urls import path
from . import views

app_name = "reservations"

urlpatterns = [
    # path("create/<int:room_pk>/<int:year>-<int:month>-<int:day>-<int:days>/", views.create, name="create",),
    path("create/<int:room_pk>/", views.create, name="create",),
    path("review/<int:pk>/", views.ReservationReviewView.as_view(), name="review",),
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="detail",),
    path("<int:pk>/<str:command>", views.edit, name="edit",),
]
